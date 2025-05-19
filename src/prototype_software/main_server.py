import cv2 as cv
from vision_detector import visionDetector
from picamera2 import Picamera2
import time
import threading
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

## GLOBAL VARIABLES
latest_red_pos = None
latest_green_pos = None
latest_blue_pos = None

## modified class for http server handler
class DetectionDataHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        if self.path =='/detection_data':
            self._set_headers()
            data = {
                'red_postion': latest_red_pos,
                'green_position': latest_green_pos,
                'blue_position': latest_blue_pos,
                'timestamp': time.time()
            }
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_response(404)
            self.end_headers()

def start_server(port=8765):
    server_address = ('', port)
    httpd = ThreadingHTTPServer(server_address, DetectionDataHandler)
    print (f'Starting server on port {port}')
    httpd.serve_forever()

def run_vision_detection():
    global latest_red_pos, latest_green_pos, latest_blue_pos

    picam2 =Picamera2()
    picam2.configure(picam2.create_preview_configuration(raw={"size":(1640,1232)},
                                                        main={"format":"RGB888","size":(1024,1024)}))

    picam2.start()
    time.sleep(2)

    try:
        while True:
            video = picam2.capture_array()
            vd = visionDetector(video)
            vd.detect_color()
            latest_red_pos, latest_green_pos, latest_blue_pos = vd.detect()
            vd.show()
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        picam2.stop()
        picam2.close()

if __name__ == "__main__":
    
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    run_vision_detection()