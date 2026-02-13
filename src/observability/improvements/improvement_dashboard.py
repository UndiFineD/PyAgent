#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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


"""
Improvement Dashboard - Renders a lightweight improvements dashboard and emits update callbacks

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate ImprovementDashboard()
- Register listeners with on_update(callback: Callable[[], None])
- Call add_improvement(improvement: Improvement) to append an improvement and trigger callbacks
- Use render(improvements: list[Improvement]) -> str to produce a simple markdown list of improvements

WHAT IT DOES:
Provides a minimal in-memory dashboard object that holds Improvement instances, allows registration of zero-argument update callbacks, appends improvements, notifies listeners immediately, and renders a plain markdown summary listing improvement titles.

WHAT IT SHOULD DO BETTER:
- Make callback invocation robust: catch and log exceptions per-callback to avoid one failing listener stopping others.
- Add thread-safety (e.g., locks) for concurrent access to _callbacks and _improvements.
- Persist or snapshot improvements to disk or external store for durability across runs.
- Enhance render to include metadata (status, author, timestamps), configurable templates, and sorting/filtering.
- Provide more explicit typing, input validation, and unit tests for edge cases (empty lists, duplicate improvements).
- Add unsubscribe support for callbacks and limits on callback runtime to avoid blocking.

FILE CONTENT SUMMARY:
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


"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from collections.abc import Callable

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement

__version__ = VERSION


class ImprovementDashboard:
    """Renders a lightweight dashboard and emits update callbacks."""

    def __init__(self) -> None:
        self._callbacks: list[Callable[[], None]] = []
        self._improvements: list[Improvement] = []

    def on_update(self, callback: Callable[[], None]) -> None:
        self._callbacks.append(callback)

    def add_improvement(self, improvement: Improvement) -> None:
        self._improvements.append(improvement)
        for cb in list(self._callbacks):
            cb()

    def render(self, improvements: list[Improvement]) -> str:
        lines = ["# Improvements Dashboard"]
        for imp in improvements:
            lines.append(f"- {imp.title}")
        return "\n".join(lines)
"""

from __future__ import annotations

from collections.abc import Callable

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement

__version__ = VERSION


class ImprovementDashboard:
    """Renders a lightweight dashboard and emits update callbacks."""

    def __init__(self) -> None:
        self._callbacks: list[Callable[[], None]] = []
        self._improvements: list[Improvement] = []

    def on_update(self, callback: Callable[[], None]) -> None:
        self._callbacks.append(callback)

    def add_improvement(self, improvement: Improvement) -> None:
        self._improvements.append(improvement)
        for cb in list(self._callbacks):
            cb()

    def render(self, improvements: list[Improvement]) -> str:
        lines = ["# Improvements Dashboard"]
        for imp in improvements:
            lines.append(f"- {imp.title}")
        return "\n".join(lines)
