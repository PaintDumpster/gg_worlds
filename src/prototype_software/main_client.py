import requests
import json
import time

raspi_ip = ''
PORT = 8765
URL = f'http://{raspi_ip}:{PORT}/detection_data'

def print_detection(detection_dict, color):
    if detection_dict is None:
        print(f'No {color} detected')
    else:
        print(f'\n{color} detections:')
        for item in detection_dict:
            for obj_name, details in item.items():
                print(f'{obj_name}:')
                print(f' center: {details['center']['x']}, {details['center']['y']}')
def main():
    print('Starting Client...')
    print(f"Connecting to {URL}")

    while True:
        try:
            response = requests.get(url=URL)
            if response.status_code == 200:
                data = response.json()

                print("\n"+"="*50)
                print(f"Timestamp: {time.ctime()}")
                print('='*50)

                print_detection(data['red_positions'], 'red')
                print_detection(data['green_positions'], 'green')
                print_detection(data['blue_positions'], 'blue')
            else:
                print(f'Error: {response.status_code}')
        except Exception as e:
            print(f'Error: {e}')
        
        time.sleep(1)

if __name__ == "__main__":
    main()