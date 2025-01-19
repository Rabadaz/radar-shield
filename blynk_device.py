import BlynkLib
import os
from dotenv import load_dotenv

#Blynk Credentials
load_dotenv()
BLYNK_AUTH = os.getenv("BLYNK_AUTH")
TARGET_AUTH = os.getenv("TARGET_AUTH")


class PrintResponse:
    WAITING_FOR_RESPONSE = 0
    PRINT = 1
    DONOT_PRINT = 2


class BlynkDevice:
    def __init__(self):
        self.response = PrintResponse.WAITING_FOR_RESPONSE
        self.blynk = BlynkLib.Blynk(BLYNK_AUTH,server="blynk.cloud", port=80)
        self.blynk.on("V0", self.v0_read_handler)
        self.blynk.on("V1", self.v1_read_handler)
     
    def v0_read_handler(self, value):
        if value[0] == "1":
            self.response = PrintResponse.DONOT_PRINT

    def v1_read_handler(self, value):
        if value[0] == "1":
            self.response = PrintResponse.PRINT

    def run(self):
        self.blynk.run()

    def set_state(self, state):
        self.blynk.virtual_write(11, state)

    def wait_for_print_response(self):
        while self.response == PrintResponse.WAITING_FOR_RESPONSE:
            self.run()

        response = self.response
        self.response = PrintResponse.WAITING_FOR_RESPONSE
        return response
