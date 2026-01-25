<<<<<<< HEAD
=======
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

"""Unit tests for local Ollama API connectivity."""
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor)

"""Unit tests for local Ollama API connectivity."""
import logging
import sys
import os
from pathlib import Path
from requests import Response

# Infrastructure
from src.infrastructure.backend.LLMClient import LLMClient
from src.core.base.ConnectivityManager import ConnectivityManager
from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder

def test_ollama() -> None:
    logging.basicConfig(level=logging.DEBUG)
    import requests
    
    workspace_root = Path(Path(__file__).resolve().parents[3])
    conn_manager = ConnectivityManager(str(workspace_root))
    recorder = LocalContextRecorder(workspace_root, "TestRunner")
    
    client = LLMClient(requests_lib=requests)
    
    print("Testing Ollama connectivity...")
    
    # Resilience: Check if Ollama is online using ConnectivityManager (15m TTL)
    endpoint = "http://localhost:11434/api/tags"
    if not conn_manager.is_endpoint_available(endpoint):
        print("Skipping Ollama test: cached offline.")
        return

    # Actually, let's just try to call it.
    prompt = "hi"
    model = "tinyllama"
    try:
        res: str = client.llm_chat_via_ollama(prompt=prompt, model=model)
        if res:
            print(f"Ollama Success! Response: {res}")
            # Intelligence Gap: Record the interaction
            recorder.record_interaction("ollama", model, prompt, res)
            conn_manager.update_status(endpoint, True)
        else:
            print("Ollama failed to respond (maybe model not downloaded?).")
            conn_manager.update_status(endpoint, False)
    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
        print(f"Ollama error: {e}")
        conn_manager.update_status(endpoint, False)
        
        print("Checking if we can reach the server at all...")
        try:
            resp: Response = requests.get(endpoint, timeout=5)
            print(f"Tags response: {resp.json()}")
            conn_manager.update_status(endpoint, True)
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            print(f"Could not reach Ollama server: {e2}")
            conn_manager.update_status(endpoint, False)

if __name__ == "__main__":
    test_ollama()
