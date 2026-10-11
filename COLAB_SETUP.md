# Running the diagnostics in Google Colab

This first check deliberately does not load Z-Image or install packages. It confirms the current runtime and whether the existing files in Google Drive are visible.

## 1. Open your existing Colab notebook

Select **Runtime → Change runtime type → T4 GPU** (if available), then connect to the runtime.

## 2. Mount Google Drive

Run this in a new Colab cell:

```python
from google.colab import drive
drive.mount('/content/drive')
```

Approve the Google Drive permission prompt. Your existing model folder should be at `/content/drive/MyDrive/ZImage_Bot`.

## 3. Download and run the diagnostic script from this repository

Run this in the next cell:

```python
!mkdir -p /content/zimage-bot
!wget -q https://raw.githubusercontent.com/sokolkingsokol-prog/zimage-bot/main/colab/00_runtime_check.py -O /content/zimage-bot/00_runtime_check.py
%run /content/zimage-bot/00_runtime_check.py
```

## 4. Send the output back

Copy the complete output from the cell into the ChatGPT conversation. It reports package versions, GPU/VRAM, disk space, and whether the existing model files are found.

## Safety

- This check does not download model weights, install packages, load a model, or modify your Drive.
- Never put Telegram bot tokens, API keys, passwords, or private credentials in GitHub files.
- Keep the model weights in Google Drive. Do not upload model weights to this repository.
- Do not reinstall or upgrade packages before we inspect the diagnostic output; the current runtime has had version and GPU-memory issues.
