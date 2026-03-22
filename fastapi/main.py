import os
import shutil
from pathlib import Path
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from api.analyze import analyze_video
from core.frame_processor import FrameProcessor
from core.violation_engine import ViolationEngine
from detectors.face_pipeline import FacePipeline
from detectors.gaze_detector import GazeDetector
from detectors.object_detector import ObjectDetector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.post("/test/")
async def test_detection():
    """
    Тестовый эндпоинт для проверки работы детекторов
    """
    try:
        # Создаем тестовый кадр (просто черный квадрат)
        import numpy as np
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Инициализируем детекторы
        base_dir = Path(__file__).resolve().parent
        face_model = base_dir / "models" / "face_landmarker.task"
        yolo_model = base_dir / "yolov8n.pt"
        
        face = FacePipeline(str(face_model))
        gaze = GazeDetector()
        obj = ObjectDetector(str(yolo_model))
        processor = FrameProcessor(face, gaze, obj)
        engine = ViolationEngine()
        
        # Обрабатываем тестовый кадр
        data = processor.process(test_frame)
        events = engine.detect(data)
        
        return {
            "test_frame_processed": True,
            "detector_data": {
                "gaze": str(data.get("gaze")),
                "head": str(data.get("head")),
                "mouth": str(data.get("mouth")),
                "objects_count": len(data.get("objects", []))
            },
            "violations": events
        }
        
    except Exception as e:
        logger.exception(f"Test failed: {e}")
        return {"error": str(e)}

@app.post("/analyze/")
async def analyze(video: UploadFile = File(...)):
    """
    Анализирует загруженное видео на предмет нарушений прокторинга.
    
    Args: видео файл для анализа
        
    Returns: список обнаруженных нарушений с временем
    """
    if not video.filename:
        logger.warning("Empty filename provided")
        raise HTTPException(status_code=400, detail="Empty filename.")

    filename = os.path.basename(video.filename)
    path = SAVE_DIR / filename
    
    logger.info(f"Received video upload: {filename}")

    try:
        logger.info(f"Saving video to {path}")
        with open(path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        
        file_size_mb = path.stat().st_size / (1024 * 1024)
        logger.info(f"Video saved: {filename} ({file_size_mb:.2f} MB)")

        logger.info(f"Starting analysis of {filename}")
        result = analyze_video(str(path))
        
        logger.info(f"Analysis completed for {filename}: {len(result)} violations detected")
        return {"violations": result, "filename": filename}
        
    except RuntimeError as e:
        logger.exception(f"Runtime error during analysis: {e}")
        raise HTTPException(status_code=400, detail=f"Video processing failed: {str(e)}")
    except Exception as exc:
        logger.exception(f"Unexpected error during analysis of {filename}: {exc}")
        raise HTTPException(status_code=500, detail=f"Analyze failed: {str(exc)}")
    finally:
        video.file.close()
