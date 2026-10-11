"""Safe Colab preflight: checks hardware and Drive assets without loading models.

This script does not install packages, download model weights, or change Drive files.
Run it only after connecting to the desired Colab runtime.
"""

import os
import sys
import shutil
from pathlib import Path
import importlib.metadata as metadata

print("=== Python / packages ===")
print("Python:", sys.version.split()[0])
for name in ("torch", "diffusers", "transformers", "accelerate", "triton", "lightx2v", "gptqmodel", "bitsandbytes"):
    try:
        print(f"{name}: {metadata.version(name)}")
    except metadata.PackageNotFoundError:
        print(f"{name}: NOT INSTALLED")

print("\n=== GPU ===")
try:
    import torch
    print("torch:", torch.__version__)
    print("torch.version.cuda:", torch.version.cuda)
    available = torch.cuda.is_available()
    print("CUDA available:", available)
    if available:
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            print(f"GPU {i}: {props.name}")
            print(f"  VRAM: {props.total_memory / (1024**3):.2f} GiB")
            print(f"  compute capability: {props.major}.{props.minor}")
            print(f"  allocated: {torch.cuda.memory_allocated(i) / (1024**3):.2f} GiB")
            print(f"  reserved: {torch.cuda.memory_reserved(i) / (1024**3):.2f} GiB")
    else:
        print("ACTION: Do not load a model. Select a GPU runtime if Colab makes one available.")
except Exception as exc:
    print("GPU check failed:", repr(exc))

print("\n=== Runtime disk ===")
try:
    total, used, free = shutil.disk_usage("/content")
    print(f"total={total/(1024**3):.2f} GiB, used={used/(1024**3):.2f} GiB, free={free/(1024**3):.2f} GiB")
except Exception as exc:
    print("Disk check failed:", repr(exc))

print("\n=== Expected Drive assets (presence and size only) ===")
roots = (
    Path("/content/drive/MyDrive/ZImage_Bot"),
    Path("/content/drive/My Drive/ZImage_Bot"),
)
relative_files = (
    "Z-Image-Turbo-Quantized/z_image_turbo_scaled_fp8_e4m3fn.safetensors",
    "Z-Image-Turbo-Quantized/z_image_turbo_int8.safetensors",
    "Z-Image-Turbo/vae/diffusion_pytorch_model.safetensors",
    "Qwen3-4B-GPTQ-Int4/model.safetensors",
)
seen = False
for root in roots:
    print(f"{root}: {'FOUND' if root.exists() else 'not found'}")
    if not root.exists():
        continue
    seen = True
    for relative in relative_files:
        p = root / relative
        if p.is_file():
            print(f"  OK {relative} ({p.stat().st_size / (1024**3):.2f} GiB)")
        else:
            print(f"  MISSING {relative}")
if not seen:
    print("Drive is not mounted or the expected folder is at another path.")
    print("Mount it manually in another cell if needed; this script will not request Drive access.")

print("\nPreflight complete. No models loaded; no packages installed; no files changed.")
