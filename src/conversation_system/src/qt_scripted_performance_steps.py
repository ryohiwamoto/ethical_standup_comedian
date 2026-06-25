#!/usr/bin/env python3
import os

import rospy
from dotenv import load_dotenv
from openai import OpenAI
from std_msgs.msg import String


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


SCRIPT = [
    {
        "label": "opening",
        "speech": "Hello. I am QT robot.",
        "gesture": "QT/hi",
        "emotion": "QT/happy",
    },
    {
        "label": "line_then_generated_joke",
        "steps": [
            {
                "speech": "Let me try a joke.",
                "gesture": "QT/hi",
            },
            {
                "wait": 2.0,
            },
            {
                "gesture": "QT/clapping",
            },
            {
                "wait": 1.0,
            },
            {
                "api_prompt": "Make one short robot stand-up joke about humans.",
            },
        ],
    },
    {
        "label": "shy_pause",
        "steps": [
            {
                "gesture": "QT/sad",
                "emotion": "QT/shy",
            },
            {
                "wait": 3.0,
            },
            {
                "speech": "That pause was not a bug. It was theatre.",
            },
        ],
    },
    {
        "label": "ending",
        "speech": "Thank you. My comedy module will now pretend that went well.",
        "gesture": "QT/clapping",
    },
]


class QTScriptedPerformanceSteps:
    def __init__(self):
        rospy.init_node("qt_scripted_performance_steps")

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
        rospy.loginfo("QT scripted performance steps node started.")

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

    def run_step(self, step):
        emotion = step.get("emotion")
        gesture = step.get("gesture")
        speech = step.get("speech")
        api_prompt = step.get("api_prompt")
        wait_time = float(step.get("wait", 0.0))

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

    def execute_cue(self, cue):
        label = cue.get("label", "untitled")
        print(f"\n[{self.current_index + 1}/{len(SCRIPT)}] {label}")

        steps = cue.get("steps")
        if steps:
            for step in steps:
                self.run_step(step)
            return

        self.run_step(cue)

    def print_help(self):
        print("--- QT Scripted Performance Steps ---")
        print("Enter : run current cue and move next")
        print("r     : replay current cue")
        print("s     : skip current cue")
        print("b     : go back one cue")
        print("j     : jump to cue number")
        print("q     : quit")
        print("--------------------------------------")

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
        node = QTScriptedPerformanceSteps()
        node.run()
    except rospy.ROSInterruptException:
        pass
