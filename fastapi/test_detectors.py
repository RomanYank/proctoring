#!/usr/bin/env python3
"""
Скрипт для тестирования детекторов прокторинга
"""
import sys
import os
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent))

import cv2
import numpy as np
from core.frame_processor import FrameProcessor
from core.violation_engine import ViolationEngine
from detectors.face_pipeline import FacePipeline
from detectors.gaze_detector import GazeDetector
from detectors.object_detector import ObjectDetector

def test_detectors():
    print("Тестирование детекторов прокторинга...")

    # Создаем тестовый кадр
    test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    # Добавляем белый прямоугольник в центре (имитация лица)
    cv2.rectangle(test_frame, (200, 150), (440, 330), (255, 255, 255), -1)

    try:
        # Инициализируем детекторы
        base_dir = Path(__file__).resolve().parent
        face_model = base_dir / "models" / "face_landmarker.task"
        yolo_model = base_dir / "yolov8n.pt"

        print(f"Модель лица: {face_model.exists()}")
        print(f"Модель YOLO: {yolo_model.exists()}")

        face = FacePipeline(str(face_model))
        gaze = GazeDetector()
        obj = ObjectDetector(str(yolo_model))
        processor = FrameProcessor(face, gaze, obj)
        engine = ViolationEngine()

        print("Обрабатываем тестовый кадр...")
        data = processor.process(test_frame)
        events = engine.detect(data)

        print("Результаты:")
        print(f"  Взгляд: {data.get('gaze')}")
        print(f"  Голова: {data.get('head')}")
        print(f"  Рот: {data.get('mouth')}")
        print(f"  Объекты: {len(data.get('objects', []))}")
        print(f"  Нарушения: {events}")

        return True

    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_detectors()
    sys.exit(0 if success else 1)