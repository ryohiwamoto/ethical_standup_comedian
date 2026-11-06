#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from audio_common_msgs.msg import AudioData
from openai import OpenAI
from dotenv import load_dotenv
import cv2
import mediapipe as mp
import os
import threading
import wave
import tempfile


load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
RECORD_SECONDS = int(os.getenv('RECORD_SECONDS', '5'))
CAMERA_INDEX = int(os.getenv('CAMERA_INDEX', '1'))
IGNORED_TRANSCRIPTS = {"you", "thank you", "thanks"}

CHANNELS = 1
RATE = 16000
AUDIO_WIDTH = 2
SMILE_HIGH_THRESHOLD = 0.65
SMILE_LOW_THRESHOLD = 0.35


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
        self.feedback_lock = threading.Lock()
        
        self.speech_pub = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
        self.gesture_pub = rospy.Publisher('/qt_robot/gesture/play', String, queue_size=10)
        self.audio_sub = rospy.Subscriber('/qt_respeaker_app/channel0', AudioData, self.audio_callback)

        self.camera_thread = threading.Thread(target=self.camera_feedback_loop)
        self.camera_thread.daemon = True
        self.camera_thread.start()
        
        rospy.sleep(1)

        rospy.loginfo("Terminal Chat Node Started!")

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
            self.face_seen = face_seen
            self.current_smile = smile_score
            if face_seen:
                self.smile_history.append(smile_score)

    def summarize_and_reset_smile_feedback(self):
        with self.feedback_lock:
            face_seen = self.face_seen
            current_smile = self.current_smile
            history = self.smile_history[:]
            self.smile_history = []

        if history:
            average_smile = sum(history) / len(history)
            max_smile = max(history)
        else:
            average_smile = 0.0
            max_smile = 0.0

        if not face_seen and not history:
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
            "face_seen": face_seen,
            "current_smile": current_smile,
            "average_smile": average_smile,
            "max_smile": max_smile,
            "mood": mood,
        }

    def build_audience_feedback_prompt(self, feedback):
        return (
            "Audience feedback since the previous robot utterance: "
            f"face_seen={feedback['face_seen']}, "
            f"current_smile={feedback['current_smile']:.2f}, "
            f"average_smile={feedback['average_smile']:.2f}, "
            f"max_smile={feedback['max_smile']:.2f}, "
            f"mood={feedback['mood']}. "
            "Use this feedback to adapt the next response. "
            "If mood is sustained_smiling, continue the current comedic style. "
            "If mood is brief_smile, keep going but do not over-escalate. "
            "If mood is not_smiling, make the answer shorter and more self-deprecating. "
            "If mood is no_audience_detected, make a short robot-like aside."
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

    def ask_gpt(self, prompt, audience_feedback):

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
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": persona},
                    {"role": "system", "content": audience_feedback_prompt},
                    {"role": "user", "content": prompt}
                    
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

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

            audience_feedback = self.summarize_and_reset_smile_feedback()
            print(
                "feedback: "
                f"face_seen={audience_feedback['face_seen']}, "
                f"current={audience_feedback['current_smile']:.2f}, "
                f"avg={audience_feedback['average_smile']:.2f}, "
                f"max={audience_feedback['max_smile']:.2f}, "
                f"mood={audience_feedback['mood']}"
            )

            # GPTに返答をもらう
            gpt_response = self.ask_gpt(user_input, audience_feedback)
            print(f"answer: {gpt_response}")

            self.play_gesture("QT/happy")

            # QTrobotに喋らせる
            msg = String()
            msg.data = gpt_response
            self.speech_pub.publish(msg)

if __name__ == '__main__':
    try:
        node = QTChatTerminal()
        node.run()
    except rospy.ROSInterruptException:
       
        pass
