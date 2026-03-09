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
            state = None

            if cls_id == 0:
                state = ObjectState.PERSON
            elif cls_id == 67:
                state = ObjectState.PHONE
            elif cls_id == 73:
                state = ObjectState.BOOK

            if state is None:
                continue

            coords = box.xyxy[0].cpu().numpy().astype(int)
            detections.append({
                "state": state,
                "bbox": (int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])),
            })

        return detections
