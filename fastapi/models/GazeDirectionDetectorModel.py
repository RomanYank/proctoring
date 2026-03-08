from gaze_tracking import GazeTracking
from videoProcessing.states import GazeState

class GazeDirectionDetectorModel:
    def __init__(self):
        self.gaze = GazeTracking()

    def detect_direction(self, frame):
        self.gaze.refresh(frame)

        if self.gaze.is_blinking():
            return GazeState.UNKNOWN

        if self.gaze.is_left():
            return GazeState.LEFT

        if self.gaze.is_right():
            return GazeState.RIGHT

        if self.gaze.is_center():
            return GazeState.FORWARD

        return GazeState.UNKNOWN