#!/usr/bin/env python3

from __future__ import annotations
import logging
from typing import Any, Dict, Optional
from .LLMBackend import LLMBackend

class OllamaBackend(LLMBackend):
    """Ollama LLM Backend."""

    def chat(self, prompt: str, model: str, system_prompt: str = "You are a helpful assistant.", **kwargs) -> str:
        if not self._is_working("ollama"):
            logging.debug("Ollama skipped due to connection cache.")
            return ""

        import os
        base_url = kwargs.get("base_url") or os.environ.get("DV_OLLAMA_BASE_URL") or "http://localhost:11434"
        url = base_url.rstrip("/") + "/api/generate"
        payload = {
            "model": model,
            "system": system_prompt,
            "prompt": prompt,
            "stream": False
        }
        
        timeout_s = kwargs.get("timeout_s", 120)
        
        try:
            response = self.session.post(url, json=payload, timeout=timeout_s)
            response.raise_for_status()
            content = response.json().get("response", "")
            self._record("ollama", model, prompt, content, system_prompt=system_prompt)
            self._update_status("ollama", True)
            return content
        except Exception as e:
            # Lowered logging level for fallback-friendly behavior (Phase 123)
            logging.debug(f"Ollama call failed: {e}")
            self._update_status("ollama", False)
            self._record("ollama", model, prompt, f"ERROR: {str(e)}", system_prompt=system_prompt)
            return ""
