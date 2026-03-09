from models.states import GazeState, HeadState


class UserCalibrator:
    """Собирает первые кадровые коэффициенты, чтобы отличать нормальный взгляд/голову."""

    def __init__(self, required_frames=30, min_center_fraction=0.7):
        self.required_frames = required_frames
        self.min_center_fraction = min_center_fraction
        self.frames = 0
        self.head_center_count = 0
        self.gaze_center_count = 0
        self.ready = False

    def update(self, head_state, gaze_state):
        """Обновляет статистику и отмечает готовность, когда достаточно кадров с «прямым» состоянием."""
        self.frames += 1
        if head_state and head_state == HeadState.FORWARD:
            self.head_center_count += 1
        if gaze_state and gaze_state == GazeState.CENTER:
            self.gaze_center_count += 1

        if self.frames >= self.required_frames:
            head_fraction = self.head_center_count / self.frames
            gaze_fraction = self.gaze_center_count / self.frames
            self.ready = head_fraction >= self.min_center_fraction and gaze_fraction >= self.min_center_fraction
        return self.ready
