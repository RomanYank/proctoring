from gaze_tracking import GazeTracking
from models.states import GazeState

class GazeDetector:

    def __init__(self):
        self.gaze = GazeTracking()

    def detect(self, frame):
        self.gaze.refresh(frame)

        if self.gaze.is_right():
            return GazeState.RIGHT

        if self.gaze.is_left():
            return GazeState.LEFT

        if self.gaze.is_center():
            return GazeState.CENTER

        return GazeState.UNKNOWN