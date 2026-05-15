#!/usr/bin/env python3
import sys

import cv2
import mediapipe as mp


CAMERA_INDEX = int(sys.argv[1]) if len(sys.argv) > 1 else 1


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


def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print(f"Could not open camera index {CAMERA_INDEX}")
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
        while True:
            ok, frame = cap.read()
            if not ok:
                print("No frame")
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            face_count = 0
            smile_score = 0.0

            if results.multi_face_landmarks:
                face_count = len(results.multi_face_landmarks)
                landmarks = results.multi_face_landmarks[0].landmark
                smile_score = compute_smile_score(landmarks)

                height, width = frame.shape[:2]
                for index in [61, 291, 13, 14, 33, 263]:
                    point = landmarks[index]
                    x = int(point.x * width)
                    y = int(point.y * height)
                    cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            label = f"faces: {face_count} smile: {smile_score:.2f}"
            print(label)
            cv2.putText(
                frame,
                label,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                2,
            )

            cv2.imshow("smile test", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
