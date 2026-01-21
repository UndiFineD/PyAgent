from __future__ import annotations
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
import numpy as np
from .config import LoRAConfig, LoRAInfo, AdapterStatus, LoRAMethod
from .weights import LoRAWeights

class LoRAAdapter:
    """Represents a loaded LoRA adapter."""

    def __init__(self, config: LoRAConfig):
        self.config = config
        self.weights: Optional[LoRAWeights] = None
        self.info: Optional[LoRAInfo] = None
        self._status = AdapterStatus.LOADING
        self._load_time_ms = 0.0

    @property
    def name(self) -> str: return self.config.adapter_name

    @property
    def status(self) -> AdapterStatus: return self._status

    def load(self) -> bool:
        start = time.perf_counter()
        try:
            path = Path(self.config.adapter_path)
            if path.is_dir(): self.weights = self._load_from_dir(path)
            elif path.suffix == ".safetensors": self.weights = self._load_st(path)
            elif path.suffix in (".pt", ".pth", ".bin"): self.weights = self._load_torch(path)
            else: raise ValueError(f"Unsupported format: {path}")

            self._load_time_ms = (time.perf_counter() - start) * 1000
            self._status = AdapterStatus.READY
            self.info = LoRAInfo(self.config.adapter_name, self.config.rank, self.config.alpha,
                               self.config.method, self.config.target_modules,
                               self.weights.num_parameters, self.weights.memory_bytes,
                               self._status, self._load_time_ms)
            return True
        except Exception:
            self._status = AdapterStatus.ERROR
            return False

    def _load_from_dir(self, path: Path) -> LoRAWeights:
        for f in ["adapter_model.safetensors", "adapter_model.bin"]:
            if (path / f).exists():
                return self._load_st(path / f) if f.endswith("safetensors") else self._load_torch(path / f)
        raise FileNotFoundError(f"No weights in {path}")

    def _load_st(self, path: Path) -> LoRAWeights:
        from safetensors import safe_open
        w = LoRAWeights()
        with safe_open(str(path), framework="numpy") as f:
            for key in f.keys():
                m = self._extract_module(key)
                if ".lora_A." in key.lower(): w.lora_a[m] = f.get_tensor(key)
                elif ".lora_B." in key.lower(): w.lora_b[m] = f.get_tensor(key)
        for m in w.lora_a: w.scales[m] = self.config.computed_scaling
        return w

    def _load_torch(self, path: Path) -> LoRAWeights:
        import torch
        w = LoRAWeights()
        sd = torch.load(str(path), map_location="cpu")
        for key, t in sd.items():
            m = self._extract_module(key)
            if ".lora_A." in key.lower(): w.lora_a[m] = t.numpy()
            elif ".lora_B." in key.lower(): w.lora_b[m] = t.numpy()
        for m in w.lora_a: w.scales[m] = self.config.computed_scaling
        return w

    def _extract_module(self, key: str) -> str:
        for t in self.config.target_modules:
            if t in key: return t
        for p in reversed(key.split(".")):
            if p not in ("lora_A", "lora_B", "lora_a", "lora_b", "weight", "default"): return p
        return key

    def apply_to_linear(self, module_name: str, hidden_states: np.ndarray) -> np.ndarray:
        if not self.weights or module_name not in self.weights.lora_a: return np.zeros_like(hidden_states)
        la, lb = self.weights.lora_a[module_name], self.weights.lora_b[module_name]
        scale = self.weights.scales.get(module_name, self.config.computed_scaling)
        return scale * (hidden_states @ la.T @ lb.T)

    def merge_into_weights(self, original_weights: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        if not self.weights: raise RuntimeError("Not loaded")
        merged = {k: v.copy() for k, v in original_weights.items()}
        for name, weight in merged.items():
            for t in self.config.target_modules:
                if t in name and t in self.weights.lora_a:
                    delta = self.weights.scales.get(t, self.config.computed_scaling) * (self.weights.lora_b[t] @ self.weights.lora_a[t])
                    merged[name] = weight + delta
        return merged

def load_lora_adapter(path: str, name: Optional[str] = None, rank: int = 8, scale: float = 16.0, **kwargs) -> LoRAAdapter:
    c = LoRAConfig(name or Path(path).stem, path, rank, scale, **kwargs)
    a = LoRAAdapter(c)
    a.load()
    return a

def get_lora_info(path: str) -> Optional[LoRAInfo]:
    p = Path(path)
    if p.is_dir() and (p / "adapter_config.json").exists():
        import json
        with open(p / "adapter_config.json") as f: c = json.load(f)
        return LoRAInfo(p.stem, c.get("r", 8), c.get("lora_alpha", 16), LoRAMethod.LORA, c.get("target_modules", []), 0, 0, AdapterStatus.INACTIVE)
    return None
