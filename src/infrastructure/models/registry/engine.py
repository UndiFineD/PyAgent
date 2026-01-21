from __future__ import annotations
import json
import os
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional
from .config import (
    ModelArchitecture, ArchitectureSpec, ModelInfo, ModelCapability,
    QuantizationType, VRAMEstimate
)
from .detector import ArchitectureDetector
from .estimator import VRAMEstimator

class ModelRegistry:
    """Central registry for model architectures."""
    _instance: Optional['ModelRegistry'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'ModelRegistry':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._architectures: Dict[ModelArchitecture, ArchitectureSpec] = {}
        self._model_cache: Dict[str, ModelInfo] = {}
        self._cache_lock = threading.RLock()
        self._register_defaults()
        self._initialized = True
    
    def _register_defaults(self):
        for arch in [ModelArchitecture.LLAMA, ModelArchitecture.MISTRAL, ModelArchitecture.QWEN2]:
            self.register(ArchitectureSpec(name=arch.name.lower(), architecture=arch, 
                                         capabilities=ModelCapability.TEXT | ModelCapability.TOOL_USE))
            
    def register(self, spec: ArchitectureSpec):
        self._architectures[spec.architecture] = spec
        
    def list_architectures(self) -> List[ModelArchitecture]:
        """List all registered model architectures."""
        return list(self._architectures.keys())

    def get_model_info(self, name: str, config: Optional[Dict[str, Any]] = None) -> ModelInfo:
        with self._cache_lock:
            if name in self._model_cache: return self._model_cache[name]
        config = config or self._load_config(name)
        arch = ArchitectureDetector.detect_from_config(config) if config else ArchitectureDetector.detect_from_name(name)
        caps = ArchitectureDetector.detect_capabilities(arch, config)
        info = ModelInfo(name, arch, caps, self._estimate_params(config) if config else 7_000_000_000,
                        config.get("num_hidden_layers", 32) if config else 32,
                        config.get("hidden_size", 4096) if config else 4096,
                        config.get("num_attention_heads", 32) if config else 32)
        with self._cache_lock: self._model_cache[name] = info
        return info
    
    def _load_config(self, name: str) -> Optional[Dict[str, Any]]:
        if os.path.isdir(name) and (Path(name) / "config.json").exists():
            with open(Path(name) / "config.json", mode="r", encoding="utf-8") as f:
                return json.load(f)
        try:
            from huggingface_hub import hf_hub_download
            p = hf_hub_download(repo_id=name, filename="config.json")
            with open(p, mode="r", encoding="utf-8") as f:
                return json.load(f)
        except (ImportError, RuntimeError, ValueError):
            return None
        
    def _estimate_params(self, c: Dict[str, Any]) -> int:
        h, l, v = c.get("hidden_size", 4096), c.get("num_hidden_layers", 32), c.get("vocab_size", 32000)
        return int(v * h + l * (4 * h * h + 3 * h * c.get("intermediate_size", h * 4)) + v * h)

    def estimate_vram(self, name: str, ctx: int = 4096, quant: QuantizationType = QuantizationType.NONE) -> VRAMEstimate:
        info = self.get_model_info(name)
        info.quantization = quant
        return VRAMEstimator.estimate(info, ctx=ctx)
