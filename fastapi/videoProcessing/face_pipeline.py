from dataclasses import dataclass
from videoProcessing.face_landmarker import FaceLandmarkDetector
from videoProcessing.head_orientation import HeadOrientationDetector
from videoProcessing.mouth_state import MouthStateDetector
from videoProcessing.states import HeadState, MouthState


@dataclass
class FaceData:
    head: HeadState
    mouth: MouthState
    landmarks: object | None


class FacePipeline:

    def __init__(self, model_path: str):
        self.landmarker = FaceLandmarkDetector(model_path)
        self.head_detector = HeadOrientationDetector()
        self.mouth_detector = MouthStateDetector()
        self.timestamp = 0

    def process(self, frame) -> FaceData:
        self.timestamp += 1
        result = self.landmarker.detect(frame, self.timestamp)

        if not result or not result.face_landmarks:
            return FaceData(
                head=HeadState.UNKNOWN,
                mouth=MouthState.UNKNOWN,
                landmarks=None
            )

        landmarks = result.face_landmarks[0]

        head_state = self.head_detector.classify(
            landmarks,
            frame.shape[:2]
        )

        mouth_state = self.mouth_detector.detect(landmarks)

        return FaceData(
            head=head_state,
            mouth=mouth_state,
            landmarks=landmarks
        )

    def close(self):
        self.landmarker.close()