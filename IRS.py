#!/usr/bin/python

import os
from multiprocessing import Queue
import threading
from time import sleep

from StateMachine import StateMachine
from OPS243Sensor import OPS243Sensor
from MatrixDisplay import MatrixDisplay
from ImagePrinter import ImagePrinter
from Camera import Camera
from blynk_device import BlynkDevice

printer = ImagePrinter()
sensor = OPS243Sensor(serial_port="/dev/ttyACM0")
display = MatrixDisplay()
camera = Camera()
blynk_dev = BlynkDevice()
state_machine = StateMachine(blynk_dev)

measurements = Queue()

image_threshold = 5  # km/h
run_high_score = 0
high_score = 0


def read_sensor_to_buffer():
    while True:
        mm = sensor.readLatestValue()
        if sensor.enabled:
            measurements.put(float(mm["speed"]) * 3.6)


def take_image():
    camera.take_image()


if __name__ == "__main__":
    sensor.setup()

    if os.environ.get("PRINTER") is None:
        printer.enabled = False

    sensorThread = threading.Thread(target=read_sensor_to_buffer)
    sensorThread.start()

    while True:
        print(measurements.qsize(), state_machine.state)
        if state_machine.state == StateMachine.STATE.WAITING:
            if not measurements.empty():
                state_machine.switch(StateMachine.STATE.DETECTING)
            run_high_score = 0
            sensor.enabled = True

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
                photo_thread = threading.Thread(target=take_image)
                photo_thread.start()

        elif state_machine.state == state_machine.STATE.TRIGGERED:
            if measurements.empty():
                state_machine.switch(state_machine.STATE.WAITING_FOR_PRINT_CONFIRM)

            next_measurement = measurements.get()
            high_score = max(next_measurement, high_score)
            run_high_score = max(next_measurement, run_high_score)

            display.display_measurement(next_measurement, run_high_score, beating_score=(run_high_score == next_measurement))

        elif state_machine.state == state_machine.STATE.WAITING_FOR_PRINT_CONFIRM:
            sensor.enabled = False
            # print if confirmed by blynk

            if blynk_dev.wait_for_print_response():
                while camera.in_progress:
                    sleep(0.1)
                printer.print(camera.image)
                state_machine.switch(StateMachine.STATE.WAITING)
                display.display_print_message(run_high_score)
                sleep(10)
        else:
            print("Unknown State switching to WAITING")
            state_machine.switch(state_machine.STATE.WAITING)
