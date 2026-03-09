class ViolationEngine:
    def __init__(
        self,
        looking_away_frames=3,
        multiple_person_frames=3,
        extra_person_confidence=0.8,
        extra_person_area_ratio=0.12,
    ):
        self.looking_away_frames = looking_away_frames
        self.multiple_person_frames = multiple_person_frames
        self.extra_person_confidence = extra_person_confidence
        self.extra_person_area_ratio = extra_person_area_ratio
        self._streaks = {
            "looking_away": 0,
            "multiple_persons": 0,
        }
        self._emitted = {
            "looking_away": False,
            "multiple_persons": False,
        }

    def _update_streak(self, key, active, threshold):
        if active:
            self._streaks[key] += 1
        else:
            self._streaks[key] = 0
            self._emitted[key] = False
            return False

        if self._streaks[key] >= threshold and not self._emitted[key]:
            self._emitted[key] = True
            return True

        return False

    def _is_valid_extra_person(self, detection):
        confidence = float(detection.get("confidence", 0.0))
        area_ratio = float(detection.get("area_ratio", 0.0))
        x1, y1, x2, y2 = detection.get("bbox", (0, 0, 0, 0))
        width = max(x2 - x1, 0)
        height = max(y2 - y1, 0)
        if height <= 0 or width <= 0:
            return False

        aspect_ratio = width / height
        return (
            confidence >= self.extra_person_confidence
            and area_ratio >= self.extra_person_area_ratio
            and 0.2 <= aspect_ratio <= 0.9
        )

    def detect(self, data):
        violations = []

        gaze_state = data.get("gaze")
        head_state = data.get("head")
        looking_away_active = (
            gaze_state is not None
            and gaze_state.value in ["left", "right"]
            and head_state is not None
            and head_state.value == "forward"
        )
        if self._update_streak("looking_away", looking_away_active, self.looking_away_frames):
            violations.append("Looking away")

        mouth_state = data.get("mouth")
        if mouth_state and mouth_state.value == "open":
            violations.append("Mouth open")

        if head_state and head_state.value in ["left", "right", "down", "up"]:
            violations.append(f"Head turned {head_state.value}")

        object_detections = [obj for obj in data.get("objects", []) if obj.get("state")]
        object_values = [obj["state"].value for obj in object_detections]
        person_detections = [
            obj for obj in object_detections
            if obj["state"].value == "person" and self._is_valid_extra_person(obj)
        ]

        if any(value == "phone" for value in object_values):
            violations.append("Phone detected")

        multiple_persons_active = len(person_detections) > 1
        if self._update_streak("multiple_persons", multiple_persons_active, self.multiple_person_frames):
            violations.append("Multiple persons detected")

        return violations
