
from flask import Flask, request, jsonify
import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image
import os
import datetime
import json

app = Flask(__name__)

print("📦 Loading TopoGen pipeline...")

# Model paths
base_model_path = "models/sdxl-base"
lora_weights_path = "models/lora-topogen/pytorch_lora_weights.safetensors"

# Load pipeline
pipe = StableDiffusionXLPipeline.from_pretrained(
    base_model_path,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.to("cuda")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "Mountainous terrain with valleys")
    negative_prompt = data.get("negative_prompt", "")

    print(f"🧠 Prompt: {prompt}")

    # Reapply LoRA before every generation
    pipe.load_lora_weights(lora_weights_path)

    # Encode prompt
    prompt_embeds, negative_prompt_embeds, pooled_prompt_embeds, negative_pooled_prompt_embeds = pipe.encode_prompt(
        prompt=prompt,
        negative_prompt=negative_prompt
    )

    time_ids = torch.tensor([[512, 512, 0, 0, 512, 512]], dtype=prompt_embeds.dtype, device=prompt_embeds.device)

    image = pipe(
        prompt_embeds=prompt_embeds,
        negative_prompt_embeds=negative_prompt_embeds,
        pooled_prompt_embeds=pooled_prompt_embeds,
        negative_pooled_prompt_embeds=negative_pooled_prompt_embeds,
        added_cond_kwargs={"time_ids": time_ids},
        cross_attention_kwargs={"scale": 1.2},
        height=512,
        width=512,
        num_inference_steps=20,
        guidance_scale=7.5
    ).images[0]

    # Create output directory and timestamped filename
    output_dir = "C:/Users/OWNER/Desktop/topogen_server"
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"output_topogen_{timestamp}.png"
    output_path = os.path.join(output_dir, output_filename)

    # Save image
    image.convert("RGBA").save(output_path, format="PNG", optimize=False)

    # Log generation in a JSON file
    log_path = os.path.join(output_dir, "generation_log.json")
    log_entry = {"timestamp": timestamp, "file": output_filename, "prompt": prompt}
    try:
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                log_data = json.load(f)
        else:
            log_data = []

        log_data.append(log_entry)
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2)
    except Exception as e:
        print(f"Failed to write log: {e}")

    return jsonify({
        "status": "success",
        "image_path": output_path
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
