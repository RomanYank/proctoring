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
            "objects": []
        }

        face_data = self.face.process(frame)

        if face_data:
            data["head"] = face_data["head"]
            data["mouth"] = face_data["mouth"]

        data["gaze"] = self.gaze.detect(frame)
        data["objects"] = self.object.detect(frame)

        return data