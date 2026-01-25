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

"""Integration tests for agent webhooks."""

import sys
from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock


def load_agent_module() -> Any:
    repo_root = Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.append(str(repo_root))

    import src.core.base.lifecycle.base_agent as agent_module

    return agent_module


def test_webhooks_sent_on_run(monkeypatch, tmp_path) -> None:
    agent_mod = load_agent_module()
    try:
        Agent = agent_mod.BaseAgent
    except AttributeError:
        # If agent_mod is already the class or other issue, try direct import
        from src.core.base.lifecycle.base_agent import BaseAgent as Agent

    # Create a minimal repo root
    (tmp_path / "README.md").write_text("# repo")

    agent = Agent(file_path=str(tmp_path / "agent.py"))
    # register a webhook
    calls = []

    def fake_post(url: str, json: Dict[str, Any], timeout: int) -> MagicMock:
        calls.append({"url": url, "payload": json})

        class R:
            pass

        r = R()
        r.status_code = 200
        return r

    # Ensure requests is available in the module namespace
    try:
        import requests as _requests
    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
        _requests = None

    # Patch both the module and the requests module directly if it exists
    try:
        import requests as real_requests

        monkeypatch.setattr(real_requests, "post", fake_post)
    except ImportError:
        pass

    # Patch the Agent module where it's used
    import sys

    # Find the module in sys.modules
    agent_mod_internal = sys.modules.get("src.core.base.lifecycle.base_agent")
    if agent_mod_internal:
        monkeypatch.setattr(
            agent_mod_internal,
            "requests",
            type("M", (), {"post": staticmethod(fake_post)}),
        )
        monkeypatch.setattr(agent_mod_internal, "HAS_REQUESTS", True)

    agent.register_webhook("https://example.com/webhook")

    # Run agent (dry_run; no files to process)
    agent.run()

    webhook_call = next(
        (c for c in calls if c["url"] == "https://example.com/webhook"), None
    )
    assert webhook_call is not None, f"Webhook not found in calls: {calls}"
    assert webhook_call["payload"]["event"] == "agent_complete"
