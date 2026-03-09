import logging

logger = logging.getLogger(__name__)

class FrameProcessor:

    def __init__(self, face, gaze, object_detector):
        self.face = face
        self.gaze = gaze
        self.object = object_detector

    def process(self, frame):
        data = {
            "head": None,
            "mouth": None,
            "gaze": None,
            "objects": [],
            "face_landmarks": None,
        }

        face_data = None
        try:
            face_data = self.face.process(frame)
        except Exception as exc:
            logger.exception("Face pipeline failed: %s", exc)

        if face_data:
            data["head"] = face_data["head"]
            data["mouth"] = face_data["mouth"]
            data["face_landmarks"] = face_data.get("face_landmarks")

        try:
            data["gaze"] = self.gaze.detect(frame)
        except Exception as exc:
            logger.exception("Gaze detector failed: %s", exc)

        try:
            data["objects"] = self.object.detect(frame)
        except Exception as exc:
            logger.exception("Object detector failed: %s", exc)

        return data
