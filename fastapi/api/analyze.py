import logging
from pathlib import Path

import cv2

from core.event_logger import EventLogger
from core.frame_processor import FrameProcessor
from core.violation_engine import ViolationEngine
from detectors.face_pipeline import FacePipeline
from detectors.gaze_detector import GazeDetector
from detectors.object_detector import ObjectDetector

logger = logging.getLogger(__name__)


def analyze_video(path):
    video_path = Path(path)
    base_dir = Path(__file__).resolve().parents[1]
    face_model = base_dir / "models" / "face_landmarker.task"
    yolo_model = base_dir / "yolov8n.pt"
    violations_dir = base_dir / "data" / "violations"

    face = FacePipeline(str(face_model))
    gaze = GazeDetector()
    obj = ObjectDetector(str(yolo_model))
    processor = FrameProcessor(face, gaze, obj)
    engine = ViolationEngine()
    event_logger = EventLogger(output_dir=violations_dir, session_name=video_path.stem)
    cap = cv2.VideoCapture(str(video_path))
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

            current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            mmss = f"{int(current_time // 60):02}:{int(current_time % 60):02}"
            second_bucket = int(current_time)

            data = processor.process(frame)
            events = engine.detect(data)
            for event in events:
                event_logger.add(
                    mmss,
                    event,
                    frame,
                    data.get("face_landmarks"),
                    second_bucket=second_bucket,
                )

            frame_index += 1
    finally:
        cap.release()

    result = event_logger.result()
    logger.info(
        "Analyze completed for %s: %s violations, output=%s",
        video_path.name,
        len(result),
        event_logger.output_dir,
    )
    return result
