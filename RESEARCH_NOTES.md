# Research notes and project decisions

Last reviewed: 2026-10-11

## Goal and constraints

- Build a Telegram bot that accepts a text prompt and optionally a reference image, then returns a generated image.
- Work from an Android phone; keep the setup copy/paste friendly.
- Preserve existing model weights in Google Drive; do not download them again.
- Keep all tokens and credentials out of GitHub and source files.
- Prefer free options, but never promise free GPU availability or permanent hosting.

## Confirmed existing Drive assets

Expected root: `/content/drive/MyDrive/ZImage_Bot`

- `Z-Image-Turbo-Quantized/z_image_turbo_scaled_fp8_e4m3fn.safetensors`
- `Z-Image-Turbo-Quantized/z_image_turbo_int8.safetensors`
- `Z-Image-Turbo/vae/diffusion_pytorch_model.safetensors`
- `Qwen3-4B-GPTQ-Int4/model.safetensors`

The quantized transformer filenames are now matched to the official Hugging Face repository `lightx2v/Z-Image-Turbo-Quantized`; they are not arbitrary files. Its README specifies LightX2V as the loader and shows FP8 scheme `fp8-sgl` or INT8 scheme `int8-sgl`. The README recommends a Qwen3-4B INT4 text encoder and CPU offloading for lower VRAM. Do not re-download the already-present transformer weights.

Important remaining verification: our previous diagnostic only checked the existence of `Qwen3-4B-GPTQ-Int4/model.safetensors`, not all config/tokenizer files. Check the whole local folder before attempting the model load. The official example points to `JunHowie/Qwen3-4B-GPTQ-Int4`; confirm that the local folder's config and tokenizer files match this repository.

## Current blocker

The latest runtime diagnostic showed Python 3.13.16 and `torch 2.11.0+cpu`, with `torch.cuda.is_available() == False`. Colab then explicitly reported that GPU access is temporarily unavailable due to usage limits. Do not try to work around this limit or launch a GPU job elsewhere without the user's consent. Keep GPU-dependent tests paused until Colab offers a GPU again.

## Key model source and loader

- Quantized transformer files and documented loader: https://huggingface.co/lightx2v/Z-Image-Turbo-Quantized
- Framework source: https://github.com/ModelTC/LightX2V
- Base model: https://huggingface.co/Tongyi-MAI/Z-Image-Turbo
- Qwen3 INT4 text encoder reference: https://huggingface.co/JunHowie/Qwen3-4B-GPTQ-Int4
- Official Diffusers Z-Image documentation: https://huggingface.co/docs/diffusers/api/pipelines/z_image

The documented LightX2V sequence is:
1. Construct `LightX2VPipeline(model_path="Tongyi-MAI/Z-Image-Turbo", model_cls="z_image", task="t2i")`.
2. Call `enable_quantize()` with the existing FP8 or INT8 checkpoint and the matching scheme; configure Qwen3 INT4 if its local model folder is complete.
3. Call `enable_offload(cpu_offload=True, offload_granularity="model")` before creating the generator.
4. Configure the generator and generate a single test image.

Do not blindly copy the model card's `attn_mode="flash_attn3"` onto a T4: LightX2V documents FlashAttention-3 for newer GPU architectures, and the user's previous T4 session had kernel compatibility errors. Check the actual GPU capability and the current LightX2V-supported attention backend before selecting an attention mode. Start without torch.compile or custom Triton kernels.

## Important Colab policy / reliability finding

Google's official Colab FAQ says free resources and GPUs are not guaranteed, limits vary, and free managed runtimes commonly terminate when used to bypass the notebook UI with a web UI for content generation. Therefore, a continuously running Telegram bot whose backend is a free Colab runtime is not a dependable long-term deployment plan and may be terminated. Use Colab for interactive experiments and validating the local model. Before deploying a persistent Telegram bot, choose a host whose terms explicitly permit a long-running bot worker and whose compute fits the model.

Official reference: https://research.google.com/colaboratory/faq.html

## Recommended sequence when GPU returns

1. Run `colab/01_gpu_preflight.py`; it makes no changes.
2. Mount Drive and run the existing `colab/00_runtime_check.py`.
3. Confirm GPU name, VRAM, torch CUDA build, CUDA availability, model file sizes, free disk and the complete Qwen model directory.
4. Install LightX2V in a fresh GPU runtime using its official installation instructions; capture install errors rather than repeatedly reinstalling packages.
5. Check supported attention backend for the actual GPU before loading any weights.
6. Load the existing local quantized transformer and matching Qwen3 INT4 files, enable model-level CPU offloading, and generate one test image.
7. Only after text-to-image succeeds, test reference-image input. Do not assume a reference photo is supported by the same task mode; verify LightX2V's Z-Image API first.
8. Implement Telegram handlers, one-request queue and rate limits after generation is stable; keep the Telegram token in Colab Secrets for development.
9. For persistent public use, deploy on a service that permits long-running bot processes. Do not treat free Colab as an always-on server.

## Security checklist

- Never commit Telegram tokens, bot API keys, cookies or private credentials.
- Never commit model weights or private generated images.
- Use a private Telegram bot while testing.
- Restrict image dimensions, queue length, file size and per-user request rate.
- Validate Telegram image uploads and remove temporary files after processing.
- Log technical errors without logging secrets or private prompt/reference content.

## Official references

- Colab FAQ and resource limits: https://research.google.com/colaboratory/faq.html
- Quantized model card and code example: https://huggingface.co/lightx2v/Z-Image-Turbo-Quantized
- LightX2V source: https://github.com/ModelTC/LightX2V
- Base Z-Image-Turbo model: https://huggingface.co/Tongyi-MAI/Z-Image-Turbo
- Qwen3 INT4 text encoder: https://huggingface.co/JunHowie/Qwen3-4B-GPTQ-Int4
- Diffusers Z-Image docs: https://huggingface.co/docs/diffusers/api/pipelines/z_image
