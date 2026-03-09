from ultralytics import YOLO
from models.states import ObjectState


class ObjectDetector:

    def __init__(self, model="yolov8n.pt"):
        self.model = YOLO(model)

    def detect(self, frame):
        results = self.model(frame)
        detections = []

        for box in results[0].boxes:

            cls_id = int(box.cls[0])

            if cls_id == 0:
                detections.append(ObjectState.PERSON)

            if cls_id == 67:
                detections.append(ObjectState.PHONE)

            if cls_id == 73:
                detections.append(ObjectState.BOOK)

        return detections