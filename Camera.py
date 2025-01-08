from cv2 import VideoCapture


class Camera:
    def __init__(self):
        self.image = None
        self.capture = VideoCapture(0)

    def take_image(self):
        cam = VideoCapture(0)
        s, img = cam.read()
        if s:
            self.image = img
        cam.release()
        return s
