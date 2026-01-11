#!/usr/bin/env python3

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class LLMBackend(ABC):
    """Base class for LLM backends."""
    
    def __init__(self, session: Any, connectivity_manager: Any, recorder: Any = None) -> None:
        self.session = session
        self.connectivity = connectivity_manager
        self.recorder = recorder

    @abstractmethod
    def chat(self, prompt: str, model: str, system_prompt: str = "You are a helpful assistant.", **kwargs) -> str:
        """Excecute a chat completion."""
        raise NotImplementedError()

    def _is_working(self, provider_id: str) -> bool:
        return self.connectivity.is_endpoint_available(provider_id)

    def _update_status(self, provider_id: str, working: bool) -> None:
        self.connectivity.update_status(provider_id, working)

    def _record(self, provider: str, model: str, prompt: str, result: str, system_prompt: str = "") -> None:
        if self.recorder:
            try:
                import time
                meta = {
                    "system_prompt": system_prompt,
                    "phase": 120,
                    "timestamp_unix": time.time()
                }
                self.recorder.record_interaction(provider, model, prompt, result, meta=meta)
            except Exception:
                pass
