#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
High-performance native vLLM engine for PyAgent's 'Own AI'.
Optimized for local inference and future trillion-parameter context handling.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from typing import Any
import os

__version__ = VERSION

try:
    from vllm import LLM, SamplingParams
    HAS_VLLM = True
except ImportError:
    HAS_VLLM = False







class VllmNativeEngine:
    """
    Manages a local vLLM instance using the library directly.
    Preferred for 'Own AI' where local hardware is sufficient.
    """
    _instance: VllmNativeEngine | None = None
    _llm: Any | None = None

    def __init__(self, model_name: str = "meta-llama/Llama-3-8B-Instruct",
                 gpu_memory_utilization: float = 0.8,
                 tensor_parallel_size: int = 1) -> None:
        self.model_name = model_name
        self.gpu_memory_utilization = gpu_memory_utilization
        self.tensor_parallel_size = tensor_parallel_size
        self.enabled = HAS_VLLM

    @classmethod
    def get_instance(cls, **kwargs) -> VllmNativeEngine:
        if cls._instance is None:
            cls._instance = VllmNativeEngine(**kwargs)
        return cls._instance

    def _init_llm(self) -> bool:
        """Lazily initialize the vLLM engine to save VRAM until needed."""
        if not self.enabled:
            return False

        if self._llm is None:
            try:
                import torch
                # Phase 108: Dynamic hardware detection
                # Default to CUDA if available for high-performance 'Own AI'
                if "VLLM_TARGET_DEVICE" not in os.environ:
                    if torch.cuda.is_available():
                        os.environ["VLLM_TARGET_DEVICE"] = "cuda"
                        logging.info("vLLM: CUDA detected. Using GPU for native inference.")
                    else:
                        os.environ["VLLM_TARGET_DEVICE"] = "cpu"
                        logging.warning("vLLM: No CUDA detected. Using CPU mode (Lower performance).")

                logging.info(f"Initializing Native vLLM: {self.model_name} (Device: {os.environ.get('VLLM_TARGET_DEVICE', 'auto')})...")

                import torch
                # Only check CUDA if we aren't explicitly targeting CPU
                if os.environ.get("VLLM_TARGET_DEVICE") != "cpu" and not torch.cuda.is_available():
                    logging.warning("vLLM: No CUDA detected. Falling back to CPU mode.")
                    os.environ["VLLM_TARGET_DEVICE"] = "cpu"

                # Configure for CPU if applicable
                kwargs = {
                    "model": self.model_name,
                    "trust_remote_code": True
                }

                if os.environ.get("VLLM_TARGET_DEVICE") == "cpu":
                    kwargs["device"] = "cpu"
                else:
                    kwargs["gpu_memory_utilization"] = self.gpu_memory_utilization
                    kwargs["tensor_parallel_size"] = self.tensor_parallel_size

                self._llm = LLM(**kwargs)
                logging.info("Native vLLM Engine started successfully.")
            except Exception as e:
                logging.error(f"Failed to start Native vLLM Engine: {e}")
                self.enabled = False
                return False
        return True

    def generate(self, prompt: str, system_prompt: str = "",
                 temperature: float = 0.7, max_tokens: int = 1024) -> str:
        """Generates text from the local model."""
        if not self._init_llm():
            return ""

        try:
            # Format according to chat templates if possible, or simple concat
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nAssistant:" if system_prompt else prompt

            sampling_params = SamplingParams(
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.95
            )

            outputs = self._llm.generate([full_prompt], sampling_params)

            if outputs:
                return outputs[0].outputs[0].text
            return ""
        except Exception as e:
            logging.error(f"Native vLLM generation failed: {e}")
            return ""

    def shutdown(self) -> None:
        """Clears the vLLM instance and frees VRAM (Phase 108)."""
        if self._llm:
            # vLLM doesn't have a simple 'off' but we can delete reference
            # and try to trigger GC or rely on process exit.
            import gc
            import torch
            del self._llm
            self._llm = None
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            logging.info("Native vLLM Engine shut down and VRAM cleared.")
