import cups
import cv2
from tempfile import mkstemp
from time import sleep, time

class ImagePrinter:

    def __init__(self, base_path = "./ImageStore"):
        self.conn = cups.Connection()
        self.printer_name = "Canon_SELPHY_CP1500"
        cups.setUser('pi')
        self.base_path = base_path
        self.enabled = True

    def print(self, img):

        if self.enabled:
            file_path = self.base_path + "/" + str(int(time())) + ".png"
            cv2.imwrite(file_path, img)
            job_id = self.conn.printFile(self.printer_name, file_path, "radar-shield", {})
            while self.conn.getJobs().get(job_id, None):
                sleep(1)
        else:
            print("Printing is disabled")
            sleep(100)
