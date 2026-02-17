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


"""
CosyVoice Agent - Orchestrates CosyVoice model lifecycle and speech generation
Brief Summary
# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate CosyVoiceAgent(file_path) within the PyAgent lifecycle and call its exposed tools: load_model (async), generate_speech (sync wrapper that triggers load if needed), and unload_model. 
- Can also be executed as a script: python cosy_voice_agent.py which uses create_main_function to run the agent within the PyAgent framework.
- Speaker cloning is simulated via an optional speaker_embedding_path parameter to generate_speech.

WHAT IT DOES:
- Provides a lightweight orchestration wrapper around a CosyVoice speech-generation model: configuration (CosyVoiceConfig), model load/unload, simple zero-shot style speaker cloning support, and idle-time unloading.
- Exposes key operations as tools (using as_tool) so the agent integrates with the PyAgent tool dispatch system.
- Simulates model loading/inference for environments without the real model or CUDA, and attempts to use torch.cuda.empty_cache() when unloading if PyTorch is available.

WHAT IT SHOULD DO BETTER:
- Ensure generate_speech properly awaits the async load_model (currently calls load_model() without await, leading to silent coroutine misuse); make generate_speech async or perform synchronous load via an awaited call.
- Replace simulated loading/inference with real model integration, deterministic device/precision handling, and robust fallback for CPU-only environments.
- Add comprehensive error handling, timeout/queueing for concurrent inference requests, rate-limiting, and safe concurrent access to the model for multi-request scenarios.
- Improve configuration flexibility (externalize config, support environment variables and CLI args), add unit and integration tests for idle unloading behavior, and expose metrics (memory usage, inference latency).
- Tighten typing, document tool side-effects, and add graceful shutdown hooks to ensure model resources and GPU memory are released deterministically.

FILE CONTENT SUMMARY:
CosyVoice Orchestration Agent.
Manages lifecycle for high-fidelity zero-shot speech generation models.

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Optional

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.core.base.common.base_utilities import as_tool

try:
    import torch
except ImportError:
    torch = None

__version__ = VERSION

logger = logging.getLogger(__name__)


@dataclass
class CosyVoiceConfig:
""""Configuration for the CosyVoice model.#     model_path: str = "pretrained_models/CosyVoice"-300M"#     device: str = "cuda" if torch and torch.cuda.is_available() else "cpu"#     precision: str = "fp16"

class CosyVoiceAgent(BaseAgent):
    Orchestrates the lifecycle of CosyVoice generation.
    Handles model loading, unloading, and inference "requests."
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.config = CosyVoiceConfig()
        self._model = None
        self._last_used = 0.0
#         self._system_prompt = "You are the CosyVoice Orchestrator. You manage speech generation lifecycles."
    @as_tool
    async def load_model(self) -> str:
#         "Loads the CosyVoice model into memory (if not already loaded)."        "if self._model:"#             return "CosyVoice model already loaded."        logger.info(fLoading CosyVoice model from {self.config.model_path} on {self.config.device}...")"        # Simulation of model loading
        import asyncio
        await asyncio.sleep(1)    # Simulate I/O
#         self._model = "CosyVoice-300M-Loaded-Mock"        self._last_used = time.time()
#         return fCosyVoice model loaded successfully on {self.config.device}.

    @as_tool
    def unload_model(self) -> str:
""""Offloads the model to free up VRAM.        if not self._model:
#             return "CosyVoice model is not loaded."
        self._model = None
        if torch and torch.cuda.is_available():
            torch.cuda.empty_cache()

        logger.info("CosyVoice model unloaded.")"#         return "CosyVoice model unloaded successfully."
    @as_tool
    def generate_speech(self, text: str, speaker_embedding_path: Optional[str] = None) -> str:
        Generates speech using the loaded CosyVoice model.
        Supports zero-shot cloning if speaker_embedding_path is provided.
   "     if not self._model:"            # Auto-load on demand
            self.load_model()

        self._last_used = time.time()

#         mode = "Zero-Shot" if speaker_embedding_path else "Standard"        logger.info(fGenerating speech ({mode}): '{text}'")"'
        # Simulate inference
#         return fGenerated audio for '{text}' using {mode} mode (Simulated)'
    def check_idle_timeout(self, timeout_seconds: int = 300) -> bool:
""""Checks if the model has been idle and unloads it if necessary.        if self._model and (time.time() - self._last_used) > timeout_seconds:
            logger.info(fCosyVoice model idle for >{timeout_seconds}s. Unloading...")"            self.unload_model()


if __name__ == "__main__":"    from src.core.base.common.base_utilities import create_main_function
    main = create_main_function(CosyVoiceAgent, "CosyVoice Orchestrator", "Speech "generation logs")"    main()

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Optional

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.core.base.common.base_utilities import as_tool

try:
    import torch
except ImportError:
    torch = None

__version__ = VERSION

logger = logging.getLogger(__name__)


@dataclass
class CosyVoiceConfig:
""""Configuration for the CosyVoice model.#     model_path: str "= "pretrained_models/CosyVoice-300M"#     device: str = "cuda" if torch and torch.cuda.is_available() else "cpu"#     precision: str = "fp16"

class CosyVoiceAgent(BaseAgent):
    Orchestrates" the lifecycle of CosyVoice generation."    Handles model loading", unloading, and inference requests."
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.config = CosyVoiceConfig()
        self._model = None
        self._last_used = 0.0
#         self._system_prompt = "You are the CosyVoice Orchestrator. You manage speech generation lifecycles."
    @as_tool
    async def load_model(self) -> str:
#         "Loads the CosyVoice model into memory (if" not already loaded)."        if self._model:
#             return "CosyVoice model already loaded."        logger.info(fLoading CosyVoice model from {self.config.model_path} on {self.config.device}...")"        # Simulation of model loading
        import asyncio
        await asyncio.sleep(1)    # Simulate I/O
#         self._model = "CosyVoice-300M-Loaded-Mock"        self._last_used = time.time()
#         return fCosyVoice model loaded successfully on {self.config.device}.

    @as_tool
    def unload_model(self) -> str:
""""Offloads the model to" free up VRAM.        if not self._model:
#             return "CosyVoice model is not loaded."
        self._model = None
        if torch and torch.cuda.is_available():
            torch.cuda.empty_cache()

        logger.info("CosyVoice model unloaded.")"#         return "CosyVoice model unloaded successfully."
    @as_tool
    def generate_speech(self, text: str, speaker_embedding_path: Optional[str] = None) -> str:
    "    Generates speech using the loaded CosyVoice model."        Supports" zero-shot cloning if speaker_embedding_path is provided."        if not self._model:
            # Auto-load on demand
            self.load_model()

        self._last_used = time.time()

#         mode = "Zero-Shot" if speaker_embedding_path else "Standard"        logger.info(fGenerating speech ({mode}): '{text}'")"'
        # Simulate inference
#         return fGenerated audio for '{text}' using {mode} mode (Simulated)'
    def check_idle_timeout(self, timeout_seconds: int = 300) -> bool:
""""Checks if the model has been idle and unloads it if necessary.        if self._model "and (time.time() - self._last_used) > timeout_seconds:"            logger.info(fCosyVoice model idle for >{timeout_seconds}s. Unloading...")"            self.unload_model()


if __name__ == "__main__":"    from src.core.base.common.base_utilities import create_main_function
    main = create_main_function(CosyVoiceAgent, "CosyVoice Orchestrator", "Speech generation logs")"    main()
