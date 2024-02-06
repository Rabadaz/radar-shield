import serial
import json
import sys


class OPS243Sensor(object):
    def __init__(self, serial_port="/dev/ttyACM1"):
        self.serial = serial.Serial(serial_port, 9600)
        self.enabled = True

    def setup(self, direction_filter="I", min_detection_speed=1,json_output=True):
        if not self.serial.is_open:
          sys.exit(-1)
        self.serial.write(b"OJ" if json_output else b"Oj")
        self.serial.readline()

        self.serial.write(b"R|")
        self.serial.readline()
        if direction_filter == "I":
            self.serial.write(b"R+")
            self.serial.readline()
        elif direction_filter == "O":
            self.serial.write(b"R-")
            self.serial.readline()
        self.serial.write(b"R>%d" % min_detection_speed)
        self.serial.readline()

    def readLatestValue(self):
        json_data = {"speed": 0.0}
        if self.serial.is_open:
            try:
                raw_data = self.serial.readline()
            except Exception:
                return json_data

            if not self.enabled:
                return {"speed":0.0}

            try:
                json_data = json.loads(raw_data)
                if isinstance(json_data, float):
                    json_data = {"speed": json_data}
            except ValueError as e:
                pass

            if "speed" not in json_data:
                return {"speed":0.0}

        return json_data



