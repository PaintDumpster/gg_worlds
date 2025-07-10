import requests
import base64
import os
import sys
import re

def sanitize_filename(text):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', text)

def generate_landmark_image(prompt, safe_name, steps=30, width=1024, height=1024):
    save_dir = r"..\landmarks_blender\spec_model"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{safe_name}.png")

    payload = {
        "prompt": prompt,
        "steps": steps,
        "width": width,
        "height": height
    }

    response = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", json=payload)

    if response.status_code == 200:
        result = response.json()
        if 'images' in result and len(result['images']) > 0:
            image_data = result['images'][0]
            base64_data = image_data.split(",", 1)[1] if "," in image_data else image_data
            image_bytes = base64.b64decode(base64_data)
            with open(save_path, "wb") as f:
                f.write(image_bytes)
            print(f"Image saved as {save_path}")
        else:
            print("No images returned by API.")
            if 'error' in result:
                print("API error message:", result['error'])
    else:
        print(f"API call failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        user_prompt = sys.argv[1]
        safe_name = sys.argv[2]
    else:
        user_prompt = input("Enter your landmark prompt: ")
        safe_name = sanitize_filename(user_prompt)

    generate_landmark_image(user_prompt, safe_name)
