from collections import deque

from gaze_tracking import GazeTracking
from models.states import GazeState


class GazeDetector:
    """Converts raw gaze ratios into more conservative stable gaze states."""

    def __init__(self, left_threshold=0.82, right_threshold=0.18, window_size=8, min_votes=5):
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
        self.gaze.refresh(frame)
        state = self._raw_detect()
        self.history.append(state)

        left_votes = sum(1 for value in self.history if value == GazeState.LEFT)
        right_votes = sum(1 for value in self.history if value == GazeState.RIGHT)
        center_votes = sum(1 for value in self.history if value == GazeState.CENTER)

        if left_votes >= self.min_votes and self.history[-1] == GazeState.LEFT:
            return GazeState.LEFT

        if right_votes >= self.min_votes and self.history[-1] == GazeState.RIGHT:
            return GazeState.RIGHT

        if center_votes >= max(3, self.min_votes - 1):
            return GazeState.CENTER

        return GazeState.UNKNOWN
