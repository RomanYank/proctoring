from gaze_tracking import GazeTracking
#Документация и примеры для GazeTracking https://github.com/antoinelame/GazeTracking
class GazeDirectionDetectorModel:
    def __init__(self):
        self.gaze = GazeTracking()

    def detect_direction(self, frame):
        self.gaze.refresh(frame)
        annotated_frame = self.gaze.annotated_frame()

        if self.gaze.is_blinking():
            direction = "blinking"
        elif self.gaze.is_left():
            direction = "left"
        elif self.gaze.is_right():
            direction = "right"
        elif self.gaze.is_center():
            direction = "center"
        else:
            direction = "unknown"

        return annotated_frame, direction