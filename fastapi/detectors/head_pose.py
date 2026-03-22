import logging
from collections import deque
from models.states import HeadState

logger = logging.getLogger(__name__)


class HeadPoseDetector:
    """
    Определяет позу (ориентацию) головы на основе MediaPipe Face Landmarks.
    Выявляет повороты и наклоны головы.
    """
    
    NOSE_TIP = 1
    LEFT_EYE = 33
    RIGHT_EYE = 263
    CHIN = 152
    LEFT_EAR = 234
    RIGHT_EAR = 454

    def __init__(
        self,
        horizontal_threshold=0.22,
        up_threshold=0.25,
        down_threshold=0.60,
        window_size=6,
        min_votes=4,
    ):
        """
        Инициализирует детектор позы головы.
        
        Args:
            horizontal_threshold: порог для бокового поворота
            up_threshold: порог для поворота вверх
            down_threshold: порог для поворота вниз
            window_size: размер окна для усреднения
            min_votes: минимальное количество голосов
        """
        self.horizontal_threshold = horizontal_threshold
        self.up_threshold = up_threshold
        self.down_threshold = down_threshold
        self.history = deque(maxlen=window_size)
        self.min_votes = min_votes
        logger.info(f"HeadPoseDetector initialized")

    def _raw_detect(self, landmarks):
        """
        Определяет позу головы на основе текущего кадра.
            
        Returns: поза головы (FORWARD, LEFT, RIGHT, UP, DOWN или UNKNOWN)
        """
        if not landmarks or len(landmarks) < 455:  # Нужно минимум 455 точек
            return HeadState.UNKNOWN
        
        try:
            nose = landmarks[self.NOSE_TIP]
            left_eye = landmarks[self.LEFT_EYE]
            right_eye = landmarks[self.RIGHT_EYE]
            chin = landmarks[self.CHIN]
            left_ear = landmarks[self.LEFT_EAR]
            right_ear = landmarks[self.RIGHT_EAR]

            # Вычисляем ширину лица
            face_width = abs(right_ear.x - left_ear.x)
            if face_width <= 1e-6:
                face_width = abs(right_eye.x - left_eye.x)

            # Вычисляем высоту лица
            eye_mid_y = (left_eye.y + right_eye.y) / 2.0
            vertical_distance = abs(chin.y - eye_mid_y)
            
            if face_width <= 1e-6 or vertical_distance <= 1e-6:
                logger.debug("Cannot calculate head pose: invalid face dimensions")
                return HeadState.UNKNOWN

            # Центр лица
            face_mid_x = (left_ear.x + right_ear.x) / 2.0
            
            # Нормализованные смещения
            horizontal_offset = (nose.x - face_mid_x) / face_width
            vertical_offset = (nose.y - eye_mid_y) / vertical_distance

            logger.debug(f"Head pose offsets - horizontal: {horizontal_offset:.3f}, vertical: {vertical_offset:.3f}")

            # Определяем позу
            if horizontal_offset >= self.horizontal_threshold:
                return HeadState.LEFT
            if horizontal_offset <= -self.horizontal_threshold:
                return HeadState.RIGHT
            if vertical_offset <= -self.up_threshold:
                return HeadState.UP
            if vertical_offset >= self.down_threshold:
                return HeadState.DOWN
            return HeadState.FORWARD
            
        except (AttributeError, IndexError, TypeError) as e:
            logger.debug(f"Error detecting head pose: {e}")
            return HeadState.UNKNOWN

    def detect(self, landmarks):
        """
        Определяет позу головы с использованием истории для стабильности.
            
        Returns: поза головы с сглаживанием
        """
        if not landmarks:
            return HeadState.UNKNOWN

        state = self._raw_detect(landmarks)
        self.history.append(state)
        
        if not self.history:
            return HeadState.UNKNOWN

        # Подсчитываем голоса для каждого состояния
        for candidate in (HeadState.LEFT, HeadState.RIGHT, HeadState.UP, HeadState.DOWN):
            if sum(1 for value in self.history if value == candidate) >= self.min_votes:
                logger.debug(f"Head state detected: {candidate.value}")
                return candidate

        if sum(1 for value in self.history if value == HeadState.FORWARD) >= max(2, self.min_votes - 1):
            return HeadState.FORWARD

        logger.debug(f"Head state unknown - history: {[s.value for s in self.history]}")
        return HeadState.UNKNOWN
