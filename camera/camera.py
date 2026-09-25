import cv2 as cv

class Camera:

    def __init__(self) -> None:
        self.camera = cv.VideoCapture(0)

    def read(self):
        ret, frame = self.camera.read()
        return ret, frame
    
    def stop(self):
        self.camera.release()
