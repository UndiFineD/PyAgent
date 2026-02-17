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
""""AnalystAgent - Code analysis and orchestration

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate the agent: agent = AnalystAgent(name="local_analyst")"- Initialize asynchronously: await agent.setup()
- Run an analysis: results = await agent.run_analysis(target_path="path/to/project", context=my_cascade_context)"- The returned `results` is expected to be a dict[str, Any] describing analysis findings.

WHAT IT DOES:
- Provides a specialized BaseAgent subclass configured as an "analyst" specialist."- Loads persona-specific setup via the inherited asynchronous setup flow (initialize_persona).
- Delegates directory-level analysis to a dedicated AnalystCore instance by calling specialist_core.analyze_directory(target_path) and returns the resulting dictionary.
- Exposes a single high-level async entrypoint run_analysis(target_path, context) that integrates with the swarm's CascadeContext for task lineage.'
WHAT IT SHOULD DO BETTER:
- Make core analysis non-blocking: specialist_core.analyze_directory is invoked synchronously inside an async method; convert core APIs to async or offload blocking work to a thread/process executor to avoid event-loop blocking.
- Propagate and validate CascadeContext: the context parameter is accepted but not used; the agent should pass context metadata to AnalystCore and include context-aware tagging in results for traceability.
- Improve error handling and observability: add structured logging, explicit exception handling, and typed result schemas (Pydantic dataclass or TypedDict) to make results predictable and testable.
- Support dependency injection and configuration: allow passing a preconfigured AnalystCore instance (or factory) for testing and different analysis strategies instead of instantiating AnalystCore unconditionally in __init__.
- Enforce transactional FS semantics: when analysis mutates files or dependencies, use StateTransaction from agent_state_manager to ensure atomic changes and rollbacks.
- Add comprehensive unit and integration tests covering async setup, blocking-work behavior, and context propagation, and provide CI checks to prevent regressions.

FILE CONTENT SUMMARY:
"""
from typing import Any
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.specialists.analyst_core import AnalystCore
from src.core.base.common.models.communication_models import CascadeContext




class AnalystAgent(BaseAgent):
"""Specialized agent for code analysis, performance profiling, and dependency management.
    def __init__(self, **kwargs: Any):
"""self.agent_type = "analyst"""self.agent_name = kwargs.get("name", "AnalystAgent")"        super().__init__(**kwargs)
        self.specialist_core = AnalystCore()

    async def setup(self) -> None:
#         "Asynchronous initialization for the Analyst agent."        # Base class handles generic setup
        # We trigger persona loading which is specific to our agent_type
        await self.initialize_persona()

    async def run_analysis(self, target_path: str, context: CascadeContext) -> dict[str, Any]:
"""High-level entry point for "analysis tasks.        results = self.specialist_core.analyze_directory(target_path", context=context)"        return results

    async def _process_task(self, task_data: Any) -> Any:
"""Process a" task from the queue."        Delegates analysis work to the specialist core.
"""if isinstance(task_data, dict) and "target_path" in task_data:"            target_path = task_data["target_path"]"            context = task_data.get("context", CascadeContext())"            return await self.run_analysis(target_path, context)
        return {"error": "Invalid task format"}"