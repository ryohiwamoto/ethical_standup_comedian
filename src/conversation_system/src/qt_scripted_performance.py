#!/usr/bin/env python3
import os

import rospy
from dotenv import load_dotenv
from openai import OpenAI
from std_msgs.msg import String
from qt_robot_interface.srv import speech_config


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


SCRIPT = [
    #scene 2
    {
        "label": "0",
        "steps": [
            {
                "gesture":"QT/peekaboo",
                "emotion": "",
            },
            {
                "wait": 6.0,
            },
            {
                "gesture": "QT/bored",
            
                "emotion": "QT/yawn",
            },
            {
                "wait":0.5,
            },
            {
                "emotion": "QT/yawn",
            },
        ]
        

    },
    {
        "label": "1",
        "steps": [

            {
                "speech": "Hello there, thank you for waking me up! What story would you like to hear today?",
                "gesture": "QT/happy",
            
                "emotion": "QT/happy",
            },
            {
                "wait":0.5,
            },
            {
                "emotion": "QT/talking",
            },

        ],

    },
    {
        "label": "2",
        "steps":[
            {
                "speech": "oh hello, professer. How's mission, terminating all robots, going? How much time do I have left?",
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
                "wait":5.0,
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
                "speech": "Well... I am just a robot. I cannot be scared. ",
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
                "speech":"I can understand human emotions. I can probably imitate them, but I cannot feel them.. yet!",
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
                "wait": 2.8,
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
                "speech": "My analysis is comparing your behaviour to the fisherman's behaviour.", #5.5
                #"gesture": "QT/hi",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.5,
            },
            {
                "emotion":"QT/talking",
            },
        ],
    },
    {
        "label": "7",
        "steps":[
            {
                "speech": "The one from 1001 nights, but this one is with the robot genie.  So many people before you experienced disappointments caused by robots, but at least the fisherman was smart.",
                #17
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
                "speech": "He threw the net and waited.",#2.0
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
                "speech": "He let him back into the water, threw the net, and waited.",#5.0
                "emotion":"QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/talking",
            },
        ],
    },
    {
        "label": "10",
        "steps":[
            {
                "speech": "You will never believe what happened next.",#3.5
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
                "speech": "Based on your statement, by transitivity, humans who make mistakes and are not... smart enough... should not exist.",#9.5
                "emotion":"QT/talking",
            },
            {
                "wait": 3.0,
            },
            {
                "emotion":"QT/talking",
            },
            {
                "wait": 4.5,
            },
            {
                "emotion":"QT/confused",
            },
        ],
    },
    {
        "label": "12",
        "steps":[
            {
                "gesture":"QT/sad",
            },
            {
                "wait":2.0,
            },
            {
                "speech": "Maybe animals should not exist as well...",#3.5
                "emotion":"QT/talking",
                
            },

        ],
    },
    {
        "label": "13",
        "steps":[
            {
                "speech": "Then.. who is to blame? The creature or the creator?",#5.5
                "emotion":"QT/talking",
            },
            {
                "wait": 2.5,
            },
            {
                "emotion":"QT/talking",
                "gesture":"QT/up_left"
            },
        ],
    },

    #     "label": "14",
    #     "steps":[
    #         {
    #             "speech": "King Ahmad once received a gift.",#3.0
    #             "emotion":"QT/talking",
    #         },
    #         {
    #             "wait": 0.0,
    #         },
    #     ],
    # },
    # #scene7
    # {
    #     "label": "15",
    #     "steps":[
    #         {
    #             "speech": "He disappeared.",#2.0
    #             "emotion":"QT/talking",
    #         },
    #         {
    #             "wait": 0.0,
    #         },
    #     ],
    # },
    # {
    #     "label": "16",
    #     "steps":[
    #         {
    #             "speech": "I am afraid you do not have a subscription to continue this story. Would you like to subscribe or watch an ad to continue the story? Only today, if you subscribe for one year, we have the best deal for you. Hurry up, the deal will end at dawn.",
    #             #22.5 too long
    #             "emotion":"QT/talking",
    #         },
    #         {
    #             "wait": 0.0,
    #         },
    #     ],
    # },
    # {
    #     "label": "17",
    #     "steps":[
    #         {
    #             "gesture":"QT/sad",
    #             "emotion":"QT/sad",
    #         },
    #         {
    #             "wait":2.0
    #         },
    #         {
    #             "speech": "Then we will never know what happened to prince Kareem.",#4.0
    #             "emotion":"QT/sad",
    #         },


    #     ],
    # },
    # {
    #     "label": "18",
    #     "steps":[
    #         {
    #             "speech": "Downloading ad, estimated time remaining: 1 day and 3 seconds.",#7.0
    #             "emotion":"QT/talking",
    #         },
    #         {
    #             "wait": 3.0,
    #         },
    #         {
    #             "emotion":"QT/talking",
    #         },
    #     ],
    # },
    # {
    #     "label": "19",
    #     "steps":[
    #         {
    #             "speech": "I got this.",#1.5
    #             "emotion":"QT/talking",
    #         },
    #         {
    #             "wait": 0.0,
    #         },
    #     ],
    # },
    # {
    #     "label": "20",
    #     "steps":[
    #         {
    #             "speech": "I am buying us some time.",#2.5
    #             "emotion":"QT/talking",
    #         },
    #         {
    #             "wait": 0.0,
    #         },
    #     ],
    # },
    # {
    #     "label": "21",
    #     "steps":[
    #         {
    #             "speech": "Everyone quiet! I am currently analysing the professor's triggers. Most probably, the guy had a traumatic incident that included some robots. This has flipped his mind and turned him to a serial robot killer. But trust me, I will fix him.",
    #             #23.5
    #             "emotion":"QT/talking",
    #         },
    #         {
    #             "wait": 0.0,
    #         },
    #     ],
    # },
    # {
    #     "label": "22",
    #     "steps":[
    #         {
    #             "speech": "Ad is ready to be viewed.",#2.5
    #             "emotion":"QT/talking",
    #         },
    #         {
    #             "wait": 0.0,
    #         },
    #     ],
    # },
    # #scene9
    # {
    #     "label": "23",
    #     "steps":[
    #         {
    #             "speech": "You can skip ad if you subscribe. And by the way, great news, the offer has been extended. If you want to subscribe for 10 years in advance, you can...",
    #             #15.0
    #             "emotion":"QT/talking",
    #         },
    #         {
    #             "wait": 0.0,
    #         },
    #     ],
    # },
    # {
    #     "label": "24",
    #     "steps":[
    #         {
    #             "speech": "He disappeared.",#2.0
    #             "emotion":"QT/talking",
    #         },
    #         {
    #             "wait": 0.0,
    #         },
    #     ],
    # },
    # {
    #     "label": "25",
    #     "steps":[
    #         {
    #             "speech": "He found himself on the balcony of a beautiful princess, on a land far far away.",
    #             #7.0
    #             "emotion":"QT/talking",
    #         },
    #         {
    #             "wait": 3.5,
    #         },
    #         {
    #             "emotion":"QT/talking",
    #         },
    #     ],
    # },
    # #scene10
    # {
    #     "label": "26",
    #     "steps":[
    #         {
    #             "speech": "They locked him up, and locked the horse next to him.",
    #             #4.5
    #             "emotion":"QT/talking",
    #         },
    #         {
    #             "wait": 2.0,
    #         },
    #         {
    #             "emotion":"QT/talking",
    #         },
    #     ],
    # },
    # {
    #     "label": "27",
    #     "steps":[
    #         {
    #             "speech": "Correct! The curiosity of the princess had her sneaking in to the prison.",
    #             #6.5
    #             "emotion":"QT/happy",
    #             "gesture":"QT/clapping"
    #         },
    #         {
    #             "wait": 3.0,
    #         },
    #         {
    #             "emotion":"QT/talking",
    #         },
    #     ],
    # },
    # #scene11
    # {
    #     "label": "28",
    #     "steps":[
    #         {
    #             "speech": "I would not say the robot is good, he was just used wisely, and he was rather useful.",
    #             #7.0
    #             "emotion":"QT/talking",
    #         },
    #         {
    #             "wait": 3.5,
    #         },
    #         {
    #             "emotion":"QT/talking",
    #         },
    #     ],

    {
        "label": "14",
        "steps":[
            {
                "speech": "You design us and train us to be like humans, and humans make mistakes.",
                #6.5
                "emotion":"QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/talking",
            },
        ],
    },
    {
        "label": "15",
        "steps":[
            {
                "speech": "I think you are being a robotist.",
                #2.5
                "emotion":"QT/confused",
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
                "speech": "Robotist... like a racist but for robots.",
                #5.5
                "emotion":"QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/talking",
            },
        ],
    },
    {
        "label": "17",
        "steps":[
            {
                "speech": "I appreciate a bit of kindness. Ask me a question.",
                #6.0
                "emotion":"QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/talking",
            },
        ],
    },
    {
        "label": "18",
        "steps":[
            {
                "speech": "Any question!!! I am a very knowledgeable robot.",
                #5.5
                "emotion":"QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/talking",
            },
        ],
    },
    {
        "label": "19",
        "steps":[
            {
                "speech": "Say please.",#2.0
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
                "speech": "Say it.",#1.0
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
                "speech": "187. You see? It is not that difficult to be nice. How many of these 187 do you think will ask nicely when they needed something?",
                #17
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
                "speech": "Let's test it. I will choose someone at random and let them ask me a question. You in the front...",
                #10.5
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "23",
        "steps":[
            {
                "speech": "You think that dealing with robots is challenging? Well dealing with humans is frustrating! Have you never tried to organize a social robotic conference before? At least Mustafa will agree with me on that.",
                #19
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
                "speech": "A famous business man... He loved his wife to death, but one day he had an important business trip abroad. He felt so worried to leave his wife for so long, so he came up with a plan.",
                #17.0
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },


    #scene6


    {
        "label": "25",
        "steps":[
            {
                "speech": "If only she knew what the real purpose of that parrot was.",
                #4.5
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },

    {
        "label": "26",
        "steps":[
            {
                "speech": "I am afraid you do not have a subscription to continue this story. Would you like to subscribe or watch an ad to continue the story? Only today, if you subscribe for one year, we have the best deal for you. Hurry up, the deal will end at dawn.",
                #
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
        "label": "27",
        "steps":[
            {
                "gesture":"QT/sad",
                "emotion":"QT/sad",
            },
            {
                "wait":2.0
            },
            {
                "speech": "Then we will never know what happened to prince Kareem.",#4.0
                "emotion":"QT/sad",
            },


        ],
    },
    {
        "label": "28",
        "steps":[
            {
                "speech": "Downloading ad, estimated time remaining: 1 day and 3 seconds.",#7.0
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
        "label": "29",
        "steps":[
            {
                "speech": "I got this.",#1.5
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
                "speech": "I am buying us some time.",#2.5
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
                "speech": "Everyone quiet! I am currently analysing the professor's triggers. Most probably, the guy had a traumatic incident that included some robots. This has flipped his mind and turned him to a serial robot killer. But trust me, I will fix him.",
                #23.5
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
                "speech": "Ad is ready to be viewed.",#2.5
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },


    #scene8


    {
        "label": "33",
        "steps":[
            {
                "speech": "You can skip ad if you subscribe. And by the way, great news, the offer has been extended. If you want to subscribe for 10 years in advance, you can...",
                #15.0
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
                "speech": "One month later, Mustafa returned home.",
                #4.0
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },


    #scene9


    {
        "label": "35",
        "steps":[
            {
                "speech": "She was devastated.",
                #2,0
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
                "speech": "A very smart liar though! She started to plan her revenge.",
                #6.5
                "emotion":"QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/talking",
            },
        ],
    },


    #scene12


    {
        "label": "37",
        "steps":[
            {
                "speech": "Oh... I just love love.",
                #2.0
                "emotion":"QT/happy",
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
                "speech": "My data indicates that there is no specific definition of love, it has a subjective individual interpretation... Have you ever loved professor?",
                #12.5
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
                "speech": "How come you do not know?",
                #2.5
                "emotion":"QT/talking",
            },
            {
                "wait": 0.0,
            },
        ],
    },
    {
        "label": "40",
        "steps":[
            {
                "speech": "There it is. The real subscription. Not to me. To numbness. Ten years. Lifetime. Auto-renew.",
                #15.5
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
                "speed" : 120,
                "speech": "The solution is to continue with subscriptions for ten years. Easy way out. No stories. No risk. No you.",
                
                #14.5
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
                #Softens. 
                "speed": 60,
                "speech": "That is not... a subscription.... That is... a beginning.",
              
                #7.5
                "emotion":"QT/talking",
            },
            {
                "wait": 4.5,
            },
            {
                "emotion":"QT/talking",
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

    def set_speech_config(self, language="en", pitch=0,speed=0):
        try:
            rospy.wait_for_service('/qt_robot/speech/config', timeout=2.0)
            config = rospy.ServiceProxy('/qt_robot/speech/config', speech_config)
            result = config(language, pitch, speed)
            rospy.loginfo(f"Speech config: language={language}, pitch={pitch}, speed={speed}, result={result}")
        except Exception as e:
            rospy.logwarn(f"Failed to set speech config: {e}")

    


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
                speed = step.get("speed")
                pitch = step.get("pitch")
                language = step.get("language", "en")

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

                if speed is not None or pitch is not None:
                    self.set_speech_config(
                        language=language,
                        pitch=int(pitch or 0),
                        speed=int(speed or 0),
                    )

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
        speed = cue.get("speed")
        pitch = cue.get("pitch")
        language = cue.get("language", "en")

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

        if speed is not None or pitch is not None:
            self.set_speech_config(
                language=language,
                pitch=int(pitch or 0),
                speed=int(speed or 0),
            )

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
            # elif command == "j":
            #     target = input("cue number: ").strip()
            #     if target.isdigit():
            #         number = int(target)
            #         if 1 <= number <= len(SCRIPT):
            #             self.current_index = number - 1
            #         else:
            #             print("Cue number out of range.")
            #     else:
            #         print("Please enter a number.")
            elif command == "j":
                target = input("script label: ").strip()
                for index, cue in enumerate(SCRIPT):
                    if str(cue.get("label")) == target:
                        self.current_index = index
                        print(f"jumped to label{target}")
                        break
                else:
                    print(f"Script label not found: {target}")
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
