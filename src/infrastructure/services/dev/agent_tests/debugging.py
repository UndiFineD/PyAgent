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


"""Debugging utilities for test execution."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .enums import ExecutionMode
from .models import ExecutionTrace

__version__ = VERSION


def _empty_str_list() -> list[str]:
    return []


def _empty_action_list() -> list[dict[str, Any]]:
    return []


class ExecutionReplayer:
    """Replay test execution for debugging."""

    def __init__(self) -> None:
        """Initialize execution replayer."""
        self.traces: dict[str, ExecutionTrace] = {}
        self._current_recording: str | None = None
        self._step_index: dict[str, int] = {}

    def start_recording(self, test_id: str) -> ExecutionTrace:
        """Start recording test execution."""
        trace = ExecutionTrace(test_id=test_id, timestamp=datetime.now().isoformat())
        self.traces[test_id] = trace
        self._current_recording = test_id
        return trace

    def record_step(self, action: str, data: dict[str, Any] | None = None) -> None:
        """Record an execution step."""
        if not self._current_recording:
            return

        trace = self.traces.get(self._current_recording)
        if trace:
            step: dict[str, Any] = {
                "index": len(trace.steps),
                "timestamp": datetime.now().isoformat(),
                "action": action,
                "data": data or {},
            }
            trace.steps.append(step)

    def stop_recording(self) -> ExecutionTrace | None:
        """Stop recording and return the trace."""
        if not self._current_recording:
            return None

        trace = self.traces.get(self._current_recording)
        self._current_recording = None
        return trace

    def replay(
        self,
        test_id: str,
        mode: ExecutionMode = ExecutionMode.FULL_REPLAY,
        breakpoint_step: int = -1,
    ) -> list[dict[str, Any]]:
        """Replay a recorded execution."""
        trace = self.traces.get(test_id)

        if not trace:
            return []
        replayed: list[dict[str, Any]] = []
        for i, step in enumerate(trace.steps):
            if mode == ExecutionMode.BREAKPOINT and i == breakpoint_step:
                break
            replayed.append({"step": i, "action": step["action"], "replayed": True})
            if mode == ExecutionMode.STEP_BY_STEP:
                pass
        return replayed

    def get_step(self, test_id: str, step_index: int) -> dict[str, Any] | None:
        """Get a specific step from a trace."""
        trace = self.traces.get(test_id)
        if trace and 0 <= step_index < len(trace.steps):
            return trace.steps[step_index]

        return None

    def export_trace(self, test_id: str) -> str:
        """Export a trace to JSON."""
        trace = self.traces.get(test_id)
        if not trace:
            return "{}"

        return json.dumps(
            {
                "test_id": trace.test_id,
                "timestamp": trace.timestamp,
                "steps": trace.steps,
                "variables": trace.variables,
            },
            indent=2,
        )


class TestProfiler:
    """Runtime profiling for tests."""

    __test__ = False

    def __init__(self) -> None:
        """Initialize test profiler."""
        from .models import TestProfile

        self.profiles: dict[str, TestProfile] = {}
        self._start_times: dict[str, float] = {}

    def start_profiling(self, test_id: str) -> None:
        """Start profiling a test."""
        import time

        self._start_times[test_id] = time.time()

    def stop_profiling(
        self,
        test_id: str,
        memory_peak_mb: float = 0.0,
        io_operations: int = 0,
        function_calls: int = 0,
    ) -> Any:
        """Stop profiling and record results."""

        import time

        from .models import TestProfile

        start = self._start_times.pop(test_id, time.time())
        cpu_time = (time.time() - start) * 1000
        profile = TestProfile(
            test_id=test_id,
            cpu_time_ms=cpu_time,
            memory_peak_mb=memory_peak_mb,
            io_operations=io_operations,
            function_calls=function_calls,
            timestamp=datetime.now().isoformat(),
        )
        self.profiles[test_id] = profile
        return profile

    def get_slowest_tests(self, limit: int = 10) -> list[Any]:
        """Get the slowest tests."""
        sorted_profiles = sorted(self.profiles.values(), key=lambda p: p.cpu_time_ms, reverse=True)
        return sorted_profiles[:limit]

    def get_memory_heavy_tests(self, limit: int = 10) -> list[Any]:
        """Get tests with highest memory usage."""
        sorted_profiles = sorted(self.profiles.values(), key=lambda p: p.memory_peak_mb, reverse=True)
        return sorted_profiles[:limit]

    def generate_report(self) -> str:
        """Generate profiling report."""
        report = ["# Test Profiling Report\n"]
        report.append(f"Total profiled: {len(self.profiles)}\n")
        report.append("## Slowest Tests\n")
        for profile in self.get_slowest_tests(5):
            report.append(f"- `{profile.test_id}`: {profile.cpu_time_ms:.2f}ms, {profile.memory_peak_mb:.1f}MB")
        return "\n".join(report)


class TestRecorder:
    """Records test execution."""

    __test__ = False

    def __init__(self) -> None:
        self._active: TestRecorder.Recording | None = None

    @dataclass
    class Recording:
        """A recording of test actions."""

        test_name: str
        actions: list[dict[str, Any]] = field(default_factory=_empty_action_list)

    def start_recording(self, test_name: str) -> None:
        self._active = TestRecorder.Recording(test_name=test_name)

    def record_action(self, action_type: str, data: dict[str, Any]) -> None:
        if self._active is None:
            raise RuntimeError("Recording not started")
        self._active.actions.append({"type": action_type, "data": dict(data)})

    def stop_recording(self) -> TestRecorder.Recording:
        if self._active is None:
            raise RuntimeError("Recording not started")
        recording = self._active
        self._active = None
        return recording

    def record(self, test_name: str, result: bool) -> None:
        """Legacy record API."""
        if self._active is None:
            self.start_recording(test_name)
        self.record_action("result", {"passed": bool(result)})


class TestReplayer:
    """Replays recorded tests."""

    @dataclass
    class ReplayResult:
        """Result of a test replay."""

        success: bool
        errors: list[str] = field(default_factory=_empty_str_list)

    def replay(self, recording: Any) -> TestReplayer.ReplayResult:
        """Replay a recording."""
        actions = getattr(recording, "actions", None)
        if actions is None:
            return TestReplayer.ReplayResult(success=False, errors=["missing_actions"])
        return TestReplayer.ReplayResult(success=True)
