# ZImage Bot

Phone-first Telegram image generation bot project.

## Current status

The model files are already stored in Google Drive. The current free Colab runtime had no GPU available, and Colab reported GPU usage limits. Do not load the model or reinstall packages until a GPU runtime is actually available.

## Project guide

- [Research notes and decisions](RESEARCH_NOTES.md)
- [Bot architecture and deployment guardrails](BOT_ARCHITECTURE.md)
- [Colab setup instructions](COLAB_SETUP.md)
- [GPU recovery checklist](COLAB_GPU_RECOVERY.md)
- [Safe GPU preflight script](colab/01_gpu_preflight.py)
- [Runtime and Drive diagnostics](colab/00_runtime_check.py)

## Important

Free Colab GPU availability is not guaranteed. Use Colab first for interactive model validation; don't rely on a free managed Colab session as a permanently running Telegram bot host. See the official [Colab FAQ](https://research.google.com/colaboratory/faq.html).

Keep model weights in Google Drive and credentials in Colab Secrets or a deployment platform's secret store. Never commit model weights, Telegram tokens, API keys, passwords, or private generated images to this repository.
