import math
from collections import deque
from models.states import MouthState

class MouthStateDetector:

    UPPER_LIP = 13
    LOWER_LIP = 14
    LEFT_EYE = 33
    RIGHT_EYE = 263

    def __init__(self, threshold=0.25, window=5):
        self.threshold = threshold
        self.history = deque(maxlen=window)

    def _distance(self, p1, p2):
        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        )

    def detect(self, landmarks):
        upper = landmarks[self.UPPER_LIP]
        lower = landmarks[self.LOWER_LIP]

        left_eye = landmarks[self.LEFT_EYE]
        right_eye = landmarks[self.RIGHT_EYE]

        mouth_distance = self._distance(upper, lower)
        face_scale = self._distance(left_eye, right_eye)

        if face_scale <= 1e-6:
            return MouthState.CLOSED

        ratio = mouth_distance / face_scale
        state = ratio > self.threshold

        self.history.append(state)

        if sum(self.history) > len(self.history) / 2:
            return MouthState.OPEN

        return MouthState.CLOSED
