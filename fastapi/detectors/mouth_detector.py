import math
import logging
from collections import deque
from models.states import MouthState

logger = logging.getLogger(__name__)

class MouthStateDetector:
    # MediaPipe Face Landmarks indices for mouth
    # Referenced: https://developers.google.com/mediapipe/solutions/vision/face_landmarker
    MOUTH_TOP = 13        # Top of mouth (center)
    MOUTH_BOTTOM = 14     # Bottom of mouth (center)
    UPPER_INNER = 78      # Upper inner lip (center)
    LOWER_INNER = 81      # Lower inner lip (center)
    
    LEFT_EYE = 33         # Left eye outer corner
    RIGHT_EYE = 263       # Right eye outer corner
    
    MOUTH_LEFT = 61       # Left mouth corner
    MOUTH_RIGHT = 291     # Right mouth corner

    def __init__(self, threshold=0.08, window=3):
        self.threshold = threshold
        self.history = deque(maxlen=window)

    def _distance(self, p1, p2):
        """Вычисляет евклидово расстояние между двумя точками."""
        if p1 is None or p2 is None:
            return 0
        try:
            return math.sqrt(
                (p1.x - p2.x) ** 2 +
                (p1.y - p2.y) ** 2
            )
        except (AttributeError, TypeError):
            return 0

    def detect(self, landmarks):
        if not landmarks:
            return MouthState.CLOSED
            
        try:
            mouth_top = landmarks[self.MOUTH_TOP] if len(landmarks) > self.MOUTH_TOP else None
            mouth_bottom = landmarks[self.MOUTH_BOTTOM] if len(landmarks) > self.MOUTH_BOTTOM else None
            
            left_eye = landmarks[self.LEFT_EYE] if len(landmarks) > self.LEFT_EYE else None
            right_eye = landmarks[self.RIGHT_EYE] if len(landmarks) > self.RIGHT_EYE else None
            
            mouth_left = landmarks[self.MOUTH_LEFT] if len(landmarks) > self.MOUTH_LEFT else None
            mouth_right = landmarks[self.MOUTH_RIGHT] if len(landmarks) > self.MOUTH_RIGHT else None
            
            if not all([mouth_top, mouth_bottom, left_eye, right_eye]):
                return MouthState.CLOSED
            
            mouth_distance = self._distance(mouth_top, mouth_bottom)
            
            face_scale = self._distance(left_eye, right_eye)
            
            if face_scale <= 1e-6:
                logger.debug("Face scale too small, skipping mouth detection")
                return MouthState.CLOSED
            
            ratio = mouth_distance / face_scale
            
            if mouth_left and mouth_right:
                mouth_width = self._distance(mouth_left, mouth_right)
                width_ratio = mouth_width / face_scale
                ratio = (ratio + width_ratio) / 2
            
            is_open = ratio > self.threshold
            self.history.append(is_open)
            
            logger.debug(f"Mouth detection: distance={mouth_distance:.3f}, face_scale={face_scale:.3f}, ratio={ratio:.3f}, threshold={self.threshold}, is_open={is_open}")
            
            if sum(self.history) > len(self.history) / 2:
                return MouthState.OPEN
            
            return MouthState.CLOSED
            
        except Exception as exc:
            logger.exception("Mouth detection failed: %s", exc)
            return MouthState.CLOSED
