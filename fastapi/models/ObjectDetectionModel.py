from ultralytics import YOLO
from videoProcessing.states import ObjectState


class ObjectDetectionModel:
    def __init__(self, model_path="yolov11n.pt"):
        self.model = YOLO(model_path)

    def detect_objects(self, frame):
        results = self.model(frame)[0]
        detections = []
        for det in results.boxes:

            cls_id = int(det.cls[0].item())
            conf = det.conf[0].item()

            if conf < 0.5:
                continue

            if cls_id == ObjectState.PERSON.value:
                detections.append(ObjectState.PERSON)

            elif cls_id == ObjectState.PHONE.value:
                detections.append(ObjectState.PHONE)

            elif cls_id == ObjectState.BOOK.value:
                detections.append(ObjectState.BOOK)

        return detections, results