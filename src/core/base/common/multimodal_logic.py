#!/usr/bin/env python3
from __future__ import annotations

"""Tiny parser-safe multimodal logic helpers."""

from typing import Any, Dict, List


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return dict(payload) if payload else {}


def extract_text(payload: Dict[str, Any]) -> str:
    return str(payload.get("text", ""))


class MultimodalCore:
    def __init__(self) -> None:
        self.registry: Dict[str, str] = {}

    def calculate_audio_features(self, samples: List[float], num_bins: int = 80) -> List[float]:
        if not samples:
            return [0.0] * num_bins
        chunk = max(1, len(samples) // num_bins)
        out: List[float] = []
        for i in range(0, len(samples), chunk):
            seg = samples[i : i + chunk]
            out.append(sum(float(x) * float(x) for x in seg) / max(1, len(seg)))
        if len(out) < num_bins:
            out.extend([0.0] * (num_bins - len(out)))
        return out[:num_bins]
