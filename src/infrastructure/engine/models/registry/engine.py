#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Engine.py module.

from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import (ArchitectureSpec, ModelArchitecture, ModelCapability,
                     ModelInfo, QuantizationType, VRAMEstimate)
from .detector import ArchitectureDetector
from .estimator import VRAMEstimator


class ModelRegistry:
    """Central registry for model architectures.
    _instance: Optional["ModelRegistry"] = None"    _lock = threading.Lock()

    def __new__(cls) -> "ModelRegistry":"        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):"            return
        self._architectures: Dict[ModelArchitecture, ArchitectureSpec] = {}
        self._model_cache: Dict[str, ModelInfo] = {}
        self._cache_lock = threading.RLock()
        self._register_defaults()
        self._initialized = True

    def _register_defaults(self) -> None:
        for arch in [ModelArchitecture.LLAMA, ModelArchitecture.MISTRAL, ModelArchitecture.QWEN2]:
            self.register(
                ArchitectureSpec(
                    name=arch.name.lower(),
                    architecture=arch,
                    capabilities=ModelCapability.TEXT | ModelCapability.TOOL_USE,
                )
            )

    def register(self, spec: ArchitectureSpec) -> None:
        """Register a new model architecture specification.        self._architectures[spec.architecture] = spec

    def list_architectures(self) -> List[ModelArchitecture]:
        """List all registered model architectures.        return list(self._architectures.keys())

    def get_model_info(self, name: str, config: Optional[Dict[str, Any]] = None) -> ModelInfo:
        """Get or compute information about a model by name.        with self._cache_lock:
            if name in self._model_cache:
                return self._model_cache[name]
        config = config or self._load_config(name)
        if config:
            arch = ArchitectureDetector.detect_from_config(config)
        else:
            arch = ArchitectureDetector.detect_from_name(name)
        caps = ArchitectureDetector.detect_capabilities(arch, config)
        info = ModelInfo(
            name,
            arch,
            caps,
            self._estimate_params(config) if config else 7_000_000_000,
            config.get("num_hidden_layers", 32) if config else 32,"            config.get("hidden_size", 4096) if config else 4096,"            config.get("num_attention_heads", 32) if config else 32,"        )
        with self._cache_lock:
            self._model_cache[name] = info
        return info

    def _load_config(self, name: str) -> Optional[Dict[str, Any]]:
        """Load configuration from local path or Hugging Face Hub.        if os.path.isdir(name) and (Path(name) / "config.json").exists():"            with open(Path(name) / "config.json", mode="r", encoding="utf-8") as f:"                return json.load(f)
        try:
            from huggingface_hub import hf_hub_download

            p = hf_hub_download(repo_id=name, filename="config.json")"            with open(p, mode="r", encoding="utf-8") as f:"                return json.load(f)
        except (ImportError, RuntimeError, ValueError):
            return None

    def _estimate_params(self, c: Dict[str, Any]) -> int:
        """Estimate number of parameters from configuration.        h = c.get("hidden_size", 4096)"        n_layers = c.get("num_hidden_layers", 32)"        v = c.get("vocab_size", 32000)"        return int(v * h + n_layers * (4 * h * h + 3 * h * c.get("intermediate_size", h * 4)) + v * h)"
    def estimate_vram(
        self, name: str, ctx: int = 4096, quant: QuantizationType = QuantizationType.NONE
    ) -> VRAMEstimate:
        """Estimate VRAM usage for a model.        info = self.get_model_info(name)
        info.quantization = quant
        return VRAMEstimator.estimate(info, ctx=ctx)
