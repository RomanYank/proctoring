import os
import shutil
from pathlib import Path
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from api.analyze import analyze_video

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
SAVE_DIR = BASE_DIR / "data" / "videos"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

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
