import subprocess
import os
import re

def sanitize_filename(text):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', text)

if __name__ == "__main__":
    prompt = input("Enter your landmark prompt: ")
    safe_name = sanitize_filename(prompt)
    output_dir = os.path.abspath(r"..\landmarks_blender\spec_model")

    os.makedirs(output_dir, exist_ok=True)

    # Run speculative.py with prompt and safe name
    print("\n--- Generating image ---")
    subprocess.run(["python", "speculative.py", prompt, safe_name], check=True)

    image_path = os.path.join(output_dir, f"{safe_name}.png")

    if os.path.exists(image_path):
        print(f"Image confirmed at {image_path}")
    else:
        print("Expected image not found. Aborting.")
        exit(1)

    # Path to example_elena.py
    trellis_script = os.path.abspath(
    r"C:\Users\user\Desktop\landmarks_studio\v27_py311_cu118_torch2.1.2\trellis-spz\code\example_elena.py"
)

    # Run example_elena.py with image path, base name, output dir
    print("\n--- Generating 3D model ---")
trellis_python = r"C:\Users\user\Desktop\landmarks_studio\v27_py311_cu118_torch2.1.2\trellis-spz\code\venv\Scripts\python.exe"

subprocess.run([
    trellis_python, trellis_script,
    image_path,
    safe_name,
    output_dir
], check=True)

