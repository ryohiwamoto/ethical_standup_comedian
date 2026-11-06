#!/usr/bin/env python3
import rospy
from std_msgs.msg import String


class QTManualGestureTest:
    def __init__(self):
        rospy.init_node("qt_manual_gesture_test")
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
        rospy.sleep(1.0)
        rospy.loginfo("QT manual gesture test started.")

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

    def play_clap_then_hi(self):
        self.play_gesture("QT/clapping")
        rospy.sleep(3.0)
        self.play_gesture("QT/hi")

    def run(self):
        print("--- QT Manual Gesture Test ---")
        print("Enter : play QT/clapping, then QT/hi")
        print("c     : play QT/clapping")
        print("h     : play QT/hi")
        print("s     : type text and make QT speak")
        print("q     : quit")
        print("--------------------------------")

        while not rospy.is_shutdown():
            command = input("command: ").strip().lower()

            if command == "q":
                print("bye")
                break
            if command == "":
                self.play_clap_then_hi()
            elif command == "c":
                self.play_gesture("QT/clapping")
            elif command == "h":
                self.play_gesture("QT/hi")
            elif command == "s":
                text = input("speech text: ").strip()
                if text:
                    self.say(text)
            else:
                print("Unknown command. Use Enter, c, h, s, or q.")


if __name__ == "__main__":
    try:
        node = QTManualGestureTest()
        node.run()
    except rospy.ROSInterruptException:
        pass
