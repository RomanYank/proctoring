from ultralytics import YOLO
import cv2

class ObjectDetectionModel:
    def __init__(self, model_path="yolov11n.pt"):
        self.model = YOLO(model_path) 

    def detect_objects(self, frame):
        results = self.model(frame)
        annotated_frame = results[0].plot()

        person_count = 0

        for det in results[0].boxes:
            cls_id = int(det.cls[0].item())

            if det.conf[0].item() > 0.5:
                if cls_id == 0:
                    person_count += 1
                    if person_count > 1:
                        cv2.putText(annotated_frame, "More than one person detected!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        break 

                elif cls_id == 67:
                    cv2.putText(annotated_frame, "PHONE DETECTED!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                elif cls_id == 73:
                    cv2.putText(annotated_frame, "BOOK DETECTED!", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        return annotated_frame, results
