import os
import shutil
from fastapi import FastAPI, UploadFile, File
from api.analyze import analyze_video

app = FastAPI()

SAVE_DIR = "data/videos"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.post("/analyze/")
async def analyze(video: UploadFile = File(...)):

    filename = os.path.basename(video.filename)
    path = os.path.join(SAVE_DIR, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    result = analyze_video(path)

    return {"violations": result}