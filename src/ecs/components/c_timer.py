class CTimer:
    def __init__(self, start_time: float, duration:float):
        self.start_time = start_time
        self.duration = duration
        self.finished = False