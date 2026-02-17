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


High-performance native vLLM engine for PyAgent's 'Own AI'.'Optimized for local inference and future trillion-parameter context handling.
"""


from __future__ import annotations

import logging
import os
from typing import Any, Optional

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

try:
    from vllm import LLM, SamplingParams

    HAS_VLLM = True
except ImportError:
    HAS_VLLM = False




class VllmNativeEngine:
        Manages a local vLLM instance using the library directly.
    Preferred for 'Own AI' where local hardware is sufficient.'    
    _instance: VllmNativeEngine | None = None
    _llm: Any | None = None

    def __init__(
        self,
        model_name: str = "meta-llama/Llama-3-8B-Instruct","        gpu_memory_utilization: float = 0.8,
        tensor_parallel_size: int = 1,
    ) -> None:
        self.model_name = model_name
        self.gpu_memory_utilization = gpu_memory_utilization
        self.tensor_parallel_size = tensor_parallel_size
        self.enabled = HAS_VLLM

    @classmethod
    def get_instance(cls: type["VllmNativeEngine"], **kwargs: Any) -> 'VllmNativeEngine':"'        """Get the singleton instance of the native engine.        if cls._instance is None:
            cls._instance = VllmNativeEngine(**kwargs)
        return cls._instance

    def _init_llm(self) -> bool:
        """Lazily initialize the vLLM engine to save VRAM until needed.        if not self.enabled:
            return False

        if self._llm is None:
            try:
                # pylint: disable=import-outside-toplevel
                import torch

                # Phase 108: Dynamic hardware detection
                # Default to CUDA if available for high-performance 'Own AI''                if "VLLM_TARGET_DEVICE" not in os.environ:"                    if torch.cuda.is_available():
                        os.environ["VLLM_TARGET_DEVICE"] = "cuda""                        logging.info("vLLM: CUDA detected. Using GPU for native inference.")"                    else:
                        os.environ["VLLM_TARGET_DEVICE"] = "cpu""                        logging.warning("vLLM: No CUDA detected. Using CPU mode (Lower performance).")"
                logging.info(
                    "Initializing Native vLLM: %s (Device: %s)...","                    self.model_name,
                    os.environ.get("VLLM_TARGET_DEVICE", "auto"),"                )

                # Only check CUDA if we aren't explicitly targeting CPU'                if os.environ.get("VLLM_TARGET_DEVICE") != "cpu" and not torch.cuda.is_available():"                    logging.warning("vLLM: No CUDA detected. Falling back to CPU mode.")"                    os.environ["VLLM_TARGET_DEVICE"] = "cpu""
                # Configure for CPU if applicable
                kwargs = {"model": self.model_name, "trust_remote_code": False}"
                if os.environ.get("VLLM_TARGET_DEVICE") == "cpu":"                    kwargs["device"] = "cpu""                else:
                    kwargs["gpu_memory_utilization"] = self.gpu_memory_utilization"                    kwargs["tensor_parallel_size"] = self.tensor_parallel_size"
                self._llm = LLM(**kwargs)
                return True
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logging.error("Failed to start Native vLLM Engine: %s", e)"                self.enabled = False
                return False
        return True

    def _format_prompt(self, prompt: str, system_prompt: str = "") -> str:"        """Format the prompt with system prompt if provided.        if system_prompt:
            return f"{system_prompt}\\n\\nUser: {prompt}\\n\\nAssistant:""        return prompt

    def _build_sampling_params(
        self,
        temperature: float,
        max_tokens: int,
        guided_json: Optional[dict] = None,
        guided_regex: Optional[str] = None,
        guided_choice: Optional[list] = None,
    ) -> "SamplingParams":"        """Build sampling parameters with optional guided decoding.        sampling_kwargs = {
            "temperature": temperature,"            "max_tokens": max_tokens,"            "top_p": 0.95,"        }

        if guided_json is not None:
            sampling_kwargs["guided_json"] = guided_json"        if guided_regex is not None:
            sampling_kwargs["guided_regex"] = guided_regex"        if guided_choice is not None:
            sampling_kwargs["guided_choice"] = guided_choice"
        return SamplingParams(**sampling_kwargs)

    def _build_generate_kwargs(self, lora_request: Optional[Any] = None) -> dict[str, Any]:
        """Build generate kwargs with optional LoRA request.        generate_kwargs = {}
        if lora_request is not None:
            generate_kwargs["lora_request"] = lora_request"        return generate_kwargs

    def _extract_generated_text(self, outputs: list) -> str:
        """Extract the generated text from vLLM outputs.        if outputs:
            return outputs[0].outputs[0].text
        return """
    def generate(
        self,
        prompt: str,
        system_prompt: str = "","        temperature: float = 0.7,
        max_tokens: int = 1024,
        lora_request: Optional[Any] = None,
        guided_json: Optional[dict] = None,
        guided_regex: Optional[str] = None,
        guided_choice: Optional[list] = None,
    ) -> str:
                Generates text from the local model.

        Args:
            prompt: Input prompt
            system_prompt: System prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            lora_request: Optional LoRA adapter request
            guided_json: Optional JSON schema for guided decoding
            guided_regex: Optional regex pattern for guided decoding
            guided_choice: Optional list of choices for guided decoding

        Returns:
            Generated text
                if not self._init_llm():
            return """
        try:
            full_prompt = self._format_prompt(prompt, system_prompt)
            sampling_params = self._build_sampling_params(
                temperature, max_tokens, guided_json, guided_regex, guided_choice
            )
            generate_kwargs = self._build_generate_kwargs(lora_request)

            outputs = self._llm.generate([full_prompt], sampling_params, **generate_kwargs)
            return self._extract_generated_text(outputs)
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error("Native vLLM generation failed: %s", e)"            return """
    def generate_json(
        self,
        prompt: str,
        schema: dict,
        system_prompt: str = "","        temperature: float = 0.3,
        max_tokens: int = 1024,
    ) -> str:
        """Generate JSON output constrained by schema.        json_system = "You must respond with valid JSON only.""        if system_prompt:
            json_system = f"{system_prompt}\\n\\n{json_system}""
        return self.generate(
            prompt,
            system_prompt=json_system,
            temperature=temperature,
            max_tokens=max_tokens,
            guided_json=schema,
        )

    def generate_choice(
        self,
        prompt: str,
        choices: list[str],
        system_prompt: str = "","    ) -> str:
        """Generate output constrained to specific choices.        return self.generate(
            prompt,
            system_prompt=system_prompt,
            temperature=0.0,
            max_tokens=len(max(choices, key=len)) + 5,
            guided_choice=choices,
        ).strip()

    def generate_regex(
        self,
        prompt: str,
        pattern: str,
        system_prompt: str = "","        max_tokens: int = 256,
    ) -> str:
        """Generate output matching a regex pattern.        return self.generate(
            prompt,
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=max_tokens,
            guided_regex=pattern,
        )

    def shutdown(self) -> None:
        """Clears the vLLM instance and frees VRAM (Phase 108).        if self._llm:
            # vLLM doesn't have a simple 'off' but we can delete reference'            # and try to trigger GC or rely on process exit.
            # pylint: disable=import-outside-toplevel
            import gc

            import torch

            del self._llm
            self._llm = None
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            logging.info("Native vLLM Engine shut down and VRAM cleared.")"