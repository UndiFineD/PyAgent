#!/usr/bin/env python3

from __future__ import annotations
import logging
from typing import Any, Dict, Optional
from .LLMBackend import LLMBackend

class VllmBackend(LLMBackend):
    """vLLM (OpenAI-compatible) LLM Backend."""

    def chat(self, prompt: str, model: str, system_prompt: str = "You are a helpful assistant.", **kwargs) -> str:
        if not self._is_working("vllm"):
            logging.debug("vLLM skipped due to connection cache.")
            return ""

        import os
        base_url = kwargs.get("base_url") or os.environ.get("DV_VLLM_BASE_URL") or "http://localhost:8000"
        url = base_url.rstrip("/") + "/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }
        
        timeout_s = kwargs.get("timeout_s", 60)
        
        try:
            response = self.session.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=timeout_s)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            self._record("vllm", model, prompt, content, system_prompt=system_prompt)
            self._update_status("vllm", True)
            return content
        except Exception as e:
            # Lowered logging level for fallback-friendly behavior (Phase 123)
            logging.debug(f"vLLM call failed: {e}")
            self._update_status("vllm", False)
            self._record("vllm", model, prompt, f"ERROR: {str(e)}", system_prompt=system_prompt)
            return ""
