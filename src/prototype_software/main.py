import cv2 as cv
from vision_detector import visionDetector
from picamera2 import Picamera2
import time

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(raw={"size":(1640,1232)},
                                                    main={"format":"RGB888","size":(1024,1024)}))
picam2.start()
time.sleep(2)

if __name__ == "__main__":
    
    while True:
        video = picam2.capture_array()
        vd = visionDetector(video)
        vd.detect_color()
        red_pos, green_pos, blue_pos = vd.detect()
        vd.show()
        if cv.waitKey(1) & 0xFF == ord("q"):
            break
    picam2.stop()
    picam2.close()