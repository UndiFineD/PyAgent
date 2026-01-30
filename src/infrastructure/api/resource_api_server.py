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


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from src.infrastructure.api.resource.resource_manager import ResourceManager

app = FastAPI(title="PyAgent Resource API", description="Serves vLLM, Ollama, and NPU resources.")
manager = ResourceManager()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/vllm/infer")
async def vllm_infer(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    model = data.get("model", "meta-llama/Llama-3-8B-Instruct")
    system_prompt = data.get("system_prompt")
    result = manager.infer_vllm(prompt, model, system_prompt)
    return JSONResponse({"result": result})

@app.post("/ollama/infer")
async def ollama_infer(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    model = data.get("model", "glm-4.6:cloud")
    system_prompt = data.get("system_prompt")
    result = manager.infer_ollama(prompt, model, system_prompt)
    return JSONResponse({"result": result})

@app.post("/npu/task")
async def npu_task(request: Request):
    data = await request.json()
    task = data.get("task", "")
    result = manager.run_npu_task(task)
    return JSONResponse({"result": result})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
