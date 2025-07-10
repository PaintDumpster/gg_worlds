import os
import sys
import imageio
from PIL import Image
from trellis.pipelines import TrellisImageTo3DPipeline
from trellis.utils import render_utils, postprocessing_utils

# === 0. System Setup ===
sys.path.append(os.getcwd())

os.environ['ATTN_BACKEND'] = 'xformers'
os.environ['SPCONV_ALGO'] = 'native'

# === 1. Parse Arguments ===
image_path = sys.argv[1] if len(sys.argv) >= 2 else "assets/example_image.jpg"
base_name = sys.argv[2] if len(sys.argv) >= 3 else "output"
output_dir = sys.argv[3] if len(sys.argv) >= 4 else "."

os.makedirs(output_dir, exist_ok=True)

# === 2. Load Image ===
try:
    image = Image.open(image_path).convert("RGB")
except Exception as e:
    print(f"[ERROR] Failed to open image at {image_path}: {e}")
    sys.exit(1)

# === 3. Initialize Pipeline ===
try:
    pipeline = TrellisImageTo3DPipeline.from_pretrained("JeffreyXiang/TRELLIS-image-large")
    pipeline.cuda()
except Exception as e:
    print(f"[ERROR] Failed to load pipeline: {e}")
    sys.exit(1)

# === 4. Run Pipeline ===
try:
    outputs = pipeline.run(image, seed=1)
except Exception as e:
    print(f"[ERROR] Pipeline run failed: {e}")
    sys.exit(1)

# === 5. Export GLB Model ===
try:
    glb = postprocessing_utils.to_glb(
        outputs['gaussian'][0],
        outputs['mesh'][0],
        simplify=0.95,
        texture_size=1024,
    )
    glb_output_path = os.path.join(output_dir, f"{base_name}.glb")
    glb.export(glb_output_path)
    print(f"[✓] Exported GLB to: {glb_output_path}")
except Exception as e:
    print(f"[ERROR] Failed to export GLB: {e}")

# === 6. Optional: Render Videos ===
# Uncomment below if needed

# try:
#     video = render_utils.render_video(outputs['gaussian'][0])['color']
#     imageio.mimsave(os.path.join(output_dir, f"{base_name}_gaussian.mp4"), video, fps=30)
#     print(f"Saved Gaussian video.")

#     video = render_utils.render_video(outputs['radiance_field'][0])['color']
#     imageio.mimsave(os.path.join(output_dir, f"{base_name}_rf.mp4"), video, fps=30)
#     print(f"Saved Radiance Field video.")

#     video = render_utils.render_video(outputs['mesh'][0])['normal']
#     imageio.mimsave(os.path.join(output_dir, f"{base_name}_mesh.mp4"), video, fps=30)
#     print(f"Saved Mesh video.")
# except Exception as e:
#     print(f"[WARN] Video rendering failed: {e}")
