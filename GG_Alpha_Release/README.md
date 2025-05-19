# GG Worlds Alpha - Terrain Generator for Blender

Welcome to **GG Worlds (Alpha)**! This tool lets you generate realistic terrain textures and heightmaps using AI directly from **inside Blender**.

No coding needed. This guide walks you through **everything step-by-step** so anyone can use it.

---

[![GG Worlds](https://img.shields.io/badge/discord-ark-%237289da.svg?logo=discord)](https://discord.gg/Dw23W5j5)

---


## 📦 What You Get

This alpha release includes:

- Blender Addon (`GG_BlenderPlugin.zip`)
- AI Backend to generate terrain (`topogen_api.py`)
- A one-click start file (`ggworlds_start.bat`)

You write a detailed prompt like:
> "Rocky mountain with a valley and river"

And the tool creates a 3D terrain image you can preview and apply in Blender.

---

## 🧰 What You Need First

### ✅ 1. A Computer with a Supported NVIDIA GPU
- The AI model is very large (~70GB) and needs a good graphics card
- This is meant for high-end systems or workstations

### ✅ 2. Install Blender
- [Download Blender here](https://www.blender.org/download/)
- Version 3.0 or later is recommended

### ✅ 3. Install Python
- [Download Python 3.10+ here](https://www.python.org/downloads/)
- During install, make sure to check the box **"Add Python to PATH"**

---

## 📁 Folder Setup (Very Important!)

Your folder should look like this:

```
GGWorlds_Alpha_Release/
├── models/
│   ├── sdxl-base/                <-- Put your SDXL base model files here
│   └── lora-topogen/
│       └── pytorch_lora_weights.safetensors
├── venv/                        <-- Auto-generated when backend starts
├── generation_log.json          <-- Stores generation logs
├── GG_BlenderPlugin.zip         <-- Blender addon file
├── ggworlds_start.bat           <-- Double-click to start backend
├── requirements.txt             <-- Lists Python dependencies
├── topogen_api.py               <-- Backend server script
```

> If you are missing the model files, the backend will NOT work.

---

## ▶️ How to Run the AI Backend (Image Generator)

1. **Open the GGWorlds_Alpha_Release folder**
2. **Double-click** the file: `ggworlds_start.bat`
3. A black window will appear and do the following:
   - Create a virtual environment (first time only)
   - Install all the needed libraries (first time only)
   - Start the server
4. When you see:
   ```
   📦 Loading TopoGen pipeline...
   ✅ Running on CUDA
   * Running on http://0.0.0.0:5000
   ```
   ✅ You're ready to go!

> Do **not close** this window. It must stay open while you use Blender.

---

## 🧩 How to Install the Blender Addon

1. Open **Blender**
2. Go to **Edit > Preferences > Add-ons**
3. Click **Install** (top right)
4. Select `GG_BlenderPlugin.zip`
5. Enable the addon by checking the box: ✅ GG Worlds (Alpha)
6. Press `N` to open the side panel, and click on the **GG** tab

---

## 🏞 How to Generate Terrain in Blender

1. In the GG Panel:
   - Click **"Generate Base Plane"**
2. Enter a terrain prompt:
   > e.g., "Snowy hills with pine trees"
3. Click **Generate**
   - Wait ~10–20 seconds (check for progress in the PowerShell)
4. When the preview image appears:
   - Click **Preview** to apply it visually
   - Click **Apply** to modify the mesh with height

✅ Done! You now have AI-generated terrain inside Blender!

---

## 🛠 If Something Isn’t Working

- 🔴 **No image preview?**
  - Make sure the backend is running (black window open)
  - Make sure your models are in the `models/` folder

- 🔴 **"Image not found after waiting" error?**
  - You must have the `generation_log.json` created by the backend
  - The image must be saved in a valid location

- 🔴 **Backend says no CUDA or crashes?**
  - You need a proper NVIDIA GPU with the correct drivers installed
  - If you're unsure, ask in the community (see below)

---

## 💬 Community & Support

Join us on Discord:
👉 https://discord.gg/Dw23W5j5

Ask questions, share terrain ideas, and get support directly from the devs.

---

## 📄 License
- This code is released under the MIT License
- The SDXL model is licensed under CreativeML Open RAIL-M
- Do not redistribute the model weights unless you're complying with the license terms

---

Thank you for testing GG Worlds Alpha!
We’re excited to see what you build.
