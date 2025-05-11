import cv2 as cv
import numpy as np

class visionDetector:
    def __init__(self, camera_input=None):
        self.camera_input = camera_input
    def crop_image(self):
        