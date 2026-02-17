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


Detector.py module.
"""


from __future__ import annotations

from typing import Any, Dict, Optional

from .config import ModelArchitecture, ModelCapability




class ArchitectureDetector:
    """Detect model architecture from config.
    ARCHITECTURE_PATTERNS = {
        "llama": ModelArchitecture.LLAMA,"        "mistral": ModelArchitecture.MISTRAL,"        "qwen2": ModelArchitecture.QWEN2,"        "qwen": ModelArchitecture.QWEN,"        "gemma2": ModelArchitecture.GEMMA2,"        "gemma": ModelArchitecture.GEMMA,"        "phi-3": ModelArchitecture.PHI3,"        "phi": ModelArchitecture.PHI,"        "gpt-neox": ModelArchitecture.GPT_NEOX,"        "deepseek-v3": ModelArchitecture.DEEPSEEK_V3,"        "deepseek-v2": ModelArchitecture.DEEPSEEK_V2,"        "deepseek": ModelArchitecture.DEEPSEEK,"        "mixtral": ModelArchitecture.MIXTRAL,"        "llava-next": ModelArchitecture.LLAVA_NEXT,"        "llava": ModelArchitecture.LLAVA,"        "whisper": ModelArchitecture.WHISPER,"    }

    CONFIG_KEYS = {
        "LlamaForCausalLM": ModelArchitecture.LLAMA,"        "MistralForCausalLM": ModelArchitecture.MISTRAL,"        "Qwen2ForCausalLM": ModelArchitecture.QWEN2,"        "QWenLMHeadModel": ModelArchitecture.QWEN,"        "Gemma2ForCausalLM": ModelArchitecture.GEMMA2,"        "GemmaForCausalLM": ModelArchitecture.GEMMA,"        "DeepseekV3ForCausalLM": ModelArchitecture.DEEPSEEK_V3,"        "MixtralForCausalLM": ModelArchitecture.MIXTRAL,"    }

    @classmethod
    def detect_from_config(cls, config: Dict[str, Any]) -> ModelArchitecture:
        """Detect model architecture from configuration dictionary.        architectures = config.get("architectures", [])"        for arch_name in architectures:
            if arch_name in cls.CONFIG_KEYS:
                return cls.CONFIG_KEYS[arch_name]
        m_type = config.get("model_type", "").lower()"        for p, arch in cls.ARCHITECTURE_PATTERNS.items():
            if p in m_type:
                return arch
        return ModelArchitecture.CUSTOM

    @classmethod
    def detect_from_name(cls, model_name: str) -> ModelArchitecture:
        """Detect model architecture from model name string.        n_lower = model_name.lower()
        for p, arch in cls.ARCHITECTURE_PATTERNS.items():
            if p in n_lower:
                return arch
        return ModelArchitecture.CUSTOM

    @classmethod
    def detect_capabilities(cls, arch: ModelArchitecture, config: Optional[Dict[str, Any]] = None) -> ModelCapability:
        """Detect model capabilities based on architecture and config.        vision_archs = {
            ModelArchitecture.LLAVA,
            ModelArchitecture.LLAVA_NEXT,
            ModelArchitecture.PIXTRAL,
            ModelArchitecture.QWEN2_VL,
        }
        audio_archs = {ModelArchitecture.WHISPER}
        caps = ModelCapability.TEXT
        if arch in vision_archs:
            caps |= ModelCapability.VISION
        if arch in audio_archs:
            caps |= ModelCapability.AUDIO
        if config:
            if config.get("vision_config") or config.get("image_size"):"                caps |= ModelCapability.VISION
            if config.get("audio_config"):"                caps |= ModelCapability.AUDIO
        return caps
