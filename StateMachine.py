import time
from enum import Enum

class StateMachine:
    class STATE(Enum):
        WAITING = 0
        DETECTING = 1,
        TRIGGERED = 2,
        WAITING_FOR_PRINT_CONFIRM = 3


    def __init__(self):
        self.state = self.STATE.WAITING
        self.last_switch = time.time()

    def switch(self, state, min_switch_time_duration = 0):
        current_time = time.time()
        if (current_time - self.last_switch) < min_switch_time_duration:
            return False

        self.state = state
        self.last_switch = time.time()
        return True


