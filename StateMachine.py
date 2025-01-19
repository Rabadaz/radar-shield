import time
from enum import Enum


class StateMachine:
    class STATE(Enum):
        WAITING = 0
        DETECTING = 1,
        TRIGGERED = 2,
        WAITING_FOR_PRINT_CONFIRM = 3

    def __init__(self, blynk_dev):
        self.state = self.STATE.WAITING
        self.last_switch = time.time()
        self.blynk_dev = blynk_dev

    def switch(self, state, min_switch_time_duration = 0):
        current_time = time.time()
        if (current_time - self.last_switch) < min_switch_time_duration:
            return False

        self.state = state
        self.last_switch = time.time()
        if state == self.STATE.WAITING:
            self.blynk_dev.set_state(self.STATE.DETECTING)
        else:
            self.blynk_dev.set_state(state)

        return True


