import base64
import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
import cv2

logger = logging.getLogger(__name__)
class EventLogger:
    def __init__(self, output_dir=None, session_name=None, duplicate_cooldown_seconds=8):
        self.events = []
        if output_dir is None:
            output_dir = Path(__file__).resolve().parents[1] / "data" / "violations"

        base_output_dir = Path(output_dir)
        base_output_dir.mkdir(parents=True, exist_ok=True)

        safe_session = self._safe_name(session_name or "session")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        self.output_dir = base_output_dir / f"{stamp}_{safe_session}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.events_path = self.output_dir / "events.json"
        self._counter = 0
        self._last_second_by_event = {}
        self.duplicate_cooldown_seconds = duplicate_cooldown_seconds

    def _safe_name(self, text):
        return re.sub(r"[^a-zA-Z0-9_-]+", "_", text).strip("_").lower() or "violation"

    def _apply_face_mask(self, frame, face_landmarks):
        return frame.copy()

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
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
        safe_event = self._safe_name(event)
        filename = f"{stamp}_{self._counter:05d}_{safe_event}.jpg"
        filepath = self.output_dir / filename

        screenshot = self._build_screenshot(frame, event, event_time, face_landmarks)
        saved = cv2.imwrite(str(filepath), screenshot)
        if not saved:
            logger.error("Failed to write screenshot: %s", filepath)
            filepath_str = ""
        else:
            filepath_str = str(filepath)

        ok, jpeg = cv2.imencode(".jpg", screenshot)
        image_log = base64.b64encode(jpeg).decode("ascii") if ok else ""
        return filepath_str, image_log

    def _build_event(self, time, event, screenshot_path, image_log):
        return {
            "time": time,
            "violation": event,
            "screenshot_path": screenshot_path,
            "img_log": image_log,
        }

    def _persist(self):
        self.events_path.write_text(
            json.dumps(self.events, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def add(self, time, event, frame=None, face_landmarks=None, second_bucket=None):
        if second_bucket is not None:
            last_second = self._last_second_by_event.get(event)
            if last_second is not None and second_bucket - last_second < self.duplicate_cooldown_seconds:
                return
            self._last_second_by_event[event] = second_bucket

        if frame is None:
            self.events.append(self._build_event(time, event, "", ""))
            self._persist()
            return

        screenshot_path, image_log = self._save_screenshot(frame, event, time, face_landmarks)
        self.events.append(self._build_event(time, event, screenshot_path, image_log))
        self._persist()

    def result(self):
        self._persist()
        return self.events
