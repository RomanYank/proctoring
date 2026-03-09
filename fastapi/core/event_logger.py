import base64
import re
from datetime import datetime
from pathlib import Path
import cv2

class EventLogger:
    """Сохраняет события нарушений и делает подпись на кадре."""

    def __init__(self, output_dir=None):
        self.events = []
        if output_dir is None:
            output_dir = Path(__file__).resolve().parents[1] / "data" / "violations"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._counter = 0
        self._last_second_by_event = {}

    def _safe_name(self, text):
        return re.sub(r"[^a-zA-Z0-9_-]+", "_", text).strip("_").lower() or "violation"

    def _apply_face_mask(self, frame, face_landmarks):
        """Возвращает копию кадра."""
        return frame

    def _build_screenshot(self, frame, event, event_time, face_landmarks):
        screenshot = self._apply_face_mask(frame, face_landmarks)
        cv2.putText(
            screenshot,
            f"{event_time} | {event}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
        return screenshot

    def _save_screenshot(self, frame, event, event_time, face_landmarks):
        self._counter += 1
        stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S%f")
        safe_event = self._safe_name(event)
        filename = f"{stamp}_{self._counter:05d}_{safe_event}.jpg"
        filepath = self.output_dir / filename

        screenshot = self._build_screenshot(frame, event, event_time, face_landmarks)
        cv2.imwrite(str(filepath), screenshot)

        ok, jpeg = cv2.imencode(".jpg", screenshot)
        image_log = base64.b64encode(jpeg).decode("ascii") if ok else ""
        return str(filepath), image_log

    def add(self, time, event, frame=None, face_landmarks=None, second_bucket=None):
        """Добавляет запись нарушения и отсекает дубликат того же типа в течение секунды."""
        if second_bucket is not None:
            if self._last_second_by_event.get(event) == second_bucket:
                return
            self._last_second_by_event[event] = second_bucket

        if frame is None:
            self.events.append(
                {
                    "time": time,
                    "violation": event,
                    "screenshot_path": "",
                    "img_log": "",
                }
            )
            return

        screenshot_path, image_log = self._save_screenshot(frame, event, time, face_landmarks)
        self.events.append(
            {
                "time": time,
                "violation": event,
                "screenshot_path": screenshot_path,
                "img_log": image_log,
            }
        )

    def result(self):
        return self.events
