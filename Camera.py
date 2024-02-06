from cv2 import VideoCapture


class Camera:
    def __init__(self):
        self.image = None
        self.in_progress = False

    def take_image(self):
        self.in_progress = True
        cam = VideoCapture(0)
        s, img = cam.read()
        if s:
            self.image = img
        cam.release()
        self.in_progress = False
        return s
