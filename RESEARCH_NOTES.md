# Research notes and project decisions

Last reviewed: 2026-10-11

## Goal and constraints

- Build a Telegram bot that accepts a prompt and optionally a reference image, then returns a generated image.
- Work from an Android phone; keep the setup copy/paste friendly.
- Preserve existing model weights in Google Drive; do not download them again without a reason.
- Keep all tokens and credentials out of GitHub and source files.
- Prefer free options, but do not promise that free GPU capacity is always available.

## Confirmed existing Drive assets

Expected root: `/content/drive/MyDrive/ZImage_Bot`

- `Z-Image-Turbo-Quantized/z_image_turbo_scaled_fp8_e4m3fn.safetensors`
- `Z-Image-Turbo-Quantized/z_image_turbo_int8.safetensors`
- `Z-Image-Turbo/vae/diffusion_pytorch_model.safetensors`
- `Qwen3-4B-GPTQ-Int4/model.safetensors`

These files were visible in the last runtime diagnostic. Their presence alone does not prove that they form a compatible, runnable pipeline; we must identify the exact quantization implementation and matching configs before loading them.

## Current blocker

The latest runtime diagnostic showed Python 3.13.16 and `torch 2.11.0+cpu`, with `torch.cuda.is_available() == False`. Colab then explicitly reported that GPU access is temporarily unavailable due to usage limits. Do not try to work around this limit. Keep GPU-dependent tests paused until Colab offers a GPU again.

## Important Colab policy / reliability finding

Google's official Colab FAQ says free resources and GPUs are not guaranteed, limits vary, and free managed runtimes commonly terminate when used to bypass the notebook UI with a web UI for content generation. Therefore, a continuously running Telegram bot whose backend is a free Colab runtime is not a dependable long-term deployment plan and may be terminated. Use Colab first for interactive experiments and validating the local model. Before deploying a persistent Telegram bot, choose a hosting service whose terms explicitly permit a bot worker and whose available compute fits the model.

Official reference: https://research.google.com/colaboratory/faq.html

## Model/inference findings

- Official Z-Image project: https://github.com/Tongyi-MAI/Z-Image
- Official Diffusers pipeline docs: https://huggingface.co/docs/diffusers/api/pipelines/z_image
- Official project documents a 6B-parameter family and standard Z-Image-Turbo inference. Its standard model layout is not the same as the custom quantized single-file transformer in this Drive folder.
- A T4 GPU has about 16 GB VRAM class hardware, but the user previously encountered a near-full VRAM/OOM condition and Triton compatibility errors. Do not assume BF16, FP8, or arbitrary Triton kernels will work on T4. Detect the actual GPU and choose a supported inference path.
- The filenames `z_image_turbo_scaled_fp8_e4m3fn.safetensors` and `z_image_turbo_int8.safetensors` are not enough to identify a supported loader. First locate the source repo/model card and exact load code used when these files were obtained. Do not invent a loader or silently convert weights.

## Recommended sequence when GPU returns

1. Run `colab/01_gpu_preflight.py`; it makes no changes.
2. Mount Drive and run the existing `colab/00_runtime_check.py`.
3. Confirm the GPU model, VRAM, torch build, CUDA availability, model file sizes, and available disk.
4. Identify the quantization format/source and match the loader to the existing weights.
5. Generate one small test image interactively and save it to Drive. Do not start a Telegram polling loop yet.
6. Test reference-image conditioning separately only if the chosen pipeline supports image-to-image/reference input.
7. Implement bot handlers and queueing after generation is stable; store the Telegram token in Colab Secrets for testing, never in GitHub.
8. For persistent public use, deploy on a service that allows long-running bot processes. Do not treat Colab as an always-on server.

## Security checklist

- Never commit Telegram tokens, bot API keys, cookies, or private credentials.
- Never commit model weights or private generated images.
- Use a private Telegram bot while testing.
- Restrict image dimensions, queue length, file size, and per-user request rate.
- Validate downloaded Telegram files and remove temporary files after processing.
- Log technical errors without logging secrets or private prompt/reference content.

## Useful official references

- Colab FAQ and resource limits: https://research.google.com/colaboratory/faq.html
- Z-Image official source: https://github.com/Tongyi-MAI/Z-Image
- Diffusers Z-Image docs: https://huggingface.co/docs/diffusers/api/pipelines/z_image
