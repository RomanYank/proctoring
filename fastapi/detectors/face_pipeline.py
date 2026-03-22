from detectors.face_landmarker import FaceLandmarkDetector
from detectors.head_pose import HeadPoseDetector
from detectors.mouth_detector import MouthStateDetector

class FacePipeline:
    def __init__(self, model):
        self.landmarks = FaceLandmarkDetector(model)
        self.mouth = MouthStateDetector()
        self.head_pose = HeadPoseDetector()
        self.timestamp = 0

    def process(self, frame):
        result = self.landmarks.detect(frame, self.timestamp)
        self.timestamp += 1

        if not result.face_landmarks:
            return None

        landmarks = result.face_landmarks[0]
        mouth_state = self.mouth.detect(landmarks)
        head_state = self.head_pose.detect(landmarks)

        return {
            "mouth": mouth_state,
            "head": head_state,
            "face_landmarks": landmarks,
        }
