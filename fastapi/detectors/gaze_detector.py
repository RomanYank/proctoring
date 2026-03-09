from collections import deque

from gaze_tracking import GazeTracking
from models.states import GazeState


class GazeDetector:
    """Следит за положением зрачков и возвращает сглаженное состояние взгляда."""

    def __init__(self, left_threshold=0.75, right_threshold=0.25, window_size=6, min_votes=4):
        self.gaze = GazeTracking()
        self.left_threshold = left_threshold
        self.right_threshold = right_threshold
        self.history = deque(maxlen=window_size)
        self.min_votes = min_votes

    def _raw_detect(self):
        ratio = self.gaze.horizontal_ratio()
        if ratio is None:
            return GazeState.UNKNOWN
        if ratio >= self.left_threshold:
            return GazeState.LEFT
        if ratio <= self.right_threshold:
            return GazeState.RIGHT
        return GazeState.CENTER

    def detect(self, frame):
        """Обновляет кадр и возвращает текущий стабилизированный GazeState."""
        self.gaze.refresh(frame)
        state = self._raw_detect()
        self.history.append(state)

        if sum(1 for value in self.history if value == GazeState.LEFT) >= self.min_votes:
            return GazeState.LEFT

        if sum(1 for value in self.history if value == GazeState.RIGHT) >= self.min_votes:
            return GazeState.RIGHT

        if sum(1 for value in self.history if value == GazeState.CENTER) >= max(2, self.min_votes - 1):
            return GazeState.CENTER

        return GazeState.UNKNOWN
