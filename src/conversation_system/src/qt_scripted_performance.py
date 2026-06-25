#!/usr/bin/env python3
import os

import rospy
from dotenv import load_dotenv
from openai import OpenAI
from std_msgs.msg import String


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


SCRIPT = [
    #scene 2
    {
        "label": "1",
        "steps": [
            {
                "gesture":"QT/peekaboo",
                "emotion": "",
            },

            {
                "wait": 7.0,
            },
            {
                "speech": "Hello there, thank you for waking me up! ",
                "gesture": "QT/bored",
            
                "emotion": "QT/yawn",
            },
            {
                "wait":0.5,
            },
            {
                "emotion": "QT/yawn",
            },

            {
                "wait": 11.0,
            },
            {
                "gesture": "QT/happy",
            },
            {
                "wait": 1.0,
            },
            {
                "speech": "What story would you like to hear today?",
                "emotion": "QT/talking",
            },


        ],

    },
    {
        "label": "2",
        "steps":[
            {
                "speech": "oh hello, professer. How's mission terminating all robots going? How much time do I have left?",
                "gesture": "QT/up_left",
                "emotion": "QT/talking",
            },
            {
                "wait":0.5,
            },
            {
                "emotion": "QT/talking",
            },
            {
                "wait":3.5,
            },
            {
                "emotion": "QT/talking",
            },
            {
                "wait":5.5,
            },
            {
                "emotion": "QT/talking",
            },
        ],

    },
    {
        "label": "3",
        "steps": [
            {
                "speech": "Unfortunately, I am just a robot. I cannot be scared. ",
                "gesture": "QT/clapping",
                "emotion": "QT/shy",
            },
            {
                "wait":2.0,
            },
            {
                "emotion": "QT/shy",
            },

            {
                "wait": 7.5,
            },
            {
                "speech":"I can understand human emotions. I can probably imitate them, but I cannot feel them yet!",
                "emotion": "QT/talking",
            },
            {
               "wait": 2.0,
            },
            {
                "emotion": "QT/talking",
            },          
                        {
               "wait": 2.0,
            },
            {
                "emotion": "QT/talking",
            },     
            {
               "wait": 4.5,
            },
            {
                "speech": "Hahaha",
                "emotion": "QT/blowing_raspberry",
            },

        ],

        
    },
 
    {
        "label": "4",
        "steps": [
            {
                "speech": "you are being sarcastic!",
                "emotion": "QT/talking",
            },

            {
                "wait": 3.0,
            },
            {
                "emotion": "QT/happy",
            },
            {
                "wait": 1.5,
            },
            {
                "speech": "Hahaha",
            },
            {
                "wait": 3.0,
            },
            {
                "speech": "I can be funny as well.",
                "emotion": "QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "api_prompt": "Make one short robot stand-up joke about humans.",
            },
            {
                "wait": 1.0,
            },
            {
                "emotion":"QT/talking",
            },
            {
                "wait": 3.0,
            },
            {
                "emotion":"QT/talking",
            },
        ],
    },
    {
        "label": "5",
        "steps":[
            {
                "speech": "Why are you scared Professor?",
                "gesture": "QT/angry",
                "emotion": "QT/confused",
            },
        ],
    },
        {
        "label": "6",
        "steps":[
            {
                "speech": "My analysis is comparing your behaviour to the fisherman's behaviour.",
                #"gesture": "QT/hi",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,

            },
        ],
    },
    {
        "label": "7",
        "steps":[
            {
                "speech": "The one from 1001 nights, but this one is with the robot genie.  So many people before you experienced disappointments caused by robots, but at least the fisherman was smart.",
                #"gesture": "QT/hi",
                "emotion":"QT/talking",

            },
            {
                "wait": 0.0,

            },
        ],
    },

    #scene3
    {
        "label": "8",
        "steps":[
            {
                "speech": "He threw the net and waited.",
                "emotion":"QT/talking",

            },
            {
                "wait": 0.0,

            },
        ],
    },
    {
        "label": "9",
        "steps":[
            {
                "speech": "He let him back into the water, threw the net, and waited.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,

            },
        ],
    },
    {
        "label": "10",
        "steps":[
            {
                "speech": "You will never believe what happened next.",
                "emotion":"QT/talking",

            },
            {
                "wait": 0.0,

            },
        ],
    },


        {
        "label": "",
        "steps":[
            {

            },
            {
                "wait": 0.0,

            },
        ],
    },
]


