from ultralytics import YOLO

from models.states import ObjectState


class ObjectDetector:
    def __init__(
        self,
        model="yolov8n.pt",
        person_confidence=0.6,
        phone_confidence=0.45,
        book_confidence=0.45,
        min_person_area_ratio=0.08,
    ):
        self.model = YOLO(model)
        self.person_confidence = person_confidence
        self.phone_confidence = phone_confidence
        self.book_confidence = book_confidence
        self.min_person_area_ratio = min_person_area_ratio

    def detect(self, frame):
        results = self.model(frame)
        detections = []
        frame_height, frame_width = frame.shape[:2]
        frame_area = max(frame_height * frame_width, 1)

        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            state = None

            if cls_id == 0 and confidence >= self.person_confidence:
                state = ObjectState.PERSON
            elif cls_id == 67 and confidence >= self.phone_confidence:
                state = ObjectState.PHONE
            elif cls_id == 73 and confidence >= self.book_confidence:
                state = ObjectState.BOOK

            if state is None:
                continue

            coords = box.xyxy[0].cpu().numpy().astype(int)
            x1, y1, x2, y2 = (int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3]))
            width = max(x2 - x1, 0)
            height = max(y2 - y1, 0)
            area_ratio = (width * height) / frame_area

            if state == ObjectState.PERSON and area_ratio < self.min_person_area_ratio:
                continue

            detections.append(
                {
                    "state": state,
                    "bbox": (x1, y1, x2, y2),
                    "confidence": confidence,
                    "area_ratio": area_ratio,
                }
            )

        return detections
