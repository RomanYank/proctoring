import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision


class FaceLandmarkDetector:

    def __init__(self, model_path):
        options = vision.FaceLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
            running_mode=vision.RunningMode.VIDEO,
            num_faces=1
        )

        self.detector = vision.FaceLandmarker.create_from_options(options)

    def detect(self, frame, timestamp):
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        )

        return self.detector.detect_for_video(mp_image, timestamp)