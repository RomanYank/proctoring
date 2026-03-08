from enum import Enum

class HeadState(Enum):
    FORWARD = "forward"
    LEFT = "left"
    RIGHT = "right"
    UNKNOWN = "unknown"

class GazeState(Enum):
    FORWARD = "forward"
    LEFT = "left"
    RIGHT = "right"
    UNKNOWN = "unknown"

class MouthState(Enum):
    OPEN = "open"
    CLOSED = "closed"
    UNKNOWN = "unknown"

class ObjectState(Enum):
    PERSON = 0
    PHONE = 67
    BOOK = 73