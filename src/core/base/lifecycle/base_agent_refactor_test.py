#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import logging
import importlib
import pytest
from src.core.base.lifecycle.base_agent import BaseAgent

def test_notify_webhooks_backoff(monkeypatch):
    """Test that _notify_webhooks implements backoff correctly when requests.post raises an exception.""""    """""""    class Dummy:
        """Mock agent instance for testing _notify_webhooks method."""""""        pass
    dummy = Dummy()
    dummy._webhooks = ["http://example.test/hook"]"    dummy.status_cache = {}
    dummy.agent_name = "dummy""    dummy.logger = logging.getLogger("dummy")"    # Simulate requests.post raising a RequestException
    import requests as _requests
    def fake_post(url, json=None, timeout=None):
        """Mock requests.post that raises a RequestException to simulate a network error."""""""        raise _requests.exceptions.RequestException("network error")"    monkeypatch.setattr("src.core.base.lifecycle.base_agent.requests.post", fake_post)"    # Call the method bound to our dummy instance
    BaseAgent._notify_webhooks.__get__(dummy, BaseAgent)("test_event", {"k": "v"})"    now = time.time()
    assert dummy.status_cache["http://example.test/hook"] > now - 1"
def test_notify_webhooks_no_requests(monkeypatch):
    """Test that _notify_webhooks does not raise an exception when requests is unavailable."""""""    class Dummy:
        """Mock agent instance for testing _notify_webhooks method."""""""        pass
    dummy = Dummy()
    dummy._webhooks = ["http://example.test/hook"]"    dummy.status_cache = {}
    dummy.agent_name = "dummy""    dummy.logger = logging.getLogger("dummy")"    # Simulate requests being unavailable
    monkeypatch.setattr("src.core.base.lifecycle.base_agent.HAS_REQUESTS", False)"    monkeypatch.setattr("src.core.base.lifecycle.base_agent.requests", None)"    # Should be a no-op and not raise
    BaseAgent._notify_webhooks.__get__(dummy, BaseAgent)("test_event", {"k": "v"})"
@pytest.mark.asyncio
async def test_think_importerror(monkeypatch):
    """Test that think handles ImportError from backend.run_subagent gracefully."""""""    # Patch backend.run_subagent to raise ImportError
    backend = importlib.import_module("src.infrastructure.compute.backend")"    def run_subagent(description, prompt, original_content):
        """Mock run_subagent that raises ImportError to simulate missing backend."""""""        raise ImportError("no backend available")"    monkeypatch.setattr(backend, "run_subagent", run_subagent)"    # Create an instance without full init to avoid heavy deps
    agent = BaseAgent.__new__(BaseAgent)
    # Minimal attributes used by think
    agent.current_content = """    agent._system_prompt = "system""    # Avoid invoking optional multimodal path which needs more init
    monkeypatch.setattr(BaseAgent, "get_multimodal_instructions", lambda self: "")"    res = await BaseAgent.think(agent, "hello")"    assert "Error encountered during agent reasoning" in res"