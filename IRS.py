#!/usr/bin/python

import os
import random
from multiprocessing import Queue
from time import sleep
import threading


from StateMachine import StateMachine
from OPS243Sensor import OPS243Sensor
from MatrixDisplay import MatrixDisplay
from ImagePrinter import ImagePrinter
from Camera import Camera

printer = ImagePrinter()
sensor = OPS243Sensor(serial_port="/dev/ttyACM0")
display = MatrixDisplay()
camera = Camera()

image_threshold = 5  # km/h
high_score = 0
measurements = Queue()
state_machine = StateMachine()
run_high_score = 0


def read_sensor_to_buffer():
    while True:
        mm = sensor.readLatestValue()
        measurements.put(float(mm["speed"]) * 3.6)


if __name__ == "__main__":
    sensor.setup()

    if os.environ.get("PRINTER") is None:
        printer.enabled = False

    sensorThread = threading.Thread(target=read_sensor_to_buffer)
    sensorThread.start()

    while True:
        print(state_machine.state, measurements.qsize())
        if state_machine.state == StateMachine.STATE.WAITING:
            if not measurements.empty():
                state_machine.switch(StateMachine.STATE.DETECTING)
            run_high_score = 0

            display.display_high_score(high_score)

        elif state_machine.state == state_machine.STATE.DETECTING:
            if measurements.empty():
                state_machine.switch(StateMachine.STATE.WAITING, min_switch_time_duration=5)
                continue

            next_measurement = measurements.get()
            high_score = max(next_measurement, high_score)
            run_high_score = max(next_measurement, run_high_score)

            display.display_measurement(next_measurement, run_high_score, beating_score=(run_high_score == next_measurement))

            if next_measurement > image_threshold:
                state_machine.switch(state_machine.STATE.TRIGGERED)
                camera.take_image()

        elif state_machine.state == state_machine.STATE.TRIGGERED:
            if measurements.empty():
                state_machine.switch(state_machine.STATE.WAITING_FOR_PRINT_CONFIRM)

            next_measurement = measurements.get()
            high_score = max(next_measurement, high_score)
            run_high_score = max(next_measurement, run_high_score)

            display.display_measurement(next_measurement, run_high_score, beating_score=(run_high_score == next_measurement))

        elif state_machine.state == state_machine.STATE.WAITING_FOR_PRINT_CONFIRM:
            # print if confirmed by blynk
            if random.randint(0, 1000) < 5:
                printer.print(camera.image)
                state_machine.switch(StateMachine.STATE.WAITING)

            display.display_print_message(run_high_score)
            state_machine.switch(StateMachine.STATE.WAITING, min_switch_time_duration=60)

        else:
            print("Unknown State switching to WAITING")
            state_machine.switch(state_machine.STATE.WAITING)
