# Colab runtime and Drive diagnostics — safe to run before loading any model.
# This script does NOT download weights, install packages, or read secret values.

import os
import sys
import importlib.metadata as metadata
from pathlib import Path

print("=== Runtime ===")
print("Python:", sys.version.split()[0])

for package in ("torch", "diffusers", "transformers", "accelerate", "triton", "lightx2v", "gptqmodel"):
    try:
        print(f"{package}: {metadata.version(package)}")
    except metadata.PackageNotFoundError:
        print(f"{package}: NOT INSTALLED")

print("\n=== CUDA / GPU ===")
try:
    import torch
    print("PyTorch:", torch.__version__)
    print("CUDA available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))
        props = torch.cuda.get_device_properties(0)
        print(f"GPU VRAM: {props.total_memory / (1024**3):.2f} GiB")
        print("Allocated:", f"{torch.cuda.memory_allocated(0)/(1024**3):.2f} GiB")
        print("Reserved:", f"{torch.cuda.memory_reserved(0)/(1024**3):.2f} GiB")
except Exception as exc:
    print("Torch/CUDA check failed:", repr(exc))

print("\n=== Expected model folders ===")
candidates = [
    Path("/content/drive/MyDrive/ZImage_Bot"),
    Path("/content/drive/My Drive/ZImage_Bot"),
    Path("/content/ZImage_Bot"),
]
found = False
for root in candidates:
    print(f"{root}: {'FOUND' if root.exists() else 'not found'}")
    if root.exists():
        found = True
        for rel in (
            "Z-Image-Turbo-Quantized/z_image_turbo_scaled_fp8_e4m3fn.safetensors",
            "Z-Image-Turbo-Quantized/z_image_turbo_int8.safetensors",
            "Z-Image-Turbo/vae/diffusion_pytorch_model.safetensors",
            "Qwen3-4B-GPTQ-Int4/model.safetensors",
        ):
            p = root / rel
            print(f"  {'OK' if p.is_file() else 'MISSING'}: {rel}")
if not found:
    print("Drive may not be mounted, or the folder is at a different path.")
    print("If needed, mount Drive in a separate Colab cell; this script does not mount it automatically.")

print("\n=== Memory snapshot ===")
try:
    import shutil
    total, used, free = shutil.disk_usage("/content")
    print(f"/content disk: total={total/(1024**3):.2f} GiB, used={used/(1024**3):.2f} GiB, free={free/(1024**3):.2f} GiB")
except Exception as exc:
    print("Disk check failed:", repr(exc))

print("\nDiagnostic finished. No model was loaded and no files were changed.")
