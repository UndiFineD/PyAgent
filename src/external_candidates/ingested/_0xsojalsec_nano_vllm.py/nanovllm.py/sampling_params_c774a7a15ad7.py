# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-nano-vllm\nanovllm\sampling_params.py
from dataclasses import dataclass


@dataclass
class SamplingParams:
    temperature: float = 1.0
    max_tokens: int = 64
    ignore_eos: bool = False
