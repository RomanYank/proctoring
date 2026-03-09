import os
import shutil
from pathlib import Path
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from api.analyze import analyze_video

app = FastAPI()
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
SAVE_DIR = BASE_DIR / "data" / "videos"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/analyze/")
async def analyze(video: UploadFile = File(...)):
    if not video.filename:
        raise HTTPException(status_code=400, detail="Empty filename.")

    filename = os.path.basename(video.filename)
    path = SAVE_DIR / filename

    try:
        with open(path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        result = analyze_video(str(path))
        return {"violations": result}
    except Exception as exc:
        logger.exception("Analyze failed for %s: %s", filename, exc)
        raise HTTPException(status_code=500, detail=f"Analyze failed: {exc}")
    finally:
        video.file.close()
