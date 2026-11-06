#!/usr/bin/env python3
import os
import tempfile
import wave

import rospy
from audio_common_msgs.msg import AudioData
from dotenv import load_dotenv
from openai import OpenAI
from std_msgs.msg import String


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RECORD_SECONDS = int(os.getenv("RECORD_SECONDS", "5"))
IGNORED_TRANSCRIPTS = {"you", "thank you", "thanks"}

CHANNELS = 1
RATE = 16000
AUDIO_WIDTH = 2


class QTSimpleChat:
    def __init__(self):
        rospy.init_node("qt_simple_chat")

        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.audio_frames = []
        self.is_recording = False
        self.speech_pub = rospy.Publisher(
            "/qt_robot/speech/say",
            String,
            queue_size=10,
        )
        self.gesture_pub = rospy.Publisher(
            "/qt_robot/gesture/play",
            String,
            queue_size=10,
        )
        self.audio_sub = rospy.Subscriber(
            "/qt_respeaker_app/channel0",
            AudioData,
            self.audio_callback,
        )

        rospy.sleep(1.0)
        rospy.loginfo("QT simple chat node started.")

    def audio_callback(self, msg):
        if self.is_recording:
            self.audio_frames.append(bytes(msg.data))

    def publish_text(self, publisher, text):
        msg = String()
        msg.data = text
        publisher.publish(msg)

    def say(self, text):
        rospy.loginfo(f"Speech: {text}")
        self.publish_text(self.speech_pub, text)

    def play_gesture(self, gesture_name):
        rospy.loginfo(f"Gesture: {gesture_name}")
        self.publish_text(self.gesture_pub, gesture_name)

    def record_audio(self):
        print(f"Listening for {RECORD_SECONDS} seconds...")
        self.audio_frames = []
        self.is_recording = True
        rospy.sleep(RECORD_SECONDS)
        self.is_recording = False
        audio_data = b"".join(self.audio_frames)

        if not audio_data:
            rospy.logwarn("No audio data received from /qt_respeaker_app/channel0.")
            return ""

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_path = temp_file.name
        temp_file.close()

        with wave.open(temp_path, "wb") as wf:
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
                    language="en",
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

    def ask_gpt(self, user_input):
        system_prompt = (
            "Your name is QT robot. "
            "You are a friendly social robot. "
            "Answer naturally and briefly in conversational English. "
            "Keep responses short enough for a robot to speak aloud."
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            rospy.logerr(f"OpenAI API error: {e}")
            return "Sorry, I had a connection problem."

    def run(self):
        print("--- QT Simple Chat ---")
        print("Press Enter and speak.")
        print("Use Ctrl+C to quit.")
        print("----------------------")

        while not rospy.is_shutdown():
            input("Press Enter and speak...")
            user_input = self.listen_with_whisper()
            if not user_input:
                continue

            answer = self.ask_gpt(user_input)
            print(f"QT: {answer}")

            self.play_gesture("QT/hi")
            self.say(answer)


if __name__ == "__main__":
    try:
        node = QTSimpleChat()
        node.run()
    except rospy.ROSInterruptException:
        pass
