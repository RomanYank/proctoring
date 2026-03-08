import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision

class FaceLandmarkDetector:

    def __init__(self, model_path: str):
        options = vision.FaceLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
            running_mode=vision.RunningMode.VIDEO,
            num_faces=1,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.detector = vision.FaceLandmarker.create_from_options(options)

    def detect(self, frame, timestamp: int):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame_rgb
        )

        return self.detector.detect_for_video(mp_image, timestamp)

    def close(self):
        if self.detector:
            self.detector.close()