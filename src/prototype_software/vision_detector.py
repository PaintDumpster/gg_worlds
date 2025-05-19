import cv2 as cv
import numpy as np
import time

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

        if mask is None:
            return None
        
        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            return None
        
        detections = []

        for i, cnt in enumerate(contours):
            area = cv.contourArea(cnt)
            if area > 1000:
                x,y,w,h = cv.boundingRect(cnt)
                cv.rectangle(self.camera_input, (x,y), (x+w,y+h), color, 3)
                cv.putText(self.camera_input, desc, (x,y-5), cv.FONT_HERSHEY_SIMPLEX, 1.5, color, 2)
                detections.append({
                    f"{desc} {i}":{
                        'x':x,
                        'y':y,
                        'w':w,
                        'h':h,
                        'center':{
                            'x': x + w // 2,
                            'y': y + h // 2
                        }
                    }
                })

        return detections if detections else None
    
    def draw_json(self, positions, color):
        for pos in positions:
            for key, value in pos.items():
                x = value['x']
                y = value['y']
                w = value['w']
                h = value['h']
                center_x = value['center']['x']
                center_y = value['center']['y']
                
                cv.putText(self.camera_input, f"{key}:({center_x}, {center_y})", (x, y - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    def detect(self):
        try:
            if self.r_mask is None or self.g_mask is None or self.b_mask is None:
                self.detect_color()

            red_pos = self.draw_contours(self.r_mask, "Red", (0, 0, 255))
            green_pos = self.draw_contours(self.g_mask, "Green", (0, 255, 0))
            blue_pos = self.draw_contours(self.b_mask, "Blue", (255, 0, 0))

            return red_pos, green_pos, blue_pos
        except Exception as e:
            print(f"Error in detect: {e}")
            return None, None, None

    def show(self):

        cv.imshow("Camera Input", self.camera_input)
