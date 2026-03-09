import cv2

from core.frame_processor import FrameProcessor
from core.violation_engine import ViolationEngine
from core.event_logger import EventLogger

from detectors.face_pipeline import FacePipeline
from detectors.gaze_detector import GazeDetector
from detectors.object_detector import ObjectDetector


def analyze_video(path):
    face = FacePipeline("models/face_landmarker.task")
    gaze = GazeDetector()
    obj = ObjectDetector()
    processor = FrameProcessor(face, gaze, obj)
    engine = ViolationEngine()
    logger = EventLogger()
    cap = cv2.VideoCapture(path)
    frame_index = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        if frame_index % 5 != 0:
            frame_index += 1
            continue

        time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        mmss = f"{int(time//60):02}:{int(time%60):02}"

        data = processor.process(frame)

        events = engine.detect(data)

        for e in events:
            logger.add(mmss, e)

        frame_index += 1

    cap.release()

    return logger.result()