class CCooldown:
    def __init__(self, cooldown_time:float):
        self.cooldown_time = cooldown_time
        self.current_time = cooldown_time
        self.cooldown_finished = False