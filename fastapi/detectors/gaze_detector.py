from collections import deque

from gaze_tracking import GazeTracking
from models.states import GazeState


class GazeDetector:
    def __init__(self, left_threshold=0.86, right_threshold=0.14, window_size=10, min_votes=7):
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
        recent = list(self.history)[-3:]

        if left_votes >= self.min_votes and recent.count(GazeState.LEFT) >= 2:
            return GazeState.LEFT

        if right_votes >= self.min_votes and recent.count(GazeState.RIGHT) >= 2:
            return GazeState.RIGHT

        if center_votes >= max(4, self.min_votes - 2):
            return GazeState.CENTER

        return GazeState.UNKNOWN
