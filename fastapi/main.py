import os
import shutil
import cv2
from fastapi import FastAPI, UploadFile, File
from models.ObjectDetectionModel import ObjectDetectionModel
from models.GazeDirectionDetectorModel import GazeDirectionDetectorModel
from videoProcessing.face_pipeline import FacePipeline
from videoProcessing.states import ObjectState, HeadState, GazeState

SAVE_DIR = "data/videos"
os.makedirs(SAVE_DIR, exist_ok=True)

app = FastAPI()

# модели
object_model = ObjectDetectionModel("yolov8n.pt")
gaze_model = GazeDirectionDetectorModel()

# pipeline лица
face_pipeline = FacePipeline("models/face_landmarker.task")


@app.post("/analyze/")
async def analyze_video(video: UploadFile = File(...)):
    filename = os.path.basename(video.filename)
    input_path = os.path.join(SAVE_DIR, filename)

    with open(input_path, "wb") as f:
        shutil.copyfileobj(video.file, f)

    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        return {"error": "Не удалось открыть видео"}

    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    violations = []
    frame_index = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        timestamp_sec = round(frame_index / frame_rate, 2)
        mm_ss_time = f"{int(timestamp_sec // 60):02}:{int(timestamp_sec % 60):02}"

        face_data = face_pipeline.process(frame)

        if face_data.head != HeadState.FORWARD and face_data.head != HeadState.UNKNOWN:
            violations.append({
                "time": mm_ss_time,
                "violation": f"Отклонение головы ({face_data.head.value})"
            })

        gaze_state = gaze_model.detect_direction(frame)

        if gaze_state in [GazeState.LEFT, GazeState.RIGHT]:
            violations.append({
                "time": mm_ss_time,
                "violation": f"Смотрит в сторону ({gaze_state.value})"
            })

        detections, _ = object_model.detect_objects(frame)
        person_count = detections.count(ObjectState.PERSON)

        if person_count > 1:
            violations.append({
                "time": mm_ss_time,
                "violation": "В кадре больше одного человека"
            })

        if ObjectState.PHONE in detections:
            violations.append({
                "time": mm_ss_time,
                "violation": "Использование телефона"
            })

        if ObjectState.BOOK in detections:
            violations.append({
                "time": mm_ss_time,
                "violation": "Использование книги"
            })

        frame_index += 1

    cap.release()
    face_pipeline.close()

    return {"violations": violations}