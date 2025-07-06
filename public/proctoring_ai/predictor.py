import os
from ultralytics import YOLO
import torch
import cv2
import pandas as pd
import base64
from io import BytesIO
from PIL import Image

class ModelService:
    def __init__(self):
        model_path = "models/best.pt"
        if not os.path.isfile(model_path):
            model_path = "yolo11n.pt"

        self.model = YOLO(model_path)

    def train(self, data_yaml_path, epochs=50, imgsz=640, batch=16):
        print("Начало обучения модели...")
        self.model.train(data=data_yaml_path, epochs=epochs, imgsz=imgsz, batch=batch)
        print("Обучение завершено.")

    def predict(self, image_path, conf=0.7):
        results = self.model(image_path, conf=conf)
        annotated = results[0].plot()

        pil_image = Image.fromarray(annotated)
        buffer = BytesIO()
        pil_image.save(buffer, format="PNG")
        base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

        predictions = []

        boxes = getattr(results[0].boxes, 'data', None)
        class_ids = getattr(results[0].boxes, 'cls', None)
        confidences = getattr(results[0].boxes, 'conf', None)
        names = results[0].names if hasattr(results[0], 'names') else {}

        if boxes is not None and class_ids is not None and confidences is not None:
            boxes = boxes.tolist()
            class_ids = class_ids.tolist()
            confidences = confidences.tolist()

            for i in range(len(boxes)):
                predictions.append({
                    "confidence": confidences[i],
                    "class_id": int(class_ids[i]),
                    "class_name": names.get(int(class_ids[i]), "unknown")
                })

        return predictions, base64_image

    def save_model(self, save_path='best.pt'):
        self.model.save(save_path)
        print(f"Модель сохранена в {save_path}")

    def load_model(self, model_path):
        self.model = YOLO(model_path)
        print(f"Модель загружена из {model_path}")