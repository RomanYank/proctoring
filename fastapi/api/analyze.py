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

    # Видео уже сжато на фронтенде в actionUpload
    # поэтому используем исходный путь напрямую
    processed_video_path = str(video_path)
    
    face = FacePipeline(str(face_model))
    gaze = GazeDetector()
    obj = ObjectDetector(str(yolo_model))
    processor = FrameProcessor(face, gaze, obj)
    engine = ViolationEngine()
    event_logger = EventLogger(output_dir=violations_dir, session_name=video_path.stem)
    
    cap = cv2.VideoCapture(processed_video_path)
    frame_index = 0

    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video file: {processed_video_path}")

    try:
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        logger.info(f"Video info: {total_frames} frames at {fps} fps, resolution: {width}x{height}")
        
        if total_frames == 0:
            logger.warning("Video has no frames!")
            return []
        
        processed_frames = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Обрабатываем каждый второй кадр для оптимизации
            if frame_index % 2 != 0:
                frame_index += 1
                continue

            current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            mmss = f"{int(current_time // 60):02}:{int(current_time % 60):02}"
            second_bucket = int(current_time)

            # Обрабатываем кадр
            try:
                data = processor.process(frame)
                
                logger.debug(f"Frame {frame_index}: gaze={data.get('gaze')}, head={data.get('head')}, mouth={data.get('mouth')}, objects={len(data.get('objects', []))}")
                
                events = engine.detect(data)
                
                for event in events:
                    event_logger.add(
                        mmss,
                        event,
                        frame,
                        data.get("face_landmarks"),
                        second_bucket=second_bucket,
                    )
                    logger.info(f"Violation detected at {mmss}: {event}")
                    
            except Exception as e:
                logger.exception(f"Error processing frame {frame_index}: {e}")

            frame_index += 1
            processed_frames += 1
            
            if frame_index % 50 == 0:
                logger.debug(f"Processed {processed_frames}/{total_frames//2} frames (every 2nd frame)")
                
    finally:
        cap.release()

    result = event_logger.result()
    logger.info(
        f"Analysis completed for {video_path.name}: {len(result)} violations detected, "
        f"processed {processed_frames} frames out of {total_frames}"
    )
    return result
    )
    return result
