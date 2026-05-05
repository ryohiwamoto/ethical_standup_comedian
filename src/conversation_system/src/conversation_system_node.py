#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

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

        self.play_gesture("QT/thinking")

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
        print("QTrobot chat mode (Ctrl+C to terminate)")
        print("---------------------------------------")
        
        while not rospy.is_shutdown():
            # キーボードから入力を受け取る
            user_input = input("you: ")
            
            if not user_input:
                continue

            # GPTに返答をもらう
            gpt_response = self.ask_gpt(user_input)
            print(f"answer: {gpt_response}")

            self.play_gesture("QT/talk")

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
        
