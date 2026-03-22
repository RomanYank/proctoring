import cv2
import argparse
from pathlib import Path
from detectors.face_pipeline import FacePipeline
try:
    from detectors.gaze_detector import GazeDetector
    GAZE_AVAILABLE = True
except ImportError:
    GAZE_AVAILABLE = False
    print("Gaze detector not available (dlib not installed)")
from detectors.object_detector import ObjectDetector
from core.frame_processor import FrameProcessor
from models.states import MouthState, HeadState, GazeState

def main(mouth_threshold=0.25, mouth_window=5, camera_index=0):
    # Инициализация моделей
    base_dir = Path(__file__).resolve().parent
    face_model = base_dir / "models" / "face_landmarker.task"
    yolo_model = base_dir / "yolov8n.pt"

    # Создаем FacePipeline с настраиваемыми параметрами
    from detectors.face_landmarker import FaceLandmarkDetector
    from detectors.head_pose import HeadPoseDetector
    from detectors.mouth_detector import MouthStateDetector

    landmarks_detector = FaceLandmarkDetector(str(face_model))
    mouth_detector = MouthStateDetector(threshold=mouth_threshold, window=mouth_window)
    head_pose_detector = HeadPoseDetector()

    class CustomFacePipeline:
        def __init__(self, landmarks, mouth, head_pose):
            self.landmarks = landmarks
            self.mouth = mouth
            self.head_pose = head_pose
            self.timestamp = 0

        def process(self, frame):
            result = self.landmarks.detect(frame, self.timestamp)
            self.timestamp += 1

            if not result.face_landmarks:
                return None

            landmarks = result.face_landmarks[0]
            mouth_state = self.mouth.detect(landmarks)
            head_state = self.head_pose.detect(landmarks)

            return {
                "mouth": mouth_state,
                "head": head_state,
                "face_landmarks": landmarks,
            }

    face_pipeline = CustomFacePipeline(landmarks_detector, mouth_detector, head_pose_detector)
    if GAZE_AVAILABLE:
        gaze_detector = GazeDetector()
    else:
        class DummyGazeDetector:
            def detect(self, frame):
                return None
        gaze_detector = DummyGazeDetector()
    object_detector = ObjectDetector(str(yolo_model))
    processor = FrameProcessor(face_pipeline, gaze_detector, object_detector)

    # Захват с веб-камеры
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Не удалось открыть веб-камеру с индексом {camera_index}. Попробуйте другой индекс (0, 1, 2...)")
        return

    print("Нажмите 'q' для выхода")
    print(f"Параметры: mouth_threshold={mouth_threshold}, mouth_window={mouth_window}, camera_index={camera_index}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Обработка кадра
        data = processor.process(frame)

        # Отображение результатов на кадре
        display_text = []
        if data["mouth"]:
            display_text.append(f"Mouth: {data['mouth'].value}")
        if data["head"]:
            display_text.append(f"Head: {data['head'].value}")
        if data["gaze"]:
            display_text.append(f"Gaze: {data['gaze'].value}")
        if data["objects"]:
            objects_str = ", ".join([obj["label"] for obj in data["objects"]])
            display_text.append(f"Objects: {objects_str}")

        # Рисуем текст на кадре
        y_offset = 30
        for text in display_text:
            cv2.putText(frame, text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            y_offset += 30

        # Показываем кадр
        cv2.imshow('Real-time Behavior Analysis', frame)

        # Выход по 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-time camera behavior analysis for tuning")
    parser.add_argument("--mouth_threshold", type=float, default=0.25, help="Threshold for mouth open detection")
    parser.add_argument("--mouth_window", type=int, default=5, help="Window size for mouth state smoothing")
    parser.add_argument("--camera_index", type=int, default=0, help="Camera index (0, 1, 2...)")

    args = parser.parse_args()
    main(mouth_threshold=args.mouth_threshold, mouth_window=args.mouth_window, camera_index=args.camera_index)