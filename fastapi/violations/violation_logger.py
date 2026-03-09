class ViolationLogger:
    def __init__(self, cooldown=2):
        self.last_time = {}
        self.cooldown = cooldown

    def log(self, violations, time_str, key, message):
        last = self.last_time.get(key)

        if last == time_str:
            return

        violations.append({
            "time": time_str,
            "violation": message
        })

        self.last_time[key] = time_str