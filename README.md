# ***Terrain‑Aware Street‑Layout Generation with ComfyUI + T2I‑Adapter***


**Goal:** *turn a grayscale height/depth map into a realistic street‑layout image that hugs the terrain, using Stable Diffusion XL and the T2I‑Adapter (depth‑MiDaS) inside ComfyUI.*

**1 . How it works**

  Component____________________________________Role

  - SDXL 1.0 base checkpoint_________________The core image generator (large UNet + VAE + CLIP‑TE)

  - T2I‑Adapter (depth‑midas‑sdxl‑1.0________Reads the input depth/height map and injects "terrain awareness" into the UNet

  - ComfyUI____________________________________Node/graph interface to wire everything together and run locally (GPU)

When you press Run, ComfyUI:
  1. Encodes your prompt with SDXL’s CLIP text encoder.
    
  2. Encodes your depth map with the adapter, producing feature maps.

  3. Feeds prompt + depth features into SDXL’s UNet sampler.
    
  4. Decodes the latent back to an image → street layout that fits the land.
       

**2 . Prerequisites**

 Item____________________________________________________Minimum

  - GPU________________________________________________NVIDIA GTX 10‑series or newer (RTX preferred) — 8 GB VRAM+ for 1024×1024

  - Windows / Linux / macOS (AMD/Apple OK)_______Tested on Win 10 + RTX 3060 Laptop

  - Python 3.10________________________________________Required (3.13 causes package issues)

  - ComfyUI____________________________________________Portable or manual install

(CUDA toolkit is not required; the portable build ships its own.)

**3 . Folder layout**

    ComfyUI\
    ├─ models\
    │   ├─ checkpoints\
    │   │   └─ sd_xl_base_1.0.safetensors           (≈ 6.9 GB)

    │   └─ controlnet\
    │   │   └─ t2i-adapter-depth-midas-sdxl-1.0.safetensors

    └─ ... (rest of ComfyUI)

**4 . Setup step‑by‑step**

- Download SDXL base (https://huggingface.co/TheLastBen/SDXL/blob/main/sd_xl_base_1.0.safetensors)

- Download depth adapter (https://huggingface.co/TencentARC/t2i-adapter-depth-midas-sdxl-1.0)

- Copy the files into the folders shown above.

- Launch ComfyUI:

      #Windows portable example:
      run_nvidia_gpu.bat

Browser opens at http://127.0.0.1:8188.

**5 . Build the ComfyUI graph (nodes)**

    [Load Checkpoint]  → model/clip/vae → 
                      [SDXL Prompt Encode] →  
    [Load Image] ─┐                           ┐
                  └→ [Apply ControlNet] → KSampler → VAE Decode → Preview/Save
              
    [ControlNet Loader] ┘


Node___________________________Key setting

  - Load Checkpoint___________sd_xl_base_1.0.safetensors

  - SDXL Prompt Encode_______positive / negative prompts

  - Load Image________________your grayscale height PNG (1024×1024)

  - ControlNet Loader_________t2i-adapter-depth-midas-sdxl-1.0.safetensors

  - Apply ControlNet__________strength 1.0  start 0  end 1

  - KSampler__________________25 steps · Euler a · cfg 7

(Drag SDXL Prompt Encode from the node menu: conditioning → SDXL Prompt Encode.)

**6 . Usage**

  1. Select a height map in Load Image.

  2. Write a prompt, e.g.:

    positive:   dense urban grid following valleys
    negative:   low detail, blurry, bad perspective

  3. Click Run → result pops up in Preview Image and saves to ComfyUI/output/.

**- Parameter tips**

Issue_________________________Fix

- Roads ignore relief_____raise strength to 1.2 or reduce cfg

- Too rigid_______________lower strength to 0.6 or set start_percent 0.2

- Blurry__________________increase steps to 30 or try DPM++ 2M Karras

**7 . Calling via the ComfyUI API**

    import json, requests
    wf = json.load(open(r"C:\ComfyUI\workflows\depth_adapter_sdxl.json"))
    wf["prompt"]["3"]["inputs"]["image"] = r"C:\ComfyUI\input\my_dem.png"
    wf["prompt"]["2"]["inputs"]["text_positive"] = "street layout respecting terrain"
    wf["prompt"]["2"]["inputs"]["text_negative"] = "low detail"
    resp = requests.post("http://127.0.0.1:8188/prompt", json=wf).json()
    print("saved image:", resp["images"][0]["filename"])

**8 . Troubleshooting**

Error_________________________________________Cause / fix

Missing torch‑CUDA_________________________Install GPU build: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

comfyui‑frontend‑package not installed____pip install -r requirements.txt (Python 3.10 recommended)

Black output_________________________________Height map too small → upscale to 1024² or increase steps

**9 . Credits**

- T2I‑Adapter © Tencent ARC (https://github.com/TencentARC/T2I-Adapter)

- Stable Diffusion XL © Stability AI

- ComfyUI © comfyanonymous

(MIT License – use at your own risk.)
