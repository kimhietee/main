import time

class IntervalExecutor:
    def __init__(self, interval_seconds):
        self.interval = interval_seconds
        self.last_time = time.time()

    def should_run(self):
        current_time = time.time()
        if current_time - self.last_time >= self.interval:
            self.last_time = current_time
            return True
        return False
    

# self.print_timer = IntervalExecutor(1)

# if self.print_timer.should_run():
#     print("Bot state:", self.state)