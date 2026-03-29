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
"""Unit tests for CortAgent: run_task, metadata, CortMixin injection, default config, re-entrancy.

All tests in this module are RED-phase: they fail at collection time because
``src.core.reasoning`` does not yet exist.  The correct failure reason is
``ModuleNotFoundError``, NOT an assertion error.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from src.core.reasoning import (
    DEFAULT_CORT_CONFIG,
    CortAgent,
    CortConfig,
    CortResult,
    EvaluationEngine,
)
from src.core.reasoning.CortAgent import CortMixin
from src.core.reasoning.CortCore import CortRecursionError

# ---------------------------------------------------------------------------
# TC-CA-01  CortAgent.run_task returns a CortResult
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_cort_agent_run_task_returns_cort_result() -> None:
    """CortAgent.run_task with a mock LLM returns a CortResult instance."""
    llm_mock = AsyncMock(return_value="mock answer text")
    agent = CortAgent(
        agent_id="agent-001",
        llm=llm_mock,
        config=CortConfig(n_rounds=1, m_alternatives=1),
    )
    result = await agent.run_task("What is 2 + 2?")
    assert isinstance(result, CortResult)


# ---------------------------------------------------------------------------
# TC-CA-02  CortResult.metadata.agent_id matches the agent's agent_id
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_cort_agent_metadata_has_agent_id() -> None:
    """CortResult.metadata.agent_id equals the agent_id passed to CortAgent."""
    llm_mock = AsyncMock(return_value="answer")
    agent_id = "my-agent-42"
    agent = CortAgent(
        agent_id=agent_id,
        llm=llm_mock,
        config=CortConfig(n_rounds=1, m_alternatives=1),
    )
    result = await agent.run_task("some prompt")
    assert result.metadata.agent_id == agent_id, (
        f"Expected metadata.agent_id='{agent_id}' but got '{result.metadata.agent_id}'"
    )


# ---------------------------------------------------------------------------
# TC-CA-03  CortMixin injects reason_with_cort into a mixed class
# ---------------------------------------------------------------------------


def test_cort_mixin_injects_into_base_agent() -> None:
    """A class that inherits CortMixin receives the reason_with_cort callable method."""

    class _StubBase:
        """Minimal stub acting as a BaseAgent stand-in for this test."""

        agent_id: str = "stub-agent"

    class AgentWithCort(_StubBase, CortMixin):
        """Test class combining cort mixin with the stub base."""

    method = getattr(AgentWithCort, "reason_with_cort", None)
    assert callable(method), "CortMixin must inject 'reason_with_cort' as a callable method"


# ---------------------------------------------------------------------------
# TC-CA-04  CortAgent without explicit config uses DEFAULT_CORT_CONFIG
# ---------------------------------------------------------------------------


def test_cort_agent_default_config() -> None:
    """CortAgent constructed without an explicit config uses DEFAULT_CORT_CONFIG."""
    llm_mock = AsyncMock(return_value="")
    agent = CortAgent(agent_id="test-default", llm=llm_mock)
    assert agent._cort_core.config == DEFAULT_CORT_CONFIG, (
        "CortAgent without explicit config must delegate to DEFAULT_CORT_CONFIG"
    )


# ---------------------------------------------------------------------------
# TC-CA-05  Calling reason_with_cort from within reason_with_cort raises CortRecursionError
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_cort_agent_reentrant_raises() -> None:
    """Calling reason_with_cort from within a reason_with_cort callback raises CortRecursionError."""
    nested_raised: list[bool] = [False]
    agent: CortAgent | None = None

    async def reentrant_llm(prompt: str, *, temperature: float, max_tokens: int) -> str:
        """Attempt a nested reason_with_cort call to trigger the recursion guard."""
        nonlocal agent
        try:
            assert agent is not None  # noqa: S101
            await agent.reason_with_cort("nested prompt")
        except CortRecursionError:
            nested_raised[0] = True
        except Exception:  # noqa: BLE001
            pass
        return "outer response"

    agent = CortAgent(
        agent_id="re-entrant-agent",
        llm=reentrant_llm,
        config=CortConfig(n_rounds=1, m_alternatives=1),
    )
    await agent.run_task("outer prompt")

    assert nested_raised[0], (
        "CortRecursionError must be raised when reason_with_cort is called re-entrantly on the same CortAgent instance"
    )


# ---------------------------------------------------------------------------
# TC-CA-06  CortAgent.run() accepts a non-dict string prompt (lines 128-131)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_cort_agent_run_task_string_input() -> None:
    """CortAgent.run() with a plain string (non-dict) exercises the else-branch of the abstract run() interface."""
    llm_mock = AsyncMock(return_value="gravity pulls objects together")
    agent = CortAgent(
        agent_id="run-string-agent",
        llm=llm_mock,
        config=CortConfig(n_rounds=1, m_alternatives=1),
    )
    # Call the BaseAgent abstract `run()` method directly with a non-dict string.
    # This exercises the `else str(task)` branch and lines 128-131 of CortAgent.py.
    result = await agent.run("explain gravity")
    assert result["ok"] is True
    assert isinstance(result["result"], CortResult)
