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


OrchestratorExecutionMixin - Command execution and loop orchestration

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong

USAGE:
- Import into OrchestratorAgent to provide command execution, iteration, and processing loop behavior.
- Example: class OrchestratorAgent(OrchestratorExecutionMixin, BaseAgent): ...
- Use methods inherited from ExecCommandMixin, ExecIterationMixin, and ExecLoopMixin to implement agent run cycles and execute shell/git commands.

EXPORTED METHODS:
- run_command(command: str, *, cwd: str | None = None) -> str
- iterate_tasks(tasks: list, retries: int = 3) -> None
- start_loop() -> None
- stop_loop() -> None

SEMANTIC CONTRACTS:
- All methods are async and thread-safe.
- Exceptions raised: CommandExecutionError, IterationError, LoopTerminationError.
- Typing hints provided for all public methods.

LIFECYCLE GUARANTEES:
- Methods are coroutine-based (asyncio).
- Safe for concurrent invocation.

FILE CONTENT SUMMARY:
Orchestrator execution mixin.py module.

from __future__ import annotations

from .mixins.exec_command_mixin import ExecCommandMixin
from .mixins.exec_iteration_mixin import ExecIterationMixin
from .mixins.exec_loop_mixin import ExecLoopMixin

from typing import Any, Coroutine

class OrchestratorExecutionMixin(ExecCommandMixin, ExecIterationMixin, ExecLoopMixin):
    """Command execution, git operations, and processing loop methods for OrchestratorAgent.""""
    Methods:
        async def run_command(command: str, *, cwd: str | None = None) -> str
        async def iterate_tasks(tasks: list[Any], retries: int = 3) -> None
        async def start_loop() -> None
        async def stop_loop() -> None
    