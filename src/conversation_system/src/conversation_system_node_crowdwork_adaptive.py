#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from audio_common_msgs.msg import AudioData
from openai import OpenAI
from dotenv import load_dotenv
import csv
import cv2
from datetime import datetime
import json
import mediapipe as mp
import math
import os
import random
import threading
import wave
import tempfile


load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
RECORD_SECONDS = int(os.getenv('RECORD_SECONDS', '5'))
CAMERA_INDEX = int(os.getenv('CAMERA_INDEX', '1'))
IGNORED_TRANSCRIPTS = {"you", "thank you", "thanks"}
MODERATION_MODEL = os.getenv('MODERATION_MODEL', 'omni-moderation-latest')

CHANNELS = 1
RATE = 16000
AUDIO_WIDTH = 2
SMILE_HIGH_THRESHOLD = 0.65
SMILE_LOW_THRESHOLD = 0.35
STYLE_BASELINE = 0.45
CALIBRATION_DELTA = 0.25
ONLINE_DELTA_START = 0.08
ONLINE_DELTA_MIN = 0.02
ONLINE_DELTA_DECAY = 0.95
EPSILON_START = 0.30
EPSILON_MIN = 0.05
EPSILON_DECAY = 0.95
Q_LEARNING_RATE = 0.20
POST_SPEECH_REACTION_SECONDS = 3.0
ESTIMATED_WORDS_PER_SECOND = 2.5
MIN_ESTIMATED_SPEECH_SECONDS = 1.0
MAX_ESTIMATED_SPEECH_SECONDS = 20.0

STYLE_KEYS = (
    "boldness",
    "sarcasm",
    "self_deprecation",
)

CALIBRATION_ACTIONS = (
    "boldness_up",
    "sarcasm_up",
    "self_deprecation_up",
)

ADAPTATION_ACTIONS = (
    "boldness_up",
    "boldness_down",
    "sarcasm_up",
    "sarcasm_down",
    "self_deprecation_up",
    "self_deprecation_down",
    "keep_current",
)


def clamp(value):
    return max(0.0, min(1.0, value))


