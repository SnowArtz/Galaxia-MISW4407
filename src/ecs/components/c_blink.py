class CBlink:
    def __init__(self, blink_rate, next_blink_time):
        self.blink_rate = blink_rate
        self.next_blink_time = next_blink_time
        self.visible = True