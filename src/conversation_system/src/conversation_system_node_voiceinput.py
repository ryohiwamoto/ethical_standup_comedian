#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from openai import OpenAI
from dotenv import load_dotenv
import os
import wave
import tempfile
import pyaudio


load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
RECORD_SECONDS = int(os.getenv('RECORD_SECONDS', '5'))
IGNORED_TRANSCRIPTS = {"you", "thank you", "thanks"}

AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024


class QTChatTerminal:
    def __init__(self):
        rospy.init_node('qt_chat_terminal')

        # OpenAIの初期化 (client を正しく定義)
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
        self.speech_pub = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
        self.gesture_pub = rospy.Publisher('/qt_robot/gesture/play', String, queue_size=10)
        
        rospy.sleep(1)

        rospy.loginfo("Terminal Chat Node Started!")

    def play_gesture(self, gesture_name):
        rospy.loginfo(f"Playing gesture: {gesture_name}")
        msg = String()
        msg.data = gesture_name
        self.gesture_pub.publish(msg)

    def record_audio(self):
        audio = pyaudio.PyAudio()

        stream = audio.open(
            format=AUDIO_FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )

        print(f"Listening for {RECORD_SECONDS} seconds...")
        frames = []

        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_path = temp_file.name
        temp_file.close()

        with wave.open(temp_path, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(AUDIO_FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        return temp_path

    def listen_with_whisper(self):
        audio_path = self.record_audio()

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

    def ask_gpt(self, prompt):

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
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": persona},
                    {"role": "user", "content": prompt}
                    
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

    def run(self):
        print("--- Nigel (QTrobot) Mode ---")
        print("QTrobot voice chat mode (Ctrl+C to terminate)")
        print("---------------------------------------")
        
        while not rospy.is_shutdown():
            input("Press Enter and speak...")

            # マイクから入力を受け取り、Whisperで文字起こしする
            user_input = self.listen_with_whisper()
            
            if not user_input:
                continue

            # GPTに返答をもらう
            gpt_response = self.ask_gpt(user_input)
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
