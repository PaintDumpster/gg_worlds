# ***Terrain‑Aware Street‑Layout Generation with ComfyUI + T2I‑Adapter***


**Goal:** *turn a grayscale height/depth map into a realistic street‑layout image that hugs the terrain, using Stable Diffusion XL and the T2I‑Adapter (depth‑MiDaS)/(depth‑ZoeS) inside ComfyUI.*

![workflow 2](https://github.com/user-attachments/assets/277199f8-7485-4600-95aa-3d8603d71422)

![lugano](https://github.com/user-attachments/assets/4e7aba1b-781e-44e1-bdd9-f5a35ae2aede)

![ComfyUI_temp_aapeh_00004_](https://github.com/user-attachments/assets/e6b58467-2de0-487a-9b08-300aaa58cd57)

![ComfyUI_temp_aapeh_00008_](https://github.com/user-attachments/assets/2c8b8e15-3f09-4629-a8fa-c00811222184)

![ComfyUI_temp_aapeh_00010_](https://github.com/user-attachments/assets/1877f951-d11b-477f-9af0-e55c0a39944b)

![hobart, australia ](https://github.com/user-attachments/assets/727254f3-b30b-4088-86cd-6538c68faff8)

![ComfyUI_temp_aapeh_00003_ (1)](https://github.com/user-attachments/assets/9331535a-d11b-4264-8ec8-b8781bbd8716)



**1 . How it works**

  Component →→→→ Role

  - SDXL 1.0 base checkpoint →→→→ The core image generator (large UNet + VAE + CLIP‑TE)

  - T2I‑Adapter (depth‑midas‑sdxl‑1.0 →→→→ Reads the input depth/height map and injects "terrain awareness" into the UNet

  - ComfyUI →→→→ Node/graph interface to wire everything together and run locally (GPU)

When you press Run, ComfyUI:
  1. Encodes your prompt with SDXL’s CLIP text encoder.
    
  2. Encodes your depth map with the adapter, producing feature maps.

  3. Feeds prompt + depth features into SDXL’s UNet sampler.
    
  4. Decodes the latent back to an image → street layout that fits the land.
       

**2 . Prerequisites**

 Item →→→→ Minimum

  - GPU →→→→ NVIDIA GTX 10‑series or newer (RTX preferred) — 8 GB VRAM+ for 1024×1024

  - Windows / Linux / macOS (AMD/Apple OK) →→→→ Tested on Win 10 + RTX 3060 Laptop

  - Python 3.10 →→→→ Required (3.13 causes package issues)

  - ComfyUI →→→→ Portable or manual install

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

     [Load Checkpoint]    (sd_xl_base_1.0.safetensors)
        ├ model ─────┐
        ├ clip  → [SDXL Prompt Encode] ->+ positive/negative
        └ vae   ─────┘
                                ↓
    [ControlNet Loader] (t2i‑adapter‑depth‑midas‑sdxl‑1.0)
        ↓
    [Load Image] (grayscale depth PNG)  → [Apply ControlNet] → latent
                                ↓
    [ KSampler ]   width=1024 height=1024 steps=25 cfg=7 scheduler=euler_a
        ↓
    [ VAE Decode ] → [Preview / Save Image]


Node →→→→ Key setting

  - Load Checkpoint →→→→ sd_xl_base_1.0.safetensors

  - SDXL Prompt Encode →→→→ positive / negative prompts

  - Load Image →→→→ your grayscale height PNG (1024×1024)

  - ControlNet Loader →→→→ t2i-adapter-depth-midas-sdxl-1.0.safetensors

  - Apply ControlNet →→→→ strength 1.0  start 0  end 1

  - KSampler →→→→ 25 steps · Euler a · cfg 7

(Drag SDXL Prompt Encode from the node menu: conditioning → SDXL Prompt Encode.)

**6 . Usage**

  1. Select a height map in Load Image.

  2. Write a prompt, e.g.:

    positive:   dense urban grid following valleys
    negative:   low detail, blurry, bad perspective

  3. Click Run → result pops up in Preview Image and saves to ComfyUI/output/.

**- Parameter tips**

Issue →→→→ Fix

- Roads ignore relief →→→→ raise strength to 1.2 or reduce cfg

- Too rigid →→→→ lower strength to 0.6 or set start_percent 0.2

- Blurry →→→→ increase steps to 30 or try DPM++ 2M Karras

**7 . Calling via the ComfyUI API**

Running
      
    python main.py
UI → http://127.0.0.1:8188

API → POST JSON workflow to http://127.0.0.1:8188/prompt

    import json, requests
    wf = json.load(open(r"C:\ComfyUI\workflows\depth_adapter_sdxl.json"))
    wf["prompt"]["3"]["inputs"]["image"] = r"C:\ComfyUI\input\my_dem.png"
    wf["prompt"]["2"]["inputs"]["text_positive"] = "street layout respecting terrain"
    wf["prompt"]["2"]["inputs"]["text_negative"] = "low detail"
    resp = requests.post("http://127.0.0.1:8188/prompt", json=wf).json()
    print("saved image:", resp["images"][0]["filename"])

**8 . Troubleshooting**

Erro     →→→→     Cause / fix

Missing torch‑CUDA    →→→→    Install GPU build: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

comfyui‑frontend‑package not installed →→→→ pip install -r requirements.txt (Python 3.10 recommended)

Black output → Height map too small →→→→ upscale to 1024² or increase steps

ModuleNotFoundError →→→→ yaml	pip install pyyaml

ModuleNotFoundError →→→→ torchsde	pip install torchsde

Torch not compiled with CUDA enabled →→→→ uninstall torch → reinstall cu118 wheel

comfyui-frontend-package is not installed →→→→ pip install -r requirements.txt

2 GB torch wheel aborts with No space left on device →→→→ free ≥ 8 GB on C: drive

**9 . Credits**

- T2I‑Adapter © Tencent ARC (https://github.com/TencentARC/T2I-Adapter)

- Stable Diffusion XL – CreativeML Open RAIL‑M

- ComfyUI – Apache 2.0

- Height‑map dataset: NASADEM (NASA JPL)

(MIT License – use at your own risk.)

# Lora finetuning models

https://civitai.com/models/736706/epic-gorgeous-details?modelVersionId=863655

https://civitai.com/models/663742/flux-vividizer-or-flux-enhancer?modelVersionId=742813

https://huggingface.co/black-forest-labs/FLUX.1-dev/tree/main

https://huggingface.co/hfmaster/models/blob/ede8cefc744369a6abe0ccd23ab7b4cbff9c8846/flux/flux-turbo-8steps.safetensors

https://huggingface.co/black-forest-labs/FLUX.1-schnell/tree/main

https://huggingface.co/XLabs-AI/flux-lora-collection/tree/main

https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/flux1-dev.safetensors
