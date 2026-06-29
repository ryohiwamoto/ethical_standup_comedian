    #     ---Sample below---

    #{ <--- pink braces is a script.
    #     "label": "42", <--- label number
    #     "steps":[  <--- if u use *"steps"[]:*, u can add emotions n gestures n wait. and u can also separete a script without entering the key. 
    #         {
    #             "speed": 90,  <--- speed of speech. 
    #             "pitch" : 85,  <--- pitch of speech. if u make it higher, the voice tone go high
    #             "speech": "hello",           
    #             "emotion":"QT/talking",
    #             "gesture":"QT/hi"
    #         },
    #         {
    #             "wait": 4.5,
    #         },
    #         {
    #             "speed": 70,  <--- u can change the speed n pitch in a same script.  for ex, "hello" would be in speed90, pitch85. but "world" would be in speed70, pitch50. if they are in a same script(pink braces), they gonna get changed automaticaly without entering the Key.
    #             "pitch" : 50,  
    #             "speech": "world",
    #             "emotion":"QT/talking",
    #         },
    #     ],
    # },


#!/usr/bin/env python3
import os
import tempfile
import wave

import rospy
from audio_common_msgs.msg import AudioData
from dotenv import load_dotenv
from openai import OpenAI
from std_msgs.msg import String
from qt_robot_interface.srv import speech_config


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RECORD_SECONDS = int(os.getenv("RECORD_SECONDS", "5"))
IGNORED_TRANSCRIPTS = {"you", "thank you", "thanks"}

CHANNELS = 1
RATE = 16000
AUDIO_WIDTH = 2


