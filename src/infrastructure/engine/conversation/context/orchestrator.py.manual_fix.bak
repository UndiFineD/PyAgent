#!/usr/bin/env python3
from __future__ import annotations

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
"""
Tool orchestrator for conversation engine (minimal, parser-safe).

"""
Provides a small, well-typed orchestrator used by tests to queue and run
tool executions. The real implementation is more feature-rich; this stub
preserves the public API sufficient for imports and basic unit tests.
"""
import asyncio
import time
from typing import Any, Callable, Dict, List, Optional

try:
    from .models import ContextConfig, ToolExecution, ToolExecutionPolicy
except Exception:  # pragma: no cover - fallback for tests
    class ContextConfig:
        def __init__(self) -> None:
            self.tool_policy = None
            self.max_parallel_tools = 4
            self.tool_timeout_seconds = 10

    class ToolExecution:
        def __init__(self, call_id: str, tool_name: str, arguments: Dict[str, Any]) -> None:
            self.call_id = call_id
            self.tool_name = tool_name
            self.arguments = arguments
            self.start_time = None
            self.end_time = None
            self.status = "pending"
            self.result = None
            self.error = None

    class ToolExecutionPolicy:
        PARALLEL = "parallel"
        SEQUENTIAL = "sequential"


class ToolOrchestrator:
    def __init__(self, config: Optional[ContextConfig] = None, tool_handler: Optional[Callable] = None) -> None:
        self.config = config or ContextConfig()
        self.tool_handler = tool_handler
        self._pending: Dict[str, ToolExecution] = {}
        self._completed: List[ToolExecution] = []

    @property
    def pending_count(self) -> int:
        return len(self._pending)

    @property
    def has_pending(self) -> bool:
        return self.pending_count > 0

    def queue_tool_call(self, call_id: str, tool_name: str, arguments: Dict[str, Any]) -> ToolExecution:
        execution = ToolExecution(call_id=call_id, tool_name=tool_name, arguments=arguments)
        self._pending[call_id] = execution
        return execution

    async def execute_pending(self) -> List[ToolExecution]:
        if not self._pending:
            return []
        policy = getattr(self.config, "tool_policy", None)
        if policy == ToolExecutionPolicy.PARALLEL:
            return await self._execute_parallel()
        return await self._execute_sequential()

    async def _execute_sequential(self) -> List[ToolExecution]:
        results: List[ToolExecution] = []
        for call_id, execution in list(self._pending.items()):
            await self._execute_one(execution)
            results.append(execution)
            self._completed.append(execution)
            del self._pending[call_id]
        return results

    async def _execute_parallel(self) -> List[ToolExecution]:
        max_parallel = getattr(self.config, "max_parallel_tools", 4)
        pending_list = list(self._pending.values())
        results: List[ToolExecution] = []
        for i in range(0, len(pending_list), max_parallel):
            batch = pending_list[i : i + max_parallel]
            tasks = [self._execute_one(ex) for ex in batch]
            await asyncio.gather(*tasks, return_exceptions=True)
            results.extend(batch)
        for ex in results:
            self._completed.append(ex)
            self._pending.pop(ex.call_id, None)
        return results

    async def _execute_one(self, execution: ToolExecution) -> None:
        execution.start_time = time.time()
        execution.status = "running"
        try:
            if self.tool_handler:
                if asyncio.iscoroutinefunction(self.tool_handler):
                    execution.result = await asyncio.wait_for(self.tool_handler(execution.tool_name, execution.arguments), timeout=getattr(self.config, "tool_timeout_seconds", 10))
                else:
                    execution.result = self.tool_handler(execution.tool_name, execution.arguments)
                execution.status = "completed"
            else:
                execution.error = "No tool handler configured"
                execution.status = "failed"
        except asyncio.TimeoutError:
            execution.error = "Tool execution timed out"
            execution.status = "failed"
        except Exception as e:
            execution.error = str(e)
            execution.status = "failed"
        finally:
            execution.end_time = time.time()

    def get_results(self) -> List[ToolExecution]:
        return list(self._completed)

    def clear_completed(self) -> None:
        self._completed.clear()
