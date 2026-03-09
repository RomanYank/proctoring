import os
import shutil
import cv2
from fastapi import FastAPI, UploadFile, File
from models.ObjectDetectionModel import ObjectDetectionModel
from models.GazeDirectionDetectorModel import GazeDirectionDetectorModel
from videoProcessing.face_pipeline import FacePipeline
from videoProcessing.states import ObjectState, HeadState, GazeState, MouthState
from violations.violation_logger import ViolationLogger
from filters.gaze_filter import GazeFilter

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

    logger = ViolationLogger()
    gaze_filter = GazeFilter()

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        if frame_index % 5 != 0:
            frame_index += 1
            continue

        timestamp_sec = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        mm_ss_time = f"{int(timestamp_sec // 60):02}:{int(timestamp_sec % 60):02}"
        face_data = face_pipeline.process(frame)

        if face_data.head not in [HeadState.FORWARD, HeadState.UNKNOWN]:

            logger.log(
                violations,
                mm_ss_time,
                "head",
                f"Отклонение головы ({face_data.head.value})"
            )

        if face_data.mouth == MouthState.OPEN:

            mouth_counter += 1

            if mouth_counter > 10:

                logger.log(
                    violations,
                    mm_ss_time,
                    "talking",
                    "Возможный разговор"
                )

        else:
            mouth_counter = 0

        if face_data.head == HeadState.FORWARD:

            gaze_state = gaze_model.detect_direction(frame)
            gaze_state = gaze_filter.update(gaze_state)

            if gaze_state in [GazeState.LEFT, GazeState.RIGHT]:

                logger.log(
                    violations,
                    mm_ss_time,
                    "gaze",
                    f"Смотрит в сторону ({gaze_state.value})"
                )

        detections, _ = object_model.detect_objects(frame)
        person_count = detections.count(ObjectState.PERSON)

        if person_count > 1:

            logger.log(
                violations,
                mm_ss_time,
                "person",
                "В кадре больше одного человека"
            )

        if ObjectState.PHONE in detections:

            logger.log(
                violations,
                mm_ss_time,
                "phone",
                "Использование телефона"
            )

        if ObjectState.BOOK in detections:

            logger.log(
                violations,
                mm_ss_time,
                "book",
                "Использование книги"
            )

    cap.release()
    face_pipeline.close()

    return {"violations": violations}