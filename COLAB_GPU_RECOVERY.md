# Recover the Colab GPU runtime

The diagnostic reported `torch: 2.11.0+cpu` and `CUDA available: False`. Do not load any model until this is fixed.

## Step 1 — Select a GPU runtime

In the Colab notebook, open **Runtime → Change runtime type** and select **T4 GPU** under Hardware accelerator if it is offered. Save the setting, then connect to the runtime.

If the menu does not offer a GPU, or Colab says no GPU is available, do not reinstall PyTorch; wait and try later or use another available GPU runtime. GPU availability depends on the account and current capacity.

## Step 2 — Check the runtime before installing anything

Run this cell:

```python
import torch
print("PyTorch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print("CUDA build:", torch.version.cuda)
```

A usable GPU should show `CUDA available: True` and a GPU name (for example, Tesla T4). If it still shows `+cpu` or `False`, stop and send the output. Do not install a random PyTorch build.

## Step 3 — Reconnect Drive and rerun diagnostics

After a runtime reset, mount Drive again:

```python
from google.colab import drive
drive.mount('/content/drive')
```

Then run:

```python
!wget -q https://raw.githubusercontent.com/sokolkingsokol-prog/zimage-bot/main/colab/00_runtime_check.py -O /content/00_runtime_check.py
%run /content/00_runtime_check.py
```

Send the full output before model loading. This procedure does not download or alter model weights.
