from collections import deque

class GazeFilter:
    def __init__(self, window=5):
        self.buffer = deque(maxlen=window)

    def update(self, gaze):
        self.buffer.append(gaze)

        if len(self.buffer) < 3:
            return gaze

        return max(set(self.buffer), key=self.buffer.count)