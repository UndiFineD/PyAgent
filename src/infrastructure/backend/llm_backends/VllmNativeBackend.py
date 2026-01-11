#!/usr/bin/env python3

from __future__ import annotations
import logging
from typing import Any, Dict, Optional
from .LLMBackend import LLMBackend

class VllmNativeBackend(LLMBackend):
    """vLLM Native Engine LLM Backend."""

    def chat(self, prompt: str, model: str, system_prompt: str = "You are a helpful assistant.", **kwargs) -> str:
        try:
            from ..VllmNativeEngine import VllmNativeEngine
            engine = VllmNativeEngine.get_instance(model_name=model or "meta-llama/Llama-3-8B-Instruct")
            if not engine.enabled:
                return ""
            
            result = engine.generate(prompt, system_prompt=system_prompt)
            if result:
                self._record("vllm_native", model or engine.model_name, prompt, result, system_prompt=system_prompt)
            return result
        except Exception as e:
            logging.debug(f"vLLM Native Engine unavailable: {e}")
            return ""
