# ZImage Bot

Phone-first Telegram image generation bot project.

## Current status

The model files are already stored in Google Drive. The current free Colab runtime had no GPU available, and Colab reported GPU usage limits. Do not load the model or reinstall packages until a GPU runtime is actually available.

## Start here on a phone

- [Open the safe preflight notebook in Google Colab](https://colab.research.google.com/github/sokolkingsokol-prog/zimage-bot/blob/main/colab/ZImage_Bot_Preflight.ipynb)
- [GPU recovery checklist](COLAB_GPU_RECOVERY.md)
- [Research notes and decisions](RESEARCH_NOTES.md)

## Project guide

- [Bot architecture and deployment guardrails](BOT_ARCHITECTURE.md)
- [Colab setup instructions](COLAB_SETUP.md)
- [Safe GPU preflight script](colab/01_gpu_preflight.py)
- [Runtime and Drive diagnostics](colab/00_runtime_check.py)

## Confirmed model source

The transformer files match the filenames in [lightx2v/Z-Image-Turbo-Quantized](https://huggingface.co/lightx2v/Z-Image-Turbo-Quantized). The documented loader is [ModelTC/LightX2V](https://github.com/ModelTC/LightX2V). See the research notes for the required quantization schemes, Qwen3 text encoder check, and GPU-attention compatibility caution.

## Important

Free Colab GPU availability is not guaranteed. Use Colab first for interactive model validation; don't rely on a free managed Colab session as a permanently running Telegram bot host. See the official [Colab FAQ](https://research.google.com/colaboratory/faq.html).

Keep model weights in Google Drive and credentials in Colab Secrets or a deployment platform's secret store. Never commit model weights, Telegram tokens, API keys, passwords, or private generated images to this repository.
