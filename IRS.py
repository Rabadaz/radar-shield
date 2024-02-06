#!/usr/bin/python
import os
from queue import Queue
import threading
from cv2 import VideoCapture

from StateMachine import StateMachine
from OPS243Sensor import OPS243Sensor
from MatrixDisplay import MatrixDisplay
from ImagePrinter import ImagePrinter

printer = ImagePrinter()
sensor = OPS243Sensor(serial_port="/dev/ttyACM0")
display = MatrixDisplay()

image_threashold = 5 #km/h
high_score = 0
measurements = Queue()
state_machine = StateMachine()
run_high_score = 0

def read_sensor_to_buffer():
    while True:
        mm = sensor.readLatestValue()
        measurements.put(mm["speed"] * 3.6)

if __name__== "__main__":
    sensor.setup()

    if os.environ.get("PRINTER") is None:
        printer.enabled = False

    sensorThread = threading.Thread(target=read_sensor_to_buffer)
    sensorThread.start()
    sensorThread.join()

    while True:
        if state_machine.state == StateMachine.STATE.WAITING:
            if not measurements.empty():
                state_machine.switch(StateMachine.STATE.Detecting)
            run_high_score = 0

        elif state_machine.state == STATE.DETECTING:
            if measurements.empty():
                state_machine.switch(StateMachine.STATE.WAITING, min_switch_time_duration = 5)
                continue

            next_measurement = measurements.get()

            high_score = max(next_measurement, high_score)
            run_high_score = max(next_measurement, run_high_score)

            if next_measurement > image_threashold:
                state_machine.switch(state_machine.STATE.TRIGGERED)

        elif state_machine.state == state_machine.STATE.TRIGGERED:




        elif state_machine.state == state_machine.STATE.WAITING_FOR_PRINT_CONFIRM:


        else:
            print("Unknown State switching to WAITING")
            state_machine.switch(state_machine.STATE.WAITING)



        if measurements.empty():

        else:

        data = sensor.readLatestValue()
        speed = float(data["speed"])*3.6 # convert from m/s to km/h
        high_score = max(high_score, speed)
        current_time = time()
        if time - last_measurement > 1000:
            State = DETECTING



        if State == DETECTING:
            run_high_score = 0
            if speed >= image_threashhold:
                State = TRIGGERED
                run_high_score = speed



        elif State == TRIGGERED:


        else:





        if(speed >= image_threashold):
            cam = VideoCapture(0)
            s, img = cam.read()
            cam.release()
            printer.print(img)

        display.update(speed, high_score)


