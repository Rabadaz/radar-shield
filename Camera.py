from cv2 import VideoCapture


class Camera:
    def __init__(self):
        self.image = None

    def take_image(self):
        cam = VideoCapture(-1)
        s, img = cam.read()
        if s:
            self.image = img
        cam.release()
        return s