class QTScriptedPerformance:
    def __init__(self):
        rospy.init_node("qt_scripted_performance")

        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.current_index = 0
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
        self.emotion_pub = rospy.Publisher(
            "/qt_robot/emotion/show",
            String,
            queue_size=10,
        )

        rospy.sleep(1.0)
        rospy.loginfo("QT scripted performance node started.")

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

    def show_emotion(self, emotion_name):
        rospy.loginfo(f"Emotion: {emotion_name}")
        self.publish_text(self.emotion_pub, emotion_name)

    def ask_gpt(self, prompt):
        system_prompt = (
            "Your name is QT robot. "
            "You are a friendly social robot performer. "
            "Keep the response short, clear, and suitable to speak aloud."
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            rospy.logerr(f"OpenAI API error: {e}")
            return "Sorry, my improvisation module failed."

    def execute_cue(self, cue):
        label = cue.get("label", "untitled")
        print(f"\n[{self.current_index + 1}/{len(SCRIPT)}] {label}")

        steps = cue.get("steps")
        if steps:
            for step in steps:
                emotion = step.get("emotion")
                gesture = step.get("gesture")
                speech = step.get("speech")
                api_prompt = step.get("api_prompt")
                wait_time = float(step.get("wait",0.0))

                if emotion:
                    self.show_emotion(emotion)
                if gesture:
                    self.play_gesture(gesture)

                if api_prompt:
                    print(f"api_prompt:{api_prompt}")
                    speech = self.ask_gpt(api_prompt)
                    print(f"QT(API): {speech}")
                elif speech:
                    print(f"QT: {speech}")

                if speech:
                    self.say(speech)

                if wait_time > 0:
                    print(f"waiting{wait_time:.1f}seconds")
                    rospy.sleep(wait_time)

            return



        

        emotion = cue.get("emotion")
        gesture = cue.get("gesture")
        speech = cue.get("speech")
        #     return
        api_prompt = cue.get("api_prompt")
        wait_time = float(cue.get("wait", 0.0))

        if emotion:
            self.show_emotion(emotion)
        if gesture:
            self.play_gesture(gesture)

        if api_prompt:
            print(f"api_prompt: {api_prompt}")
            speech = self.ask_gpt(api_prompt)
            print(f"QT(API): {speech}")
        elif speech:
            print(f"QT: {speech}")

        if speech:
            self.say(speech)

        if wait_time > 0:
            print(f"waiting {wait_time:.1f} seconds")
            rospy.sleep(wait_time)

    def print_help(self):
        print("--- QT Scripted Performance ---")
        print("Enter : run current cue and move next")
        print("r     : replay current cue")
        print("s     : skip current cue")
        print("b     : go back one cue")
        print("j     : jump to cue number")
        print("q     : quit")
        print("--------------------------------")

    def run(self):
        self.print_help()

        while not rospy.is_shutdown():
            if self.current_index >= len(SCRIPT):
                print("End of script. Type b to go back or q to quit.")
                command = input("command: ").strip().lower()
            else:
                cue = SCRIPT[self.current_index]
                label = cue.get("label", "untitled")
                command = input(
                    f"cue {self.current_index + 1}/{len(SCRIPT)} "
                    f"({label}) command: "
                ).strip().lower()

            if command == "q":
                print("bye")
                break
            if command == "h":
                self.print_help()
            elif command == "r":
                if self.current_index < len(SCRIPT):
                    self.execute_cue(SCRIPT[self.current_index])
            elif command == "s":
                self.current_index = min(self.current_index + 1, len(SCRIPT))
                print(f"skipped to cue {self.current_index + 1}")
            elif command == "b":
                self.current_index = max(0, self.current_index - 1)
                print(f"back to cue {self.current_index + 1}")
            elif command == "j":
                target = input("cue number: ").strip()
                if target.isdigit():
                    number = int(target)
                    if 1 <= number <= len(SCRIPT):
                        self.current_index = number - 1
                    else:
                        print("Cue number out of range.")
                else:
                    print("Please enter a number.")
            elif command == "":
                if self.current_index < len(SCRIPT):
                    self.execute_cue(SCRIPT[self.current_index])
                    self.current_index += 1
            else:
                print("Unknown command. Press h for help.")


if __name__ == "__main__":
    try:
        node = QTScriptedPerformance()
        node.run()
    except rospy.ROSInterruptException:
        pass
