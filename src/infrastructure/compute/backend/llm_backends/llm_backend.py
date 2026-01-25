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

"""
Llm backend.py module.
"""


from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class LLMBackend(ABC):
    """Base class for LLM backends."""

    def __init__(self, session: Any, connectivity_manager: Any, recorder: Any = None) -> None:
        self.session = session
        self.connectivity = connectivity_manager
        self.recorder = recorder

    @abstractmethod
    def chat(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "You are a helpful assistant.",
        **kwargs,
    ) -> str:
        """Excecute a chat completion."""
        raise NotImplementedError()

    def _is_working(self, provider_id: str) -> bool:
        return self.connectivity.is_endpoint_available(provider_id)

    def _update_status(self, provider_id: str, working: bool) -> None:
        self.connectivity.update_status(provider_id, working)

    def _record(
        self,
        provider: str,
        model: str,
        prompt: str,
        result: str,
        system_prompt: str = "",
        latency_s: float | None = None,
    ) -> None:
        if self.recorder:
            try:
                import time

                meta = {
                    "system_prompt": system_prompt,
                    "phase": 120,
                    "latency_s": latency_s,
                    "timestamp_unix": time.time(),
                }
                self.recorder.record_interaction(provider, model, prompt, result, meta=meta)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                pass
