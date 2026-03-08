import math
from videoProcessing.states import HeadState

class HeadOrientationDetector:

    LEFT_EYE = 33
    RIGHT_EYE = 263
    NOSE = 1

    def classify(self, landmarks, frame_shape):
        left_eye = landmarks[self.LEFT_EYE]
        right_eye = landmarks[self.RIGHT_EYE]
        nose = landmarks[self.NOSE]

        lx, ly = left_eye.x, left_eye.y
        rx, ry = right_eye.x, right_eye.y
        nx = nose.x

        eye_angle = math.degrees(math.atan2(ry - ly, rx - lx))
        eye_center = (lx + rx) / 2
        nose_offset = nx - eye_center

        if nose_offset > 0.04:
            return HeadState.RIGHT

        if nose_offset < -0.04:
            return HeadState.LEFT

        if abs(eye_angle) > 20:
            return HeadState.UNKNOWN

        return HeadState.FORWARD