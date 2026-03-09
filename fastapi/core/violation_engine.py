class ViolationEngine:

    def detect(self, data):
        violations = []

        if "gaze" in data and data["gaze"].value in ["left", "right"]:
            violations.append("Looking away")

        if "mouth" in data and data["mouth"].value == "open":
            violations.append("Talking")

        if data.get("head") and data["head"].value in ["left", "right", "down", "up"]:
            violations.append(f"Head turned {data['head'].value}")
            
        if "objects" in data:

            objects = [o.value for o in data["objects"]]

            if "phone" in objects:
                violations.append("Phone detected")

            if objects.count("person") > 1:
                violations.append("Multiple persons detected")

        return violations