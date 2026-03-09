from detectors.face_landmarker import FaceLandmarkDetector
from detectors.mouth_detector import MouthStateDetector
from models.states import HeadState


class FacePipeline:
    def __init__(self, model):
        self.landmarks = FaceLandmarkDetector(model)
        self.mouth = MouthStateDetector()
        self.timestamp = 0

    def process(self, frame):
        result = self.landmarks.detect(frame, self.timestamp)
        self.timestamp += 1

        if not result.face_landmarks:
            return None

        landmarks = result.face_landmarks[0]
        mouth_state = self.mouth.detect(landmarks)

        return {
            "mouth": mouth_state,
            "head": HeadState.FORWARD
        }