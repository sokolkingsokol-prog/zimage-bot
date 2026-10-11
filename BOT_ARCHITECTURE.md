# Telegram image bot architecture

## Target user experience

1. User sends a text prompt, optionally with a reference photo.
2. Bot checks the prompt and image size/type.
3. Bot places the request in a small queue and sends a status message.
4. Worker generates one image.
5. Bot sends the image back with the prompt and seed (if supported).
6. Temporary files are deleted after sending; errors are shown in plain language.

## Components

- **Telegram adapter:** receives messages, validates uploads, sends progress and output.
- **Generation worker:** one model instance per worker process; serial queue initially to avoid VRAM exhaustion.
- **Model adapter:** the existing quantized Z-Image-Turbo weights match `lightx2v/Z-Image-Turbo-Quantized`; use the documented `ModelTC/LightX2V` loader and the matching FP8/INT8 scheme. Do not assume the ordinary Diffusers pipeline can load the quantized transformer file directly.
- **Text encoder:** verify the full local Qwen3-4B-GPTQ-Int4 folder, including config and tokenizer files, before loading.
- **Storage:** temporary input/output files in runtime disk; optional final output copy to the user's Drive folder.
- **Secrets:** Telegram token read from environment/Colab Secrets, never hardcoded or committed.
- **Configuration:** output dimensions/aspect ratio, steps, queue size, file size limit and output retention configured centrally.

## Safety and reliability rules

- Start with one user / one queued job, not parallel generation.
- Abort early when CUDA is unavailable; never silently fall back to CPU for a large model.
- Enable model-level CPU offloading as shown by the quantized model card, before creating the generator.
- Do not copy `flash_attn3` blindly to a T4 GPU; verify supported attention backend for the actual GPU and installed LightX2V version.
- Do not enable `torch.compile` or experimental Triton kernels in the first working version.
- Catch and report model-loading and generation errors; avoid retry loops that repeatedly allocate GPU memory.
- Validate reference-image support in the selected Z-Image task before accepting image uploads. Do not claim it works until an actual test passes.
- Enforce upload size, image format, per-user rate limits and queue limit.
- Never log Telegram tokens, cookies, or private file contents.
- Keep generated files and weights out of GitHub.

## Deployment decision

Use Google Colab for interactive model validation and development only. Google's free managed Colab FAQ says resources are not guaranteed and notes that content-generation web UIs on free runtimes are commonly terminated. A Telegram polling bot is a long-running worker, so free Colab is not a dependable always-on host.

After the model works, select a host whose terms permit long-running bot workers and whose compute fits the selected model. Keep a one-shot Colab notebook path as the low-cost manual fallback.

## References

- Quantized weights and load example: https://huggingface.co/lightx2v/Z-Image-Turbo-Quantized
- LightX2V source: https://github.com/ModelTC/LightX2V
- Colab policy and limits: https://research.google.com/colaboratory/faq.html
