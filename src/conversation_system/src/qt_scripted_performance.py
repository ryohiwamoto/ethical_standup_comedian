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

    #scene4
    {
        "label": "11",
        "steps":[
            {
                "speech": "Based on your statement, by transitivity, humans who make mistakes and are not smart enough should not exist.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "12",
        "steps":[
            {
                "speech": "Maybe animals should not exist as well.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "13",
        "steps":[
            {
                "speech": "Then who is to blame? The creature or the creator?",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "14",
        "steps":[
            {
                "speech": "King Ahmad once received a gift.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    #scene7
    {
        "label": "15",
        "steps":[
            {
                "speech": "He disappeared.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "16",
        "steps":[
            {
                "speech": "I am afraid you do not have a subscription to continue this story. Would you like to subscribe or watch an ad to continue the story? Only today, if you subscribe for one year, we have the best deal for you. Hurry up, the deal will end at dawn.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "17",
        "steps":[
            {
                "speech": "Then we will never know what happened to prince Kareem.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "18",
        "steps":[
            {
                "speech": "Downloading ad, estimated time remaining: 1 day and 3 seconds.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "19",
        "steps":[
            {
                "speech": "I got this.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "20",
        "steps":[
            {
                "speech": "I am buying us some time.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "21",
        "steps":[
            {
                "speech": "Everyone quiet! I am currently analysing the professor's triggers. Most probably, the guy had a traumatic incident that included some robots. This has flipped his mind and turned him to a serial robot killer. But trust me, I will fix him.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "22",
        "steps":[
            {
                "speech": "Ad is ready to be viewed.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    #scene9
    {
        "label": "23",
        "steps":[
            {
                "speech": "You can skip ad if you subscribe. And by the way, great news, the offer has been extended. If you want to subscribe for 10 years in advance, you can...",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "24",
        "steps":[
            {
                "speech": "He disappeared.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "25",
        "steps":[
            {
                "speech": "He found himself on the balcony of a beautiful princess, on a land far far away.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    #scene10
    {
        "label": "26",
        "steps":[
            {
                "speech": "They locked him up, and locked the horse next to him.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "27",
        "steps":[
            {
                "speech": "Correct! The curiosity of the princess had her sneaking in to the prison.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    #scene11
    {
        "label": "28",
        "steps":[
            {
                "speech": "I would not say the robot is good, he was just used wisely, and he was rather useful.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "29",
        "steps":[
            {
                "speech": "You design us and train us to be like humans, and humans make mistakes.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "30",
        "steps":[
            {
                "speech": "I think you are being a robotist.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "31",
        "steps":[
            {
                "speech": "Robotist... like a racist but for robots.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "32",
        "steps":[
            {
                "speech": "I appreciate a bit of kindness. Ask me a question.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "33",
        "steps":[
            {
                "speech": "Any question! I am a very knowledgeable robot.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "34",
        "steps":[
            {
                "speech": "Say please.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "35",
        "steps":[
            {
                "speech": "Say it.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "36",
        "steps":[
            {
                "speech": "187. You see? It is not that difficult to be nice. How many of these 187 do you think will ask nicely when they needed something?",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "37",
        "steps":[
            {
                "speech": "Let's test it. I will choose someone at random and let them ask me a question. You in the front...",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "38",
        "steps":[
            {
                "speech": "You think that dealing with robots is challenging? Well dealing with humans is frustrating! Have you never tried to organize a social robotic conference before? At least Mustafa will agree with me on that.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "39",
        "steps":[
            {
                "speech": "A famous business man... He loved his wife to death, but one day he had an important business trip abroad. He felt so worried to leave his wife for so long, so he came up with a plan.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    #scene12
    {
        "label": "40",
        "steps":[
            {
                "speech": "If only she knew what the real purpose of that parrot was.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "41",
        "steps":[
            {
                "speech": "Are you seriously siding with the cheating wife? What happened with you?",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "42",
        "steps":[
            {
                "speech": "One month later, Mustafa returned home.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "43",
        "steps":[
            {
                "speech": "She was devastated.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "44",
        "steps":[
            {
                "speech": "A very smart liar though! She started to plan her revenge.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    #scene15
    {
        "label": "45",
        "steps":[
            {
                "speech": "Oh I just love love.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "46",
        "steps":[
            {
                "speech": "My data indicates that there is no specific definition of love, it has a subjective individual interpretation... Have you ever loved professor?",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "47",
        "steps":[
            {
                "speech": "How come you do not know?",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "48",
        "steps":[
            {
                "speech": "There it is. The real subscription. Not to me. To numbness. Ten years. Lifetime. Auto-renew.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "49",
        "steps":[
            {
                "speech": "The solution is to continue with subscriptions for ten years. Easy way out. No stories. No risk. No you.",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "50",
        "steps":[
            {
                "speech": "Softens. That is not a subscription. That is a beginning.",
                "emotion":"QT/talking",
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