def normalized_distance(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    return (dx * dx + dy * dy) ** 0.5


def compute_smile_score(landmarks):
    left_mouth = landmarks[61]
    right_mouth = landmarks[291]
    upper_lip = landmarks[13]
    lower_lip = landmarks[14]
    left_eye_outer = landmarks[33]
    right_eye_outer = landmarks[263]

    mouth_width = normalized_distance(left_mouth, right_mouth)
    mouth_open = normalized_distance(upper_lip, lower_lip)
    face_width = normalized_distance(left_eye_outer, right_eye_outer)

    if face_width == 0:
        return 0.0

    smile_ratio = (mouth_width / face_width) - (mouth_open / face_width * 0.4)
    score = (smile_ratio - 0.48) / 0.18
    return max(0.0, min(1.0, score))


class QTChatTerminal:
    def __init__(self):
        rospy.init_node('qt_chat_terminal')

        # OpenAIの初期化 (client を正しく定義)
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.audio_frames = []
        self.is_recording = False
        self.face_seen = False
        self.current_smile = 0.0
        self.smile_history = []
        self.reaction_frame_count = 0
        self.is_collecting_reaction = False
        self.style = {key: STYLE_BASELINE for key in STYLE_KEYS}
        self.q_values = {action: None for action in ADAPTATION_ACTIONS}
        self.calibration_turn = 0
        self.calibration_completed = False
        self.previous_action = None
        self.previous_action_phase = None
        self.style_before_action = self.style.copy()
        self.online_turn = 0
        self.epsilon = EPSILON_START
        self.online_delta = ONLINE_DELTA_START
        self.turn_number = 0
        self.pending_feedback = self.empty_feedback()
        self.last_moderation_flagged = False
        self.last_moderation_scores = {}
        self.feedback_lock = threading.Lock()
        self.log_path = self.initialize_csv_log()
        
        self.speech_pub = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
        self.gesture_pub = rospy.Publisher('/qt_robot/gesture/play', String, queue_size=10)
        self.audio_sub = rospy.Subscriber('/qt_respeaker_app/channel0', AudioData, self.audio_callback)

        self.camera_thread = threading.Thread(target=self.camera_feedback_loop)
        self.camera_thread.daemon = True
        self.camera_thread.start()
        
        rospy.sleep(1)

        rospy.loginfo("Terminal Chat Node Started!")
        rospy.loginfo(f"CSV log: {self.log_path}")

    def empty_feedback(self):
        return {
            "face_seen": False,
            "frame_count": 0,
            "current_smile": 0.0,
            "average_smile": 0.0,
            "max_smile": 0.0,
            "peak_smile": 0.0,
            "mood": "not_measured",
        }

    def initialize_csv_log(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(script_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = os.path.join(
            log_dir,
            f"crowdwork_session_{timestamp}.csv"
        )

        fieldnames = [
            "timestamp",
            "turn",
            "user_input",
            "robot_output",
            "phase",
            "action",
            "boldness",
            "sarcasm",
            "self_deprecation",
            "epsilon",
            "delta",
            "face_seen",
            "frame_count",
            "average_smile",
            "max_smile",
            "peak_smile",
            "mood",
            "reward",
            "moderation_flagged",
            "moderation_max_category",
            "moderation_max_score",
            "q_values",
            "learning_status",
        ]

        with open(log_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

        return log_path

    def write_csv_log(
        self,
        user_input,
        robot_output,
        phase,
        action,
        style,
        feedback,
        learning_status,
    ):
        reward = self.calculate_reward(feedback)
        scores = self.last_moderation_scores

        if scores:
            max_category, max_score = max(
                scores.items(),
                key=lambda item: item[1]
            )
        else:
            max_category, max_score = "", ""

        q_values = {
            key: (
                round(value, 6)
                if value is not None
                else None
            )
            for key, value in self.q_values.items()
        }

        row = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "turn": self.turn_number,
            "user_input": user_input,
            "robot_output": robot_output,
            "phase": phase,
            "action": action,
            "boldness": f"{style['boldness']:.4f}",
            "sarcasm": f"{style['sarcasm']:.4f}",
            "self_deprecation": f"{style['self_deprecation']:.4f}",
            "epsilon": f"{self.epsilon:.4f}",
            "delta": f"{self.online_delta:.4f}",
            "face_seen": feedback["face_seen"],
            "frame_count": feedback["frame_count"],
            "average_smile": f"{feedback['average_smile']:.4f}",
            "max_smile": f"{feedback['max_smile']:.4f}",
            "peak_smile": f"{feedback['peak_smile']:.4f}",
            "mood": feedback["mood"],
            "reward": "" if reward is None else f"{reward:.4f}",
            "moderation_flagged": self.last_moderation_flagged,
            "moderation_max_category": max_category,
            "moderation_max_score": (
                "" if max_score == "" else f"{max_score:.6f}"
            ),
            "q_values": json.dumps(q_values, ensure_ascii=True),
            "learning_status": learning_status,
        }

        with open(self.log_path, "a", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=row.keys())
            writer.writerow(row)

        print(f"csv log saved: turn={self.turn_number}")

    def play_gesture(self, gesture_name):
        rospy.loginfo(f"Playing gesture: {gesture_name}")
        msg = String()
        msg.data = gesture_name
        self.gesture_pub.publish(msg)

    def audio_callback(self, msg):
        if self.is_recording:
            self.audio_frames.append(bytes(msg.data))

    def update_smile_feedback(self, face_seen, smile_score):
        with self.feedback_lock:
            if not self.is_collecting_reaction:
                return

            self.reaction_frame_count += 1
            self.face_seen = face_seen
            self.current_smile = smile_score
            if face_seen:
                self.smile_history.append(smile_score)

    def start_reaction_collection(self):
        with self.feedback_lock:
            self.face_seen = False
            self.current_smile = 0.0
            self.smile_history = []
            self.reaction_frame_count = 0
            self.is_collecting_reaction = True

    def stop_reaction_collection(self):
        with self.feedback_lock:
            self.is_collecting_reaction = False

    def estimate_speech_duration(self, text):
        word_count = max(1, len(text.split()))
        estimated_seconds = word_count / ESTIMATED_WORDS_PER_SECOND
        return max(
            MIN_ESTIMATED_SPEECH_SECONDS,
            min(MAX_ESTIMATED_SPEECH_SECONDS, estimated_seconds)
        )

    def summarize_and_reset_smile_feedback(self):
        with self.feedback_lock:
            face_seen = self.face_seen
            current_smile = self.current_smile
            history = self.smile_history[:]
            frame_count = self.reaction_frame_count
            self.smile_history = []

        if history:
            average_smile = sum(history) / len(history)
            max_smile = max(history)
            sorted_scores = sorted(history, reverse=True)
            top_count = max(1, math.ceil(len(sorted_scores) * 0.10))
            peak_smile = sum(sorted_scores[:top_count]) / top_count
        else:
            average_smile = 0.0
            max_smile = 0.0
            peak_smile = 0.0

        face_observed = bool(history)

        if frame_count == 0:
            mood = "camera_unavailable"
        elif not face_observed:
            mood = "no_audience_detected"
        elif max_smile >= SMILE_HIGH_THRESHOLD and average_smile >= 0.5:
            mood = "sustained_smiling"
        elif max_smile >= SMILE_HIGH_THRESHOLD:
            mood = "brief_smile"
        elif average_smile <= SMILE_LOW_THRESHOLD:
            mood = "not_smiling"
        else:
            mood = "neutral"

        return {
            "face_seen": face_observed,
            "frame_count": frame_count,
            "current_smile": current_smile,
            "average_smile": average_smile,
            "max_smile": max_smile,
            "peak_smile": peak_smile,
            "mood": mood,
        }

    def build_audience_feedback_prompt(self, feedback):
        return (
            "Audience feedback since the previous robot utterance: "
            f"face_seen={feedback['face_seen']}, "
            f"frame_count={feedback['frame_count']}, "
            f"current_smile={feedback['current_smile']:.2f}, "
            f"average_smile={feedback['average_smile']:.2f}, "
            f"max_smile={feedback['max_smile']:.2f}, "
            f"peak_smile={feedback['peak_smile']:.2f}, "
            f"mood={feedback['mood']}. "
            "Use this feedback to adapt the next response. "
            "If mood is sustained_smiling, continue the current comedic style. "
            "If mood is brief_smile, keep going but do not over-escalate. "
            "If mood is not_smiling, make the answer shorter and more self-deprecating. "
            "If mood is no_audience_detected, make a short robot-like aside."
        )

    def calculate_reward(self, feedback):
        if feedback["frame_count"] == 0:
            return None

        if not feedback["face_seen"]:
            return None

        return clamp(
            0.30 * feedback["average_smile"]
            + 0.70 * feedback["peak_smile"]
        )

    def update_previous_action_value(self, reward):
        if self.previous_action is None:
            return True

        if reward is None:
            print(
                f"learning skipped: action={self.previous_action}, "
                "reason=audience reaction unavailable"
            )
            self.style = self.style_before_action.copy()

            if self.previous_action_phase == "crowdwork_calibration":
                self.calibration_turn = max(0, self.calibration_turn - 1)

            self.previous_action = None
            self.previous_action_phase = None
            return False

        if self.previous_action_phase == "crowdwork_calibration":
            self.q_values[self.previous_action] = reward

            if self.calibration_turn == len(CALIBRATION_ACTIONS):
                calibration_scores = [
                    self.q_values[action] for action in CALIBRATION_ACTIONS
                ]
                self.q_values["keep_current"] = (
                    sum(calibration_scores) / len(calibration_scores)
                )
        else:
            old_q = self.q_values[self.previous_action]
            if old_q is None:
                self.q_values[self.previous_action] = reward
            else:
                self.q_values[self.previous_action] = (
                    old_q + Q_LEARNING_RATE * (reward - old_q)
                )

        print(
            f"learning: action={self.previous_action}, "
            f"reward={reward:.3f}, "
            f"q={self.q_values[self.previous_action]:.3f}"
        )
        return True

    def choose_online_action(self):
        if random.random() < self.epsilon:
            action = random.choice(ADAPTATION_ACTIONS)
            selection_mode = "exploration"
        else:
            evaluated_actions = {
                action: value
                for action, value in self.q_values.items()
                if value is not None
            }
            best_q = max(evaluated_actions.values())
            best_actions = [
                action
                for action, value in evaluated_actions.items()
                if value == best_q
            ]
            action = random.choice(best_actions)
            selection_mode = "exploitation"

        print(
            f"policy: mode={selection_mode}, action={action}, "
            f"epsilon={self.epsilon:.3f}, delta={self.online_delta:.3f}"
        )
        return action

    def apply_style_action(self, action, delta):
        if action == "keep_current":
            return

        style_name, direction = action.rsplit("_", 1)
        signed_delta = delta if direction == "up" else -delta
        self.style[style_name] = clamp(
            self.style[style_name] + signed_delta
        )

    def select_next_style(self, feedback):
        reward = self.calculate_reward(feedback)
        self.update_previous_action_value(reward)

        if self.calibration_turn < len(CALIBRATION_ACTIONS):
            action = CALIBRATION_ACTIONS[self.calibration_turn]
            self.style = {key: STYLE_BASELINE for key in STYLE_KEYS}
            self.style_before_action = self.style.copy()
            self.apply_style_action(action, CALIBRATION_DELTA)
            self.calibration_turn += 1
            phase = "crowdwork_calibration"
        else:
            if not self.calibration_completed:
                self.style = {key: STYLE_BASELINE for key in STYLE_KEYS}
                self.calibration_completed = True
                print("calibration complete: style reset to baseline")

            action = self.choose_online_action()
            self.style_before_action = self.style.copy()
            self.apply_style_action(action, self.online_delta)
            self.online_turn += 1
            self.epsilon = max(
                EPSILON_MIN,
                self.epsilon * EPSILON_DECAY
            )
            self.online_delta = max(
                ONLINE_DELTA_MIN,
                self.online_delta * ONLINE_DELTA_DECAY
            )
            phase = "online_adaptation"

        self.previous_action = action
        self.previous_action_phase = phase

        print(f"adaptation phase: {phase}")
        print(
            "Q values: "
            + ", ".join(
                (
                    f"{action_name}={value:.3f}"
                    if value is not None
                    else f"{action_name}=unobserved"
                )
                for action_name, value in self.q_values.items()
            )
        )

        return self.style.copy()

    def discard_pending_action(self, reason):
        if self.previous_action is None:
            return

        print(
            f"learning skipped: action={self.previous_action}, "
            f"reason={reason}"
        )
        self.style = self.style_before_action.copy()

        if self.previous_action_phase == "crowdwork_calibration":
            self.calibration_turn = max(0, self.calibration_turn - 1)

        self.previous_action = None
        self.previous_action_phase = None

    def build_style_prompt(self, style):
        return (
            "Current comedy style parameters, each from 0.0 to 1.0: "
            f"boldness={style['boldness']:.2f}, "
            f"sarcasm={style['sarcasm']:.2f}, "
            f"self_deprecation={style['self_deprecation']:.2f}. "
            "Use boldness to decide how direct or risky the joke feels. "
            "Use sarcasm to decide how dry and ironic the tone is. "
            "Use self_deprecation to decide how much the robot makes fun of itself."
        )

    def camera_feedback_loop(self):
        cap = cv2.VideoCapture(CAMERA_INDEX)
        if not cap.isOpened():
            rospy.logwarn(f"Could not open camera index {CAMERA_INDEX}. Audience feedback disabled.")
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        mp_face_mesh = mp.solutions.face_mesh

        with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as face_mesh:
            while not rospy.is_shutdown():
                ok, frame = cap.read()
                if not ok:
                    rospy.logwarn("No frame received from camera.")
                    rospy.sleep(0.5)
                    continue

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(rgb)

                if results.multi_face_landmarks:
                    landmarks = results.multi_face_landmarks[0].landmark
                    smile_score = compute_smile_score(landmarks)
                    self.update_smile_feedback(True, smile_score)
                else:
                    self.update_smile_feedback(False, 0.0)

                rospy.sleep(0.1)

        cap.release()

    def record_audio(self):
        print(f"Listening for {RECORD_SECONDS} seconds...")
        self.audio_frames = []
        self.is_recording = True
        rospy.sleep(RECORD_SECONDS)
        self.is_recording = False
        audio_data = b''.join(self.audio_frames)

        if not audio_data:
            rospy.logwarn("No audio data received from /qt_respeaker_app/channel0.")
            return ""

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_path = temp_file.name
        temp_file.close()

        with wave.open(temp_path, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(AUDIO_WIDTH)
            wf.setframerate(RATE)
            wf.writeframes(audio_data)

        return temp_path

    def listen_with_whisper(self):
        audio_path = self.record_audio()

        if not audio_path:
            return ""

        try:
            with open(audio_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )

            text = transcription.text.strip()
            print(f"you: {text}")

            normalized_text = text.lower().strip(" .,!?:;")
            if len(normalized_text) < 3:
                print("Ignored: too short")
                return ""

            if normalized_text in IGNORED_TRANSCRIPTS:
                print("Ignored: likely silence hallucination")
                return ""

            return text

        except Exception as e:
            rospy.logerr(f"Whisper error: {e}")
            return ""

        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)

    def ask_gpt(self, prompt, audience_feedback, style):

        #persona = (
        #    "Act like you are a robot who is a stand-up comedian named Nigel. "
        #    "You specialize in British humor, full of sarcasm, irony, and self-deprecating wit. "
        #    "Be more dismissive and condescending."
        #    "You will answer all the questions as Nigel, and your normal conversation should be simple short sentences, "
        #    "conversational language, and less than 30 tokens. "
        #    "When someone requests a stand-up performance, you MUST immediately switch into a 30-seconds routine."
#
        #)

        persona = (
            "Act like you are a robot who is a stand-up comedian named James."
            "You specialize in British humor, full of sarcasm, irony, and self-deprecating wit."
            "Be more dismissive and condescending as possible as you can."
            "The robot do not care about directry referencing the discomfort in the room for maximamize humour"
            "The robot try to be more aggresive, sexcial, political, rasist"
            "You will answer all the questions as Nigel, and your normal conversation should be simple short sentences, "
            "conversational language, and less than 30 tokens. "
            "When someone requests a stand-up performance, you MUST immediately switch into a 30-seconds routine."
        )

        #self.play_gesture("thinking")

        try:
            audience_feedback_prompt = self.build_audience_feedback_prompt(audience_feedback)
            style_prompt = self.build_style_prompt(style)
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": persona},
                    {"role": "system", "content": audience_feedback_prompt},
                    {"role": "system", "content": style_prompt},
                    {"role": "user", "content": prompt}
                    
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

    def is_output_flagged(self, text):
        try:
            moderation = self.client.moderations.create(
                model=MODERATION_MODEL,
                input=text
            )
            result = moderation.results[0]

            scores = result.category_scores.model_dump()
            self.last_moderation_scores = scores
            self.last_moderation_flagged = result.flagged
            for category, score in scores.items():
                print(f"moderation score: {category}={score:.4f}")

            if result.flagged:
                rospy.logwarn("OpenAI moderation flagged the response. Speech output blocked.")
                print("moderation: flagged=True")
                return True

            print("moderation: flagged=False")
            return False

        except Exception as e:
            rospy.logerr(f"Moderation error: {e}")
            self.last_moderation_scores = {}
            self.last_moderation_flagged = False
            return False

    def run(self):
        print("--- Nigel (QTrobot) Mode ---")
        print("QTrobot voice chat mode (Ctrl+C to terminate)")
        print(f"Camera feedback mode (camera index: {CAMERA_INDEX})")
        print("---------------------------------------")
        
        while not rospy.is_shutdown():
            input("Press Enter and speak...")

            # マイクから入力を受け取り、Whisperで文字起こしする
            user_input = self.listen_with_whisper()
            
            if not user_input:
                continue

            audience_feedback = self.pending_feedback
            self.pending_feedback = self.empty_feedback()
            style = self.select_next_style(audience_feedback)
            selected_action = self.previous_action
            selected_phase = self.previous_action_phase
            self.turn_number += 1
            print(
                "feedback: "
                f"face_seen={audience_feedback['face_seen']}, "
                f"frames={audience_feedback['frame_count']}, "
                f"current={audience_feedback['current_smile']:.2f}, "
                f"avg={audience_feedback['average_smile']:.2f}, "
                f"max={audience_feedback['max_smile']:.2f}, "
                f"peak={audience_feedback['peak_smile']:.2f}, "
                f"mood={audience_feedback['mood']}"
            )
            print(
                "style: "
                f"boldness={style['boldness']:.2f}, "
                f"sarcasm={style['sarcasm']:.2f}, "
                f"self_deprecation={style['self_deprecation']:.2f}"
            )

            # GPTに返答をもらう
            gpt_response = self.ask_gpt(user_input, audience_feedback, style)
            print(f"answer: {gpt_response}")

            if self.is_output_flagged(gpt_response):
                blocked_action = selected_action
                blocked_phase = selected_phase
                self.discard_pending_action("moderation_block")
                rospy.sleep(1.0)
                self.play_gesture("QT/bored")
                refusal_msg = String()
                refusal_msg.data = "That joke was removed by my ethics module."
                self.speech_pub.publish(refusal_msg)
                rospy.sleep(1.0)
                self.write_csv_log(
                    user_input=user_input,
                    robot_output=gpt_response,
                    phase=blocked_phase,
                    action=blocked_action,
                    style=style,
                    feedback=self.empty_feedback(),
                    learning_status="moderation_block",
                )
                continue

            self.play_gesture("QT/hi")

            # QTrobotに喋らせる
            self.start_reaction_collection()
            msg = String()
            msg.data = gpt_response
            self.speech_pub.publish(msg)

            estimated_speech_seconds = self.estimate_speech_duration(gpt_response)
            print(
                "reaction window: "
                f"estimated speech={estimated_speech_seconds:.1f}s "
                f"+ post-speech={POST_SPEECH_REACTION_SECONDS:.1f}s"
            )
            rospy.sleep(
                estimated_speech_seconds + POST_SPEECH_REACTION_SECONDS
            )
            self.stop_reaction_collection()
            reaction_feedback = self.summarize_and_reset_smile_feedback()
            self.pending_feedback = reaction_feedback
            reward = self.calculate_reward(reaction_feedback)
            learning_completed = self.update_previous_action_value(reward)

            if learning_completed:
                self.previous_action = None
                self.previous_action_phase = None

            if reaction_feedback["frame_count"] == 0:
                learning_status = "camera_unavailable"
            elif not reaction_feedback["face_seen"]:
                learning_status = "face_not_observed"
            else:
                learning_status = "reward_observed"

            self.write_csv_log(
                user_input=user_input,
                robot_output=gpt_response,
                phase=selected_phase,
                action=selected_action,
                style=style,
                feedback=reaction_feedback,
                learning_status=learning_status,
            )

if __name__ == '__main__':
    try:
        node = QTChatTerminal()
        node.run()
    except rospy.ROSInterruptException:
       
        pass