SCRIPT = [
    #scene 2
    {
        "label": "01",
        "steps": [
            {
                "gesture":"QT/peekaboo",
                "emotion": "",
            },

        ],       

    },
        {
        "label": "02",
        "steps": [

            {
                "speed":50,
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
                "pitch": 90,
                "speed": 95,
                "speech": "Hello there, thank you for waking me up! What story would you like to hear today?",
                "gesture": "QT/happy",
            
                "emotion": "QT/talking",
            },
            {
                "wait":0.5,
            },
            {                
                "emotion": "QT/happy",
            },

        ],

    },
    {
        "label": "2",
        "steps":[
            {
                "pitch": 90,
                "speed": 95,
                "speech": "oh hello professer. How's mission terminating all robots going? How much time do I have left?",
                "gesture": "QT/hi",
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
                "emotion": "QT/confused",
            },
        ],

    },
    {
        "label": "3",
        "steps": [
            {
                "pitch": 90,
                "speed": 110,
                "speech": "Unfortunately, I am just a robot, I cannot be scared, I can understand human emotions, I can probably imitate them, but I cannot feel them.. yet! ",
                "emotion": "QT/talking",
                "gesture": "QT/swipe_left",
            },
            {
               "wait": 2.0,
            },
            {
               
                "emotion": "QT/talking",
            },    
            {
                "wait":2,
            },
            {
                "emotion": "QT/talking",
            },    
            {
                "wait":2,
            },
            {
                "gesture": "QT/clapping",
                "emotion": "QT/shy",
            },

            {
               "wait": 4,
            },
            {
                "pitch": 110,
                "speed": 70,
                "speech": "Hahaha",
                "emotion": "QT/blowing_raspberry",
            },

        ],

        
    },
 
    {
        "label": "4",
        "steps": [
            {
                "pitch": 110,
                "speed": 95,
                "speech": "ha, ha, ha, ha, you are being sarcastic!",
                "emotion": "QT/happy",
            },

            {
                "wait": 2,
            },
            {
                "pitch": 90,
                "speech": "I can be funny as well.",
                "emotion": "QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "api_prompt": "Make one short robot stand-up joke about humans.",
                "gesture": "QT/Show-face",
            },
            {
                "wait": 1,
            },

            {
                "emotion":"QT/talking",
            },
            {
                "wait": 3,
            },
            {
                "emotion":"QT/puffing_the_chredo_eeks",
            },
        ],
    },
    {
        "label": "5",
        "steps":[
            {
                "pitch": 100,
                "speed": 100,
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
                "pitch": 100,
                "speed": 95,
                "speech": "My analysis is comparing your behaviour to the fisherman's behaviour.", #5.5
                #"gesture": "QT/hi",
                "emotion":"QT/talking",
            },
            {
                "wait": 0.5,
            },
            {
                "emotion":"QT/showing_smile",
            },
        ],
    },
    {
        "label": "7",
        "steps":[
            {
                "pitch": 100,
                "speed": 110,
                "speech": "The one from 1001 nights, but this one is with the robot genie.  So many people before you experienced disappointments caused by robots, but at least the fisherman was smart.",
                #17
                #"gesture": "QT/hi",
                "emotion":"QT/afraid",

            },
            {
                "wait": 2.5,

            },
            {
                "gesture":"QT/point_front",
                "emotion":"QT/talking",

            },
            {
                "wait": 2.5,

            },
            {
                "emotion":"QT/talking",
            },
            {
                "wait": 2.5,

            },
            {
                "emotion":"QT/brushing_teeth",
            }
        ],
    },

    #scene3


    {
        "label": "8",
        "steps":[
            {
                "pitch": 85,
                "speed": 100,
                "speech": "He threw the net, and waited.",#2.0
                "emotion":"QT/talking",

            },
        ],
    },
    {
        "label": "9",
        "steps":[
            {
                "pitch": 85,
                "speed": 100,
                "speech": "He let him back into the water, threw the net, and waited.",#5.0
                "emotion":"QT/talking",
            },
        ],
    },
    {
        "label": "10",
        "steps":[
            {
                "pitch": 95,
                "speed": 100,
                "speech": "You will never believe, what happened next.",#3.5
                "emotion":"QT/talking",
                "gesture":"QT/touch-head-back",

            },

        ],
    },


    #scene4


    {
        "label": "11",
        "steps":[
            {
                "pitch": 100,
                "speed": 100,
                "speech": "Based on your statement, by transitivity, humans who make mistakes, and are not, smart enough, should not exist.",#9.5
                "emotion":"QT/talking",
                "gesture":"QT/monkey",
            },
            {
                "wait": 3.0,
            },
            {
                "emotion":"QT/talking",
            },
            {
                "wait": 3.0,
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
                "emotion":"QT/sad",
            },
            {
                "wait": 1.0,
            },
            {
                "pitch": 100,
                "speed": 100,
                "speech": "Maybe animals should not exist as well?",#3.5
            },

        ],
    },
    {
        "label": "13",
        "steps":[
            {
                "pitch": 95,
                "speed": 110,
                "speech": "Then who is to blame? The creature? or the creator?",#5.5
                "emotion":"QT/talking",
            },
            {
                "wait": 1,
            },
            {
                "emotion":"QT/showing_smile",
                "gesture":"QT/show_tablet"
            },
        ],
    },
    {
        "label": "14",
        "steps":[
            {
                "pitch": 100,
                "speed": 90,
                "speech": "You design us and train us to be like humans, and humans make mistakes.",
                "emotion":"QT/talking",
                #6.5
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/scream",
            },
        ],
    },
    {
        "label": "15",
        "steps":[
            {
                "emotion":"QT/afraid",
            },
            {
                "wait": 1.0,
            },
            {
                "speech": "I guess, you are being a robotist.",
                #2.5
            },
        ],
    },
    {
        "label": "16",
        "steps":[
            {
                "emotion":"QT/disgusted",
            },
            {
                "wait": 1.0,
            },
            {
                "speech": "Robotist, like a racist, but for robots.",
                #5.5
                "gesture":"QT/angry"
            },

        ],
    },
    {
        "label": "17",
        "steps":[
            {
                "emotion":"QT/calming_down",
            },
            {
                "wait": 1.0,
            },
            {
                "pitch": 100,
                "speed": 100,
                "speech": "I appreciate a bit of kindness, Ask me a question.",
                #6.0
            },
        ],
    },
    {
        "label": "18",
        "steps":[
            {
                "pitch": 100,
                "speed": 100,
                "speech": "Any question, I am a very knowledgeable robot.",
                #5.5
                "emotion":"QT/talking",
            },
        ],
    },
    {
        "label": "19",
        "steps":[
            {
                "emotion":"QT/cry",
            },
            {
                "wait": 1.5,
            },
            {
                "pitch": 100,
                "speed": 90,
                "speech": "Can you say, please?",#2.0
            },
        ],
    },
    {
        "label": "20",
        "steps":[
            {
                "emotion":"QT/scream",
            },
            {
                "wait": 1.5,
            },
            {
                "speech": "COME ON SAY it!",#1.0
            },
        ],
    },
    {
        "label": "21",
        "steps":[
            {
                "gesture":"QT/stretching"
            },
            {
                "wait": 2,
            },
            {
                "speed": 100,
                "speech": "187. You see? It is not that difficult to be nice. How many of these 187 do you think will ask nicely, when they needed something?",
                #17
                "emotion":"QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/showing_smile",
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
        "label": "22",
        "steps":[
            {
                "speed": 95,
                "speech": "Let's test it. I will choose someone at random, and let them ask me a question.",
                #10.5
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
        "label": "22.1",
        "steps":[
            {
                "speed": 90,
                "speech": "You, in the front",
                #10.5
                "emotion":"QT/talking",
                "gesture":"QT/point_front"
            },
        ],
    },
    {
        "label": "interaction",
        "interaction": True,
    },
    {
        "label": "23",
        "steps":[
            {
                "speed": 105,
                "speech": "You think that dealing with robots is challenging? Well, dealing with humans is frustrating! Have you ever tried to organize a social robotic conference before? At least Mustafa will agree with me on that.",
                #19
                "emotion":"QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/talking",
            },
            {
                "wait": 2.0,
            },

            {
                "emotion":"QT/with_a_cold_cleaning_nose",
                "gesture":"QT/clapping"
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
        "label": "24",
        "steps":[
            {
                "speech": "A famous business man... He loved his wife to death, but one day he had an important business trip abroad. He felt so worried to leave his wife for so long, so he came up with a plan.",
                #17.0
                "emotion":"QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/kiss",
            },
            {
                "wait": 2.0,
            },
            {
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



    #scene6


    {
        "label": "25",
        "steps":[
            {
                "speech": "If only she knew what the real purpose of that robot was.",
                #4.5
                "emotion":"QT/talking",
            },
        ],
    },

    {
        "label": "26",
        "steps":[
            {
                "speech": "I am afraid you do not have a subscription to continue this story. Would you like to subscribe or watch an ad to continue the story? Only today, if you subscribe for one year, we have the best deal for you. Hurry up, the deal will end at dawn.",
                #
                "emotion":"QT/dirty_face_sad",
                "gesture":"QT/sad"
            },
            {
                "wait": 3.0,
            },
            {
                "emotion":"QT/dirty_face_wash",
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
                "speed": 95,
                "speech": "Then we will never know what the robot does.",#4.0
                "gesture":"QT/Show-face",
                "emotion":"QT/sad",
            },


        ],
    },
    {
        "label": "28",
        "steps":[
            {
                "speech": "Downloading ad, estimated time remaining: 1 day 2 hours and 3 seconds.",#7.0
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
        ],
    },
    {
        "label": "30",
        "steps":[
            {
                "speech": "I am buying us some time.",#2.5
                "emotion":"QT/talking",
            },
            
        ],
    },
    {
        "label": "31",
        "steps":[
            {
                "emotion":"QT/scream",                
            },
            {
                "wait": 1.0,
            },
            {
                "speed": 105,
                "speech": "Everyone QUIET! I am currently analysing the professor's triggers, Most probably he had a traumatic incident that included some robots. This has flipped his mind and turned him to a serial robot killer. But trust me, I will fix him.",
                #23.5
            },
            {
                "wait": 1.0,
            },
            {
                "emotion":"QT/talking",     
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/confused",                
                "gesture":"QT/surprise",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/afraid",             
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/calming_down",                
            },
        ],
    },
    {
        "label": "32",
        "steps":[
            {
                "speech": "Ad is ready to be viewed.",#2.5
                "emotion":"QT/showing_smile",
                "gesture":"QT/show_tablet",
            },
        ],
    },


    #scene8


              
                #7.5
               # "emotion":"QT/talking",
    {
        "label": "33",
        "steps":[
            {
                "speech": "You can skip ad if you subscribe. And by the way, great news, the offer has been extended. If you want to subscribe for 10 years in advance, you can...",
                #15.0
                "emotion":"QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/brushing_teeth_foam",
            },
        ],
    },

    {
        "label": "34",
        "steps":[
            {
                "pitch": 90,
                "speed": 110,
              
                #7.5
                "emotion":"QT/talking",
                "speech": "One month later, Mustafa returned home.",
                #4.0
                "emotion":"QT/talking",
            },
        ],
    },


    #scene9


    {
        "label": "35",
        "steps":[
            {
                "emotion":"QT/sad",
            },
            {
                "wait": 1.0,
            },
            {
                "speech": "She was devastated.",
                #2,0
            },
        ],
    },
    {
        "label": "36",
        "steps":[
            {
                "speech": "A very smart liar though, She started to plan her revenge.",
                #6.5
                "emotion":"QT/talking",
            },
        ],
    },


    #scene12


    {
        "label": "37",
        "steps":[
            {
                "emotion":"QT/shy",
            },
            {
                "wait": 1.0,
            },
            {
                "pitch": 100,
                "speed": 90,
                "speech": "ahhh, I just love love.",
                #2.0
            },
        ],
    },
    {
        "label": "38",
        "steps":[
            {
              
                #7.5
                "emotion":"QT/talking",
                "speech": "My data indicates that there is no specific definition of love, it has a subjective individual interpretation, Have you ever loved professor?",
                #12.5
                "emotion":"QT/talking",
                "gesture":"QT/Show-face",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/confused",
            },
            {
                "wait": 2.0,
            },
              
                #7.5
                #"emotion":"QT/talking",
            {
                "emotion":"QT/talking",
            },
        ],
    },
    {
        "label": "39",
        "steps":[
            {
                "emotion":"QT/afraid",
            },
            {
                "wait": 1.0,
              
                #7.5
                "emotion":"QT/talking",
            },
            {
                "speech": "How come you do not know?",
                #2.5
            },
        ],
    },
    {
        "label": "40",
        "steps":[
            {
                "speed": 105,
                "speech": "There it is, The real subscription. Not to me. To numbness. Ten years. Auto-renew... The solution is to continue with subscriptions for ten years. Easy way out. No stories. No risk. No you.",
                #15.5
                "emotion":"QT/happy",
                "gesture":"QT/bye-bye"
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/sad",
            },
            {
                "wait": 3.5,
            },
            {
                "emotion":"QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/talking",
            },
            {
                "wait": 2.0,
            },
            {
                "emotion":"QT/calming_down",
            },
        ],
    },
    {
        "label": "41",
        "steps":[
            {
                #Softens. 
                "speed": 90,
                "pitch" : 95,
                "speech": "That is not, a subscription... That is, a beginning.",
              
                #7.5
                "emotion":"QT/talking",
                "gesture":"QT/kiss"
            },
            {
                "wait": 3,
            },
            {
                "emotion":"QT/kiss",
            },
        ],
    },
]


class QTScriptedPerformance:
    def __init__(self):
        rospy.init_node("qt_scripted_performance")

        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.current_index = 0
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
        self.emotion_pub = rospy.Publisher(
            "/qt_robot/emotion/show",
            String,
            queue_size=10,
        )
        self.audio_sub = rospy.Subscriber(
            "/qt_respeaker_app/channel0",
            AudioData,
            self.audio_callback,
        )

        rospy.sleep(1.0)
        rospy.loginfo("QT scripted performance node started.")

    def audio_callback(self, msg):
        if self.is_recording:
            self.audio_frames.append(bytes(msg.data))

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
            print(f"Audience: {text}")

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

    def run_interaction(self):
        print("Audience interaction: ask QT a question by voice.")
        self.show_emotion("QT/talking")
        user_input = self.listen_with_whisper()
        if not user_input:
            self.show_emotion("QT/confused")
            self.say("Sorry, I did not catch that.")
            return

        answer = self.ask_gpt(user_input)
        print(f"QT(interaction): {answer}")
        self.show_emotion("QT/talking")
        self.play_gesture("QT/hi")
        self.say(answer)

    def execute_cue(self, cue):
        label = cue.get("label", "untitled")
        print(f"\n[{self.current_index + 1}/{len(SCRIPT)}] {label}")

        if cue.get("interaction"):
            self.run_interaction()
            return

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
                    f"(current label:{label}), command: "
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
