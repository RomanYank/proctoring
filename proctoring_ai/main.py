#модель уже обучена на датасете COCO (https://docs.ultralytics.com/ru/datasets/detect/coco/#sample-images-and-annotations)

# import cv2
# from models.ObjectDetectionModel import ObjectDetectionModel
# from models.GazeDirectionDetectorModel import GazeDirectionDetectorModel
# from models.HeadDetectionModel import HeadDetectionModel
# def main():
#     object_detection_model = ObjectDetectionModel("yolov8n.pt")
#     gaze_detection_model = GazeDirectionDetectorModel()
#     head_detection_model = HeadDetectionModel()
#     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         # Обнаружение объектов
#         annotated_frame, results = object_detection_model.detect_objects(frame)
#         # Отслеживание взгляда (используем уже аннотированный кадр)
#         annotated_frame, gaze_text = gaze_detection_model.detect_direction(annotated_frame)
#         cv2.putText(annotated_frame, gaze_text, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
#         # Детекция головы и ориентации
#         annotated_frame = head_detection_model.detect_head_orientation(annotated_frame, annotated_frame)
#         # Показ результатов
#         cv2.imshow("YOLOv8 - Person Detection, Gaze Tracking & Head Orientation", annotated_frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     cap.release()
#     cv2.destroyAllWindows()
# if __name__ == "__main__":
#     main()

#запуск uvicorn main:app --reload
import shutil
import os
import yaml
import tempfile
import pandas as pd
import cv2
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from predictor import ModelService
from processing import preprocess_dataset, convert_to_yolo
from models.ObjectDetectionModel import ObjectDetectionModel
from models.GazeDirectionDetectorModel import GazeDirectionDetectorModel
from models.HeadDetectionModel import HeadDetectionModel
from ultralytics import YOLO

app = FastAPI()
predictor = ModelService()

object_detection_model = ObjectDetectionModel("yolov8n.pt")
gaze_detection_model = GazeDirectionDetectorModel()
head_detection_model = HeadDetectionModel()

IMAGES_PATH = "data/images/train"
LABELS_PATH = "data/labels/train"
DATA_YAML_PATH = "data/config.yaml"
MODEL_SAVE_PATH = "models/best.pt"
SAVE_DIR = r"C:/ospanel/domains/project.localhost/public/frontend/web/record/video"

@app.post("/train/")
async def train_model(csv_file: UploadFile = File(...), class_desc_file: UploadFile = File(...), epochs: int = Form(50), max_images: int = Form(200)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as csv_temp:
        shutil.copyfileobj(csv_file.file, csv_temp)
        csv_path = csv_temp.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as desc_temp:
        shutil.copyfileobj(class_desc_file.file, desc_temp)
        desc_path = desc_temp.name

    target_classes = ["Person", "Book", "Mobile phone"]

    df, label_encoder, _ = preprocess_dataset(csv_path=csv_path, class_desc_path=desc_path, target_classes=target_classes, max_images_per_class=max_images)

    convert_to_yolo(df, IMAGES_PATH, LABELS_PATH, label_encoder)

    data_config = {
        "train": os.path.abspath(IMAGES_PATH),
        "val": os.path.abspath(IMAGES_PATH),
        "nc": len(target_classes),
        "names": target_classes
    }

    os.makedirs(os.path.dirname(DATA_YAML_PATH), exist_ok=True)
    with open(DATA_YAML_PATH, "w") as f:
        yaml.dump(data_config, f)

    predictor.train(data_yaml_path=DATA_YAML_PATH, epochs=epochs)
    predictor.save_model(MODEL_SAVE_PATH)

    os.remove(csv_path)
    os.remove(desc_path)

    return {"message": "Модель успешно обучена и сохранена"}

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
            violations.append({
                "time": mm_ss_time,
                "violation": f"Смотрит в сторону ({gaze_direction})"
            })

        _, head_orientation = head_detection_model.detect_head_orientation(frame, frame)
        if head_orientation != "forward":
            violations.append({
                "time": mm_ss_time,
                "violation": f"Отклонение головы ({head_orientation})"
            })

        frame_index += 1

    cap.release()

    return {
        "violations": violations
    }

@app.post("/load/")
async def load_pretrained_model(model: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pt") as temp_model_file:
        shutil.copyfileobj(model.file, temp_model_file)
        temp_model_path = temp_model_file.name

    predictor.load_model(temp_model_path)
    predictor.save_model(MODEL_SAVE_PATH)

    os.remove(temp_model_path)

    return {"message": "Модель успешно загружена и сохранена"}

@app.post("/evaluate/")
async def evaluate_image(image: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image_file:
        shutil.copyfileobj(image.file, temp_image_file)
        temp_image_path = temp_image_file.name

    predictions, base64_image = predictor.predict(temp_image_path)

    if predictions:
        table_html = "<table border='1' cellpadding='5' cellspacing='0'>"
        table_html += "<tr><th>Класс</th><th>ID</th><th>Достоверность</th></tr>"
        for pred in predictions:
            table_html += (
                f"<tr><td>{pred['class_name']}</td>"
                f"<td>{pred['class_id']}</td>"
                f"<td>{pred['confidence']:.2f}</td></tr>"
            )
        table_html += "</table>"
    else:
        table_html = "<p>Объекты не найдены</p>"

    os.remove(temp_image_path)

    return JSONResponse({
        "predictions": table_html,
        "image": base64_image
    })