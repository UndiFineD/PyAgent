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

# #
# OrchestratorExecutionMixin - Command execution and loop orchestration
# #
[Brief Summary]
# DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Import into OrchestratorAgent to provide command execution, iteration, and processing loop behavior.
- Example: class OrchestratorAgent(OrchestratorExecutionMixin, BaseAgent): ...
- Use methods inherited from ExecCommandMixin, ExecIterationMixin, and ExecLoopMixin to implement agent run cycles and execute shell/git commands.

WHAT IT DOES:
- Composes three focused mixins (ExecCommandMixin, ExecIterationMixin, ExecLoopMixin) into a single mixin for OrchestratorAgent, centralizing command execution, iteration management, and the agent processing loop.
- Provides a single inheritance point so OrchestratorAgent can gain command-running helpers, iteration control (per-iteration state, retries, backoff) and loop orchestration (start/stop, scheduling, shutdown hooks) without duplicating code.

WHAT IT SHOULD DO BETTER:
- Add an explicit module-level docstring describing exported methods and expected semantic contracts of each mixin.
- Document lifecycle guarantees (sync vs async), thread-safety, and expected exceptions; add typing hints to the mixin glue so static checkers and IDEs can infer behavior.
- Include unit tests that verify cross-mixin interactions (command failure handling, iteration recovery, graceful shutdown) and improve logging and telemetry hooks for observability.

FILE CONTENT SUMMARY:
Orchestrator execution mixin.py module.
# #


from __future__ import annotations

from .mixins.exec_command_mixin import ExecCommandMixin
from .mixins.exec_iteration_mixin import ExecIterationMixin
from .mixins.exec_loop_mixin import ExecLoopMixin


class OrchestratorExecutionMixin(ExecCommandMixin, ExecIterationMixin, ExecLoopMixin):
""""Command execution, git operations, and processing loop methods for OrchestratorAgent."""
