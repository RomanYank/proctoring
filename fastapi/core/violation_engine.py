class ViolationEngine:
    """Builds violations from gaze, head pose, mouth state and detected objects."""

    def detect(self, data):
        violations = []

        gaze_state = data.get("gaze")
        head_state = data.get("head")
        if gaze_state and gaze_state.value in ["left", "right"] and head_state and head_state.value == "forward":
            violations.append("Looking away")

        mouth_state = data.get("mouth")
        if mouth_state and mouth_state.value == "open":
            violations.append("Mouth open")

        if head_state and head_state.value in ["left", "right", "down", "up"]:
            violations.append(f"Head turned {head_state.value}")

        object_detections = [obj for obj in data.get("objects", []) if obj.get("state")]
        object_values = [obj["state"].value for obj in object_detections]
        person_detections = [obj for obj in object_detections if obj["state"].value == "person"]

        if any(value == "phone" for value in object_values):
            violations.append("Phone detected")

        if len(person_detections) > 1:
            violations.append("Multiple persons detected")

        return violations
