class ViolationEngine:
    """Определяет нарушения на основе данных о взгляде, голове и объектах."""

    def detect(self, data):
        """Принимает словарь с ключами "gaze", "mouth", "head", "objects" и возвращает список строк с описанием нарушений."""
        violations = []

        gaze_state = data.get("gaze")
        if gaze_state and gaze_state.value in ["left", "right"]:
            violations.append("Looking away")

        mouth_state = data.get("mouth")
        if mouth_state and mouth_state.value == "open":
            violations.append("Mouth open")

        head_state = data.get("head")
        if head_state and head_state.value in ["left", "right", "down", "up"]:
            violations.append(f"Head turned {head_state.value}")

        object_detections = [
            obj.get("state")
            for obj in data.get("objects", [])
            if obj.get("state")
        ]

        object_values = [obj.value for obj in object_detections]

        if any(value == "phone" for value in object_values):
            violations.append("Phone detected")

        if object_values.count("person") > 1:
            violations.append("Multiple persons detected")

        return violations
