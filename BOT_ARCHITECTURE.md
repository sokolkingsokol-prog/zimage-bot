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
- **Model adapter:** one isolated implementation matching the exact model/quantization format in Google Drive. Do not mix the standard Diffusers pipeline with unrelated quantized weights.
- **Storage:** temporary input/output files in runtime disk; optional final output copy to the user's Drive folder.
- **Secrets:** Telegram token read from environment/Colab Secrets, never hardcoded or committed.
- **Configuration:** output width/height, steps, queue size, file size limit and output retention configured centrally.

## Safety and reliability rules

- Start with one user / one queued job, not parallel generation.
- Use a default 768x768 or lower test size only if the selected pipeline supports it; the official Z-Image-Turbo example uses 1024x1024 and 8 effective DiT forwards. Confirm pipeline constraints before changing dimensions.
- Check available VRAM before loading. Abort early when CUDA is unavailable; never silently fall back to CPU for a large model.
- Do not enable torch.compile or experimental Triton kernels in the first working version.
- Catch and report model-loading and generation errors; avoid retry loops that repeatedly allocate GPU memory.
- Enforce upload size, image format, per-user rate limits and queue limit.
- Never log Telegram tokens, cookies, or private file contents.
- Keep generated files and weights out of GitHub.

## Deployment decision

Use Google Colab for interactive model validation and development only. Google's free managed Colab FAQ says resources are not guaranteed and notes that content-generation web UIs on free runtimes are commonly terminated. A Telegram polling bot is also a long-running worker, so it is not a reliable free always-on host.

After the model works, select a host whose terms permit long-running bot workers and whose compute fits the selected model. Keep a one-shot Colab notebook path as the low-cost manual fallback.
