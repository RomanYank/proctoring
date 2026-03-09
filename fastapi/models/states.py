from enum import Enum

class HeadState(Enum):
    FORWARD = "forward"
    LEFT = "left"
    RIGHT = "right"
    DOWN = "down"
    UP = "up"
    UNKNOWN = "unknown"

class MouthState(Enum):
    OPEN = "open"
    CLOSED = "closed"

class GazeState(Enum):
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    UNKNOWN = "unknown"

class ObjectState(Enum):
    PERSON = "person"
    PHONE = "phone"
    BOOK = "book"