import serial
import json
import sys

class OPS243Sensor(object):

    def __init__(self, serial_port="/dev/ttyACM1"):
        self.serial = serial.Serial(serial_port, 9600)

    def setup(self, directionFilter="I", minDetectionSpeed=1,jsonOutput=True):
        if not self.serial.is_open:
          sys.exit(-1)
        self.serial.write(b"OJ" if jsonOutput else b"Oj")
        self.serial.readline()

        self.serial.write(b"R|")
        self.serial.readline()
        if directionFilter == "I":
            self.serial.write(b"R+")
            self.serial.readline()
        elif directionFilter=="O":
            self.serial.write(b"R-")
            self.serial.readline()
        self.serial.write(b"R>%d"%minDetectionSpeed)
        self.serial.readline()





    def readLatestValue(self):
        json_data = {"speed":0.0}
        if self.serial.is_open:
            try:
                raw_data = self.serial.readline()
            except Exception as e:
                return json_data
            try:
                json_data = json.loads(raw_data)
                if isinstance(json_data, float):
                    json_data = {"speed":json_data}
            except ValueError as e:
               pass
        return json_data;



