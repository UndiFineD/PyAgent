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
"""CortAgent — agent wrapper and mixin for Chain-of-Recursive-Thoughts reasoning.

Provides:

* :class:`CortMixin` — a lightweight mixin that adds ``reason_with_cort()``
  to any class that also exposes ``self._cort_core``.
* :class:`CortAgent` — a :class:`~src.agents.BaseAgent` subclass that wires
  together an :class:`~src.core.reasoning.CortCore.CortCore` with a
  :class:`~src.core.reasoning.EvaluationEngine.EvaluationEngine` and exposes
  a simple ``run_task()`` entry point.
"""

from __future__ import annotations

from typing import Any

from src.agents.BaseAgent import AgentManifest, BaseAgent
from src.core.reasoning.CortCore import (
    DEFAULT_CORT_CONFIG,
    CortConfig,
    CortCore,
    CortResult,
    LlmCallable,
)
from src.core.reasoning.EvaluationEngine import EvaluationEngine

# ---------------------------------------------------------------------------
# CortMixin
# ---------------------------------------------------------------------------


class CortMixin:
    """Mixin that exposes ``reason_with_cort`` on any class with ``_cort_core``.

    The consuming class must provide a ``_cort_core`` attribute that is a
    :class:`~src.core.reasoning.CortCore.CortCore` instance.
    """

    async def reason_with_cort(self, prompt: str, **kwargs: Any) -> CortResult:
        """Run the CoRT reasoning loop for the given prompt.

        Args:
            prompt: The question or task to reason about.
            **kwargs: Additional keyword arguments (reserved for future use).

        Returns:
            A :class:`~src.core.reasoning.CortCore.CortResult` produced by
            the underlying :class:`~src.core.reasoning.CortCore.CortCore`.

        """
        core: CortCore = self._cort_core  # type: ignore[attr-defined]
        return await core.run(prompt)


# ---------------------------------------------------------------------------
# CortAgent
# ---------------------------------------------------------------------------


class CortAgent(BaseAgent, CortMixin):
    """A PyAgent agent that applies CoRT reasoning to every task.

    Combines :class:`~src.agents.BaseAgent.BaseAgent` lifecycle management
    with the :class:`CortMixin` to expose structured multi-round reasoning
    via ``run_task()``.

    Args:
        agent_id: Unique string identifier for this agent instance.
        llm: Async callable conforming to
            :class:`~src.core.reasoning.CortCore.LlmCallable`.
        config: Optional CoRT configuration.  Defaults to
            :data:`~src.core.reasoning.CortCore.DEFAULT_CORT_CONFIG` when
            ``None``.

    """

    def __init__(
        self,
        agent_id: str,
        llm: LlmCallable,
        config: CortConfig | None = None,
    ) -> None:
        """Initialise CortAgent with an agent_id, LLM, and optional config.

        Args:
            agent_id: Unique identifier used in task attribution metadata.
            llm: The language model callable used for chain generation.
            config: CoRT configuration; falls back to ``DEFAULT_CORT_CONFIG``.

        """
        manifest = AgentManifest(
            name="CortAgent",
            agent_id=agent_id,
        )
        super().__init__(manifest=manifest)
        self._llm = llm
        self._cort_core = CortCore(
            llm=llm,
            evaluator=EvaluationEngine(),
            config=config or DEFAULT_CORT_CONFIG,
        )

    async def run(self, task: dict[str, Any]) -> dict[str, Any]:
        """Implement the BaseAgent abstract interface via CoRT reasoning.

        Args:
            task: Task payload dictionary.  The prompt is read from the
                ``"prompt"`` key; falls back to ``str(task)`` if missing.

        Returns:
            A dictionary with ``"ok": True`` and ``"result"`` containing the
            :class:`~src.core.reasoning.CortCore.CortResult`.

        """
        prompt = task.get("prompt", str(task)) if isinstance(task, dict) else str(task)
        result = await self._cort_core.run(prompt)
        result.metadata.agent_id = self.agent_id
        return {"ok": True, "result": result}

    async def run_task(self, task: str) -> CortResult:
        """Execute a reasoning task using the CoRT pipeline.

        Args:
            task: The question or task prompt to reason about.

        Returns:
            A :class:`~src.core.reasoning.CortCore.CortResult` with the best
            chain, all rounds, and metadata including this agent's ID.

        """
        result = await self._cort_core.run(task)
        result.metadata.agent_id = self.agent_id
        return result


def validate() -> bool:
    """Validate that the CortAgent module is correctly configured.

    Returns:
        True when the module can be imported and the agent class is accessible.

    """
    assert CortAgent is not None
    return True
