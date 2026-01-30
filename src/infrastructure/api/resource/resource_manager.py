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
ResourceManager: Unified interface for vLLM, Ollama, and NPU resources.
"""

from src.infrastructure.compute.backend.llm_backends.vllm_native_backend import VllmNativeBackend
from src.infrastructure.compute.backend.llm_backends.ollama_backend import OllamaBackend
# TODO: Add NPU backend import when available

class ResourceManager:
    def __init__(self):
        self.vllm = VllmNativeBackend()
        self.ollama = OllamaBackend()
        # self.npu = NPUBackend()  # Placeholder

    def infer_vllm(self, prompt, model="meta-llama/Llama-3-8B-Instruct", system_prompt=None):
        return self.vllm.chat(prompt, model, system_prompt or "You are a helpful assistant.")

    def infer_ollama(self, prompt, model="llama3", system_prompt=None):
        return self.ollama.chat(prompt, model, system_prompt or "You are a helpful assistant.")

    def run_npu_task(self, task):
        # TODO: Implement NPU logic
        return f"[NPU] Task result for: {task}"
