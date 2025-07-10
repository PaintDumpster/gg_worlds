import os
import sys
import numpy as np
import imageio
from PIL import Image
from trellis.pipelines import TrellisImageTo3DPipeline
from trellis.utils import render_utils, postprocessing_utils

# === 0. Parse prompt argument for output naming ===
prompt = sys.argv[1] if len(sys.argv) > 1 else "default_prompt"
safe_prompt = "".join(c if c.isalnum() or c in ['_', '-'] else '_' for c in prompt)

# === 1. Environment and setup ===
sys.path.append(os.getcwd())
os.environ['ATTN_BACKEND'] = 'xformers'
os.environ['SPCONV_ALGO'] = 'native'

# === 2. Define paths ===
image_folder = os.path.abspath("assets/example_multi_image/shuffled")
output_glb_path = os.path.abspath(f"../landmarks_blender/p1model/{safe_prompt}.glb")
output_ply_path = os.path.abspath(f"./{safe_prompt}_gaussian.ply")
output_video_path = os.path.abspath(f"./{safe_prompt}_composite.mp4")

# === 3. Load pipeline ===
try:
    pipeline = TrellisImageTo3DPipeline.from_pretrained("JeffreyXiang/TRELLIS-image-large")
    pipeline.cuda()
except Exception as e:
    print(f"[ERROR] Failed to initialize pipeline: {e}")
    sys.exit(1)

# === 4. Load images ===
images = []
for fname in sorted(os.listdir(image_folder)):
    if fname.lower().endswith(".jpg"):
        img_path = os.path.join(image_folder, fname)
        try:
            images.append(Image.open(img_path).convert("RGB"))
        except Exception as e:
            print(f"[WARN] Could not open image {fname}: {e}")

if not images:
    print("[ERROR] No valid images found.")
    sys.exit(1)

print(f"[✓] Loaded {len(images)} images from {image_folder}")

# === 5. Run multi-image pipeline ===
try:
    outputs = pipeline.run_multi_image(
        images,
        seed=1,
        sparse_structure_sampler_params={"steps": 12, "cfg_strength": 7.5},
        slat_sampler_params={"steps": 12, "cfg_strength": 3},
    )
except Exception as e:
    print(f"[ERROR] Pipeline failed: {e}")
    sys.exit(1)

# === 6. Render and save composite video ===
try:
    video_gs = render_utils.render_video(outputs['gaussian'][0])['color']
    video_mesh = render_utils.render_video(outputs['mesh'][0])['normal']
    composite_video = [np.concatenate([f1, f2], axis=1) for f1, f2 in zip(video_gs, video_mesh)]
    imageio.mimsave(output_video_path, composite_video, fps=30)
    print(f"[✓] Saved composite video to: {output_video_path}")
except Exception as e:
    print(f"[WARN] Failed to render video: {e}")

# === 7. Export GLB ===
try:
    glb = postprocessing_utils.to_glb(
        outputs['gaussian'][0],
        outputs['mesh'][0],
        simplify=0.95,
        texture_size=1024,
    )
    os.makedirs(os.path.dirname(output_glb_path), exist_ok=True)
    glb.export(output_glb_path)
    print(f"[✓] Saved GLB to: {output_glb_path}")
except Exception as e:
    print(f"[ERROR] Failed to export GLB: {e}")

# === 8. Export Gaussian as PLY ===
try:
    outputs['gaussian'][0].save_ply(output_ply_path)
    print(f"[✓] Saved PLY to: {output_ply_path}")
except Exception as e:
    print(f"[WARN] Failed to save PLY: {e}")
