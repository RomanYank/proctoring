import cv2
import math
import mediapipe as mp

class HeadDetectionModel:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh()

    def get_head_orientation(self, landmarks):
        left_eye = landmarks[33]
        right_eye = landmarks[133]

        delta_x = right_eye[0] - left_eye[0]
        delta_y = right_eye[1] - left_eye[1]
        angle = math.atan2(delta_y, delta_x) * 180 / math.pi

        return angle

    def detect_head_orientation(self, frame, annotated_frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)

        orientation = "forward"  # по умолчанию

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = [(lm.x, lm.y) for lm in face_landmarks.landmark]
                angle = self.get_head_orientation(landmarks)

                if angle > 15:
                    orientation = "right"
                elif angle < -15:
                    orientation = "left"
                else:
                    orientation = "forward"

                # визуализация
                cv2.putText(annotated_frame, f"Head: {orientation}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) if orientation != "forward" else (0, 255, 0), 2)

        return annotated_frame, orientation

