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
ResourceClient: Interacts with remote resource_api_server instances.
"""

import httpx

class ResourceClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(timeout=60.0)

    async def infer_vllm(self, prompt, model="meta-llama/Llama-3-8B-Instruct"):
        resp = await self.client.post(f"{self.base_url}/vllm/infer", json={"prompt": prompt, "model": model})
        return resp.json()

    async def infer_ollama(self, prompt, model="llama3"):
        resp = await self.client.post(f"{self.base_url}/ollama/infer", json={"prompt": prompt, "model": model})
        return resp.json()

    async def run_npu_task(self, task):
        resp = await self.client.post(f"{self.base_url}/npu/task", json={"task": task})
        return resp.json()
