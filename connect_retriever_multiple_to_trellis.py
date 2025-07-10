import subprocess
import os
import shutil
import sys

# === 0. Define prompts ===
# Either pass via command-line or define here
prompts = sys.argv[1:] if len(sys.argv) > 1 else [
   "japanese temple" ,
   "eiffel tower"
]

# === 1. Set script paths ===
retriever_script = os.path.normpath("photo_retrieval_multiple.py")
trellis_script = os.path.normpath("example_multi_image_elena.py")

# === 2. Set Python interpreters ===
retriever_python = r"C:\Users\user\anaconda3\envs\retrieval\python.exe"
trellis_python = r"C:\Users\user\Desktop\landmarks_studio\v27_py311_cu118_torch2.1.2\trellis-spz\code\venv\Scripts\python.exe"

# === 3. Set output/input folders ===
trellis_input_dir = os.path.normpath(
    "C:/Users/user/Desktop/landmarks_studio/v27_py311_cu118_torch2.1.2/trellis-spz/code/assets/example_multi_image/shuffled"
)
os.makedirs(trellis_input_dir, exist_ok=True)

# === 4. Run the photo retriever script with prompts ===
print("\n--- Running photo retrieval ---")
subprocess.run([retriever_python, retriever_script] + prompts, check=True)

# === 5. Move output images to Trellis input ===
print("\n--- Moving images to Trellis ---")
for idx, fname in enumerate(sorted(os.listdir("."))):
    if fname.startswith("test_image_") and fname.endswith(".jpg"):
        new_name = f"IMG_AUTO_{idx}.jpg"
        src_path = os.path.join(".", fname)
        dst_path = os.path.join(trellis_input_dir, new_name)
        shutil.move(src_path, dst_path)
        print(f"Moved: {fname} → {new_name}")

# === 6. Run the Trellis pipeline ===
# Use first prompt as base for naming
main_prompt = "_".join(prompts).replace(" ", "_")

print("\n--- Running Trellis ---")
subprocess.run(
    [trellis_python, trellis_script, main_prompt],
    check=True,
    cwd=r"C:\Users\user\Desktop\landmarks_studio\v27_py311_cu118_torch2.1.2\trellis-spz\code"
)
