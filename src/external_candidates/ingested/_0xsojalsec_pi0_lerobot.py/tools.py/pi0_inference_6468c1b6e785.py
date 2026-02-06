# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pi0-lerobot\tools\pi0_inference.py
import torch
import tyro
from pi0_lerobot.apis.pi0_inference import InferenceArgs, inference_pi0

if __name__ == "__main__":
    with torch.inference_mode():
        inference_pi0(tyro.cli(InferenceArgs))
