import cv2
from pathlib import Path

from core.frame_processor import FrameProcessor
from core.violation_engine import ViolationEngine
from core.calibration import UserCalibrator
from core.event_logger import EventLogger

from detectors.face_pipeline import FacePipeline
from detectors.gaze_detector import GazeDetector
from detectors.object_detector import ObjectDetector


def analyze_video(path):
    base_dir = Path(__file__).resolve().parents[1]
    face_model = base_dir / "models" / "face_landmarker.task"
    yolo_model = base_dir / "yolov8n.pt"
    violations_dir = base_dir / "data" / "violations"

    face = FacePipeline(str(face_model))
    gaze = GazeDetector()
    obj = ObjectDetector(str(yolo_model))
    processor = FrameProcessor(face, gaze, obj)
    engine = ViolationEngine()
    calibrator = UserCalibrator()
    logger = EventLogger(output_dir=violations_dir)
    cap = cv2.VideoCapture(path)
    frame_index = 0

    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video file: {path}")

    try:
        while True:

            ret, frame = cap.read()

            if not ret:
                break

            if frame_index % 5 != 0:
                frame_index += 1
                continue

            time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            mmss = f"{int(time//60):02}:{int(time%60):02}"
            second_bucket = int(time)

            data = processor.process(frame)
            calibrator.update(data.get("head"), data.get("gaze"))

            events = engine.detect(data) if calibrator.ready else []

            for e in events:
                logger.add(
                    mmss,
                    e,
                    frame,
                    data.get("face_landmarks"),
                    second_bucket=second_bucket,
                )

            frame_index += 1
    finally:
        cap.release()

    return logger.result()
