import logging
from collections import deque
from models.states import GazeState

logger = logging.getLogger(__name__)


class GazeDetector:
    """
    Детектор направления взгляда на основе MediaPipe Face Landmarks.
    Анализирует положение век и глаз для определения куда смотрит человек.
    """
    
    # MediaPipe Eye Landmarks indices
    # Left eye landmarks: 33 (outer), 160, 144, 158, 163, 7 (inner)
    LEFT_EYE_OUTER = 33
    LEFT_EYE_INNER = 133
    LEFT_EYE_UP = 159
    LEFT_EYE_DOWN = 145
    
    # Right eye landmarks: 263 (outer), 249, 390, 388, 387, 386
    RIGHT_EYE_OUTER = 263
    RIGHT_EYE_INNER = 362
    RIGHT_EYE_UP = 386
    RIGHT_EYE_DOWN = 374
    
    # Iris landmarks for gaze direction
    LEFT_IRIS = [468, 469, 470, 471, 472]
    RIGHT_IRIS = [473, 474, 475, 476, 477]

    def __init__(self, left_threshold=0.25, right_threshold=0.75, window_size=5, min_votes=3):
        """
        Инициализирует детектор взгляда.
        
        Args:
            left_threshold: порог для определения взгляда влево
            right_threshold: порог для определения взгляда вправо
            window_size: размер окна для усреднения результатов
            min_votes: минимальное количество голосов для определения направления
        """
        self.left_threshold = left_threshold
        self.right_threshold = right_threshold
        self.history = deque(maxlen=window_size)
        self.min_votes = min_votes
        logger.info(f"GazeDetector initialized with thresholds: left={left_threshold}, right={right_threshold}")

    def _get_eye_horizontal_ratio(self, landmarks, eye_inner_idx, eye_outer_idx, iris_indices):
        """
        Вычисляет горизонтальное отношение для определения направления взгляда.
        
        Args:
            landmarks: список точек лица MediaPipe
            eye_inner_idx: индекс внутренней точки глаза
            eye_outer_idx: индекс внешней точки глаза
            iris_indices: индексы точек радужки
            
        Returns: значение от 0.0 (взгляд влево) до 1.0 (взгляд вправо)
        """
        try:
            iris_points = []
            for idx in iris_indices:
                if len(landmarks) > idx and landmarks[idx] is not None:
                    iris_points.append(landmarks[idx])
            
            if not iris_points:
                logger.debug(f"No iris points found for indices {iris_indices}")
                return None
            
            eye_inner = landmarks[eye_inner_idx] if len(landmarks) > eye_inner_idx else None
            eye_outer = landmarks[eye_outer_idx] if len(landmarks) > eye_outer_idx else None
            
            if not eye_inner or not eye_outer:
                return None
            
            eye_width = abs(eye_outer.x - eye_inner.x)
            if eye_width <= 1e-6:
                return None
            
            iris_center_x = sum(p.x for p in iris_points) / len(iris_points)
            
            eye_left = min(eye_inner.x, eye_outer.x)
            relative_pos = (iris_center_x - eye_left) / eye_width
            
            relative_pos = max(0.0, min(1.0, relative_pos))
            
            return relative_pos
            
        except (AttributeError, IndexError, TypeError) as e:
            logger.debug(f"Error calculating eye ratio: {e}")
            return None

    def _raw_detect(self, landmarks):
        """
        Определяет направление взгляда на основе текущего кадра.
        """
        if not landmarks or len(landmarks) < 477:
            return GazeState.UNKNOWN
        
        left_ratio = self._get_eye_horizontal_ratio(
            landmarks, 
            self.LEFT_EYE_INNER, 
            self.LEFT_EYE_OUTER,
            self.LEFT_IRIS
        )
        right_ratio = self._get_eye_horizontal_ratio(
            landmarks,
            self.RIGHT_EYE_INNER,
            self.RIGHT_EYE_OUTER,
            self.RIGHT_IRIS
        )
        
        if left_ratio is None or right_ratio is None:
            logger.debug(f"Missing iris data: left_ratio={left_ratio}, right_ratio={right_ratio}")
            return GazeState.UNKNOWN

        avg_ratio = (left_ratio + right_ratio) / 2
        
        logger.debug(f"Gaze ratios - left: {left_ratio:.2f}, right: {right_ratio:.2f}, avg: {avg_ratio:.2f}")
        
        if avg_ratio >= self.right_threshold:
            return GazeState.RIGHT
        elif avg_ratio <= self.left_threshold:
            return GazeState.LEFT
        else:
            return GazeState.CENTER

    def detect(self, frame, landmarks=None):
        try:
            state = self._raw_detect(landmarks)
            self.history.append(state)
            
            unknown_votes = sum(1 for v in self.history if v == GazeState.UNKNOWN)
            left_votes = sum(1 for v in self.history if v == GazeState.LEFT)
            right_votes = sum(1 for v in self.history if v == GazeState.RIGHT)
            center_votes = sum(1 for v in self.history if v == GazeState.CENTER)
            
            recent = list(self.history)[-3:]
            
            if left_votes >= self.min_votes and recent.count(GazeState.LEFT) >= 2:
                logger.debug(f"Gaze detected as LEFT: {left_votes} votes")
                return GazeState.LEFT
            
            if right_votes >= self.min_votes and recent.count(GazeState.RIGHT) >= 2:
                logger.debug(f"Gaze detected as RIGHT: {right_votes} votes")
                return GazeState.RIGHT
            
            if center_votes >= max(4, self.min_votes - 2):
                logger.debug(f"Gaze detected as CENTER: {center_votes} votes")
                return GazeState.CENTER
            
            logger.debug(f"Gaze UNKNOWN - votes: left={left_votes}, right={right_votes}, center={center_votes}, unknown={unknown_votes}")
            return GazeState.UNKNOWN
            
        except Exception as e:
            logger.exception(f"Gaze detection failed: {e}")
            return GazeState.UNKNOWN
