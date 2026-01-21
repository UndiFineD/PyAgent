# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Tool execution orchestration.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any, Callable, Dict, List, Optional
from .models import ToolExecution, ContextConfig, ToolExecutionPolicy


class ToolOrchestrator:
    """Orchestrate tool execution within conversation."""

    def __init__(
        self,
        config: Optional[ContextConfig] = None,
        tool_handler: Optional[Callable] = None,
    ):
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

    def queue_tool_call(
        self,
        call_id: str,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> ToolExecution:
        """Queue a tool call for execution."""
        execution = ToolExecution(
            call_id=call_id,
            tool_name=tool_name,
            arguments=arguments,
        )
        self._pending[call_id] = execution
        return execution

    async def execute_pending(self) -> List[ToolExecution]:
        """Execute all pending tool calls."""
        if not self._pending:
            return []

        if self.config.tool_policy == ToolExecutionPolicy.PARALLEL:
            return await self._execute_parallel()
        else:
            return await self._execute_sequential()

    async def _execute_sequential(self) -> List[ToolExecution]:
        """Execute tools sequentially."""
        results = []
        for call_id, execution in list(self._pending.items()):
            await self._execute_one(execution)
            results.append(execution)
            self._completed.append(execution)
            del self._pending[call_id]
        return results

    async def _execute_parallel(self) -> List[ToolExecution]:
        """Execute tools in parallel."""
        max_parallel = self.config.max_parallel_tools
        pending_list = list(self._pending.values())
        results = []

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
        """Execute a single tool."""
        execution.start_time = time.time()
        execution.status = "running"

        try:
            if self.tool_handler:
                result = await self._call_handler(execution)
                execution.result = result
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

    async def _call_handler(self, execution: ToolExecution) -> Any:
        """Call the tool handler."""
        if asyncio.iscoroutinefunction(self.tool_handler):
            return await asyncio.wait_for(
                self.tool_handler(execution.tool_name, execution.arguments),
                timeout=self.config.tool_timeout_seconds,
            )
        else:
            return self.tool_handler(execution.tool_name, execution.arguments)

    def get_results(self) -> List[ToolExecution]:
        """Get completed tool executions."""
        return list(self._completed)

    def clear_completed(self) -> None:
        """Clear completed executions."""
        self._completed.clear()
