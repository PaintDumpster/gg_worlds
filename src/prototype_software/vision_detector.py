import cv2 as cv
import numpy as np

class visionDetector:
    def __init__(self, camera_input=None):
		
        self.camera_input = camera_input
        
        self.colors = None
        
        self.r_mask = None
        self.g_mask = None
        self.b_mask = None
        
    def morphops(self, mask):
        pass
        
    def detect_color(self, color_name="red"):
        self.colors = {
            'red': {
                'lower1': np.array([0, 100, 100]),
                'upper1': np.array([10, 255, 255]),
                'lower2': np.array([160, 100, 100]),
                'upper2': np.array([179, 255, 255])
            },
            'blue': {
                'lower': np.array([100, 100, 100]),
                'upper': np.array([130, 255, 255])
            },
            'green': {
                'lower': np.array([40, 100, 100]),
                'upper': np.array([80, 255, 255])
            }
        }
        hsv = cv.cvtColor(self.camera_input, cv.COLOR_BGR2HSV)
        
        red_mask1 = cv.inRange(hsv,
        self.colors['red']['lower1'],
        self.colors['red']['upper1'])
        
        red_mask2 = cv.inRange(hsv, 
        self.colors['red']['lower2'],
        self.colors['red']['upper2'])
        
        self.r_mask = red_mask1 | red_mask2
        
        self.g_mask = cv.inRange(hsv, 
        self.colors['green']['lower'],
        self.colors['green']['upper'])
        
        self.b_mask = cv.inRange(hsv, 
        self.colors['blue']['lower'],
        self.colors['blue']['upper'])
        
        
    def draw_contours(self,mask,desc,color):
        cv.imshow('hsv_format',self.r_mask)
        
