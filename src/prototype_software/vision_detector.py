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

        largest_cotour = max(contours, key=cv.contourArea)
        area = cv.contourArea(largest_cotour)

        if area > 1000:
            x,y,w,h = cv.boundingRect(largest_cotour)
            cv.rectangle(self.camera_input,(x,y), (x+w,y+h), color, 2)
            cv.putText(self.camera_input, desc, (x,y-5), cv.FONT_HERSHEY_SIMPLEX, 1.5, color, 2)

            detection = {
                'x': x,
                'y': y,
                'w': w,
                'h': h,
                'center': {
                    'x': x+w//2,
                    'y': y+h//2
                }
            }

            cv.putText(self.camera_input,
                    f"({detection['center']['x']}, {detection['center']['y']})",
                    (x,y+h+25),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    1)
            return detection
        return None

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
class QRCodeDetector(visionDetector):
    def __init__(self, camera_input=None):
        super().__init__(camera_input)
        self.qr_detector = cv.QRCodeDetector()
        
        # Stabilization parameters
        self.last_qr_content = None
        self.last_qr_points = None
        self.detection_history = []
        self.history_max_size = 5
        self.confidence_threshold = 3  # Number of consecutive detections needed
        self.last_detection_time = 0
        self.persistence_time = 1.0  # seconds to keep displaying a QR after losing track
    
    def detect_qr(self):
        """Detects QR codes in the camera input and returns their content with stabilization"""
        if self.camera_input is None or not isinstance(self.camera_input, np.ndarray):
            return None, None, None
            
        current_time = time.time()
        try:
            # Make a copy of the image to avoid modifying the original
            frame = self.camera_input.copy()
            
            # Image preprocessing for better detection
            # 1. Apply Gaussian blur to reduce noise
            blurred = cv.GaussianBlur(frame, (5, 5), 0)
            
            # 2. Enhance contrast
            lab = cv.cvtColor(blurred, cv.COLOR_BGR2LAB)
            l, a, b = cv.split(lab)
            clahe = cv.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            enhanced = cv.merge((cl, a, b))
            enhanced = cv.cvtColor(enhanced, cv.COLOR_LAB2BGR)
            
            # Detect QR code with enhanced image
            qr_content, points, straight_qrcode = self.qr_detector.detectAndDecode(enhanced)
            
            # Apply temporal filtering and stabilization
            if points is not None and qr_content:
                # We have a new detection
                self.detection_history.append(qr_content)
                self.last_detection_time = current_time
                
                # Keep history at max size
                if len(self.detection_history) > self.history_max_size:
                    self.detection_history.pop(0)
                
                # Check if we have stable detection
                if self.is_stable_detection():
                    self.last_qr_content = qr_content
                    self.last_qr_points = points.astype(np.int32)
            else:
                # No detection in current frame
                # Check if we should keep displaying the last detection
                if current_time - self.last_detection_time > self.persistence_time:
                    # Reset if too much time passed
                    if len(self.detection_history) > 0:
                        self.detection_history.pop(0)
                    
                    if len(self.detection_history) == 0:
                        self.last_qr_content = None
                        self.last_qr_points = None
            
            # Draw the QR code if we have a stable detection
            if self.last_qr_content is not None and self.last_qr_points is not None:
                # Draw boundary around QR code
                for i in range(len(self.last_qr_points[0])):
                    cv.line(self.camera_input, 
                           tuple(self.last_qr_points[0][i]), 
                           tuple(self.last_qr_points[0][(i+1) % len(self.last_qr_points[0])]), 
                           (0, 255, 0), 
                           2)
                
                # Calculate center of QR code for text placement
                center_x = int(np.mean(self.last_qr_points[0][:, 0]))
                center_y = int(np.mean(self.last_qr_points[0][:, 1]))
                
                # Display QR code content
                cv.putText(self.camera_input, 
                          self.last_qr_content, 
                          (center_x, center_y - 20), 
                          cv.FONT_HERSHEY_SIMPLEX, 
                          0.8, 
                          (0, 0, 255), 
                          2)
                
            return self.last_qr_content, self.last_qr_points, straight_qrcode
            
        except Exception as e:
            print(f"Error in QR detection: {e}")
            return self.last_qr_content, self.last_qr_points, None
    
    def is_stable_detection(self):
        """Check if the detection is stable by looking at recent history"""
        if len(self.detection_history) < self.confidence_threshold:
            return False
            
        # Check if we have enough of the same detection
        recent_detections = self.detection_history[-self.confidence_threshold:]
        most_common = max(set(recent_detections), key=recent_detections.count)
        count = recent_detections.count(most_common)
        
        return count >= self.confidence_threshold - 1  # Allow one mismatch for robustness