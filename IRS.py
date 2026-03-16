#!/usr/bin/python

import time
from multiprocessing import Queue
import threading

from StateMachine import StateMachine
from OPS243Sensor import OPS243Sensor
from MatrixDisplay import MatrixDisplay

sensor = OPS243Sensor(serial_port="/dev/ttyACM0")
display = MatrixDisplay()
state_machine = StateMachine()

measurements = Queue()

run_high_score = 0
last_run_high_score = 0
high_score = 0
smoothed_speed = 0.0
EMA_ALPHA = 0.1  # lower = more smoothing
POST_RUN_DISPLAY_DURATION = 15  # seconds to show run result before switching to overall high score


def read_sensor_to_buffer():
    while True:
        mm = sensor.readLatestValue()
        if sensor.enabled:
            speed = float(mm["speed"]) * 3.6
            smoothed_speed = EMA_ALPHA * speed + (1 - EMA_ALPHA) * smoothed_speed
            if smoothed_speed > 2:
                measurements.put( smoothed_speed)


if __name__ == "__main__":
    sensor.setup()

    sensorThread = threading.Thread(target=read_sensor_to_buffer)
    sensorThread.start()

    while True:
        print(measurements.qsize(), state_machine.state)
        if state_machine.state == StateMachine.STATE.WAITING:
            if not measurements.empty():
                state_machine.switch(StateMachine.STATE.DETECTING)
            run_high_score = 0
            smoothed_speed = 0.0
            sensor.enabled = True

            if time.time() - state_machine.last_switch < POST_RUN_DISPLAY_DURATION:
                display.display_high_score(last_run_high_score)
            else:
                display.display_high_score(high_score)

        elif state_machine.state == state_machine.STATE.DETECTING:
            if measurements.empty():
                last_run_high_score = run_high_score
                state_machine.switch(StateMachine.STATE.WAITING, min_switch_time_duration=5)
                continue

            next_measurement = measurements.get()
            high_score = max(next_measurement, high_score)
            run_high_score = max(next_measurement, run_high_score)

            display.display_measurement(next_measurement, run_high_score)

        else:
            print("Unknown State switching to WAITING")
            state_machine.switch(state_machine.STATE.WAITING)
