import os
import shutil
import cv2
from fastapi import FastAPI, UploadFile, File
from models.ObjectDetectionModel import ObjectDetectionModel
from models.GazeDirectionDetectorModel import GazeDirectionDetectorModel
from models.HeadDetectionModel import HeadDetectionModel

SAVE_DIR = "data/videos"
os.makedirs(SAVE_DIR, exist_ok=True)

app = FastAPI()

# Модели
object_detection_model = ObjectDetectionModel("yolov8n.pt")
gaze_detection_model = GazeDirectionDetectorModel()
head_detection_model = HeadDetectionModel()

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

        _, detection_result = object_detection_model.detect_objects(frame)
        boxes = detection_result[0].boxes

        person_count = 0
        phone_detected = False
        book_detected = False

        for box in boxes:
            cls_id = int(box.cls[0].item())
            conf = box.conf[0].item()
            if conf < 0.8:
                continue

            if cls_id == 0:
                person_count += 1
            elif cls_id == 67:
                phone_detected = True
            elif cls_id == 73:
                book_detected = True

        if person_count > 1:
            violations.append({"time": mm_ss_time, "violation": "В кадре больше одного человека"})
        if phone_detected:
            violations.append({"time": mm_ss_time, "violation": "Использование телефона"})
        if book_detected:
            violations.append({"time": mm_ss_time, "violation": "Использование книги"})

        _, gaze_direction = gaze_detection_model.detect_direction(frame)
        if gaze_direction in ["left", "right"]:
            violations.append({"time": mm_ss_time, "violation": f"Смотрит в сторону ({gaze_direction})"})

        _, head_orientation = head_detection_model.detect_head_orientation(frame, frame)
        if head_orientation != "forward":
            violations.append({"time": mm_ss_time, "violation": f"Отклонение головы ({head_orientation})"})

        frame_index += 1

    cap.release()
    return {"violations": violations}
