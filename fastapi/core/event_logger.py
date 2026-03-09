class EventLogger:

    def __init__(self):
        self.events = []

    def add(self, time, event):
        self.events.append({
            "time": time,
            "violation": event
        })

    def result(self):
        return self.events