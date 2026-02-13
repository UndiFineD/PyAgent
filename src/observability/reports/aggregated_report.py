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
Aggregated Report - Aggregate multiple report sources into a unified issues summary

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
Instantiate AggregatedReport with a list of source report paths or identifiers, append or extend combined_issues with CodeIssue instances, and read summary / generated_at for metadata; intended to be used by report generation and CI tooling that merges multiple static-analysis or agent-produced reports.

WHAT IT DOES:
Provides a simple dataclass container to hold a list of source paths, a combined list of CodeIssue objects, an aggregation summary dictionary, and a generated_at timestamp. It centralizes aggregated-report state so other modules (e.g., generate_agent_reports.py) can produce, persist, or render a unified report.

WHAT IT SHOULD DO BETTER:
Add methods for merging reports (deduplication, severity reconciliation), validation of source paths and CodeIssue instances, (de)serialization to/from JSON/YAML, richer summary statistics (counts by severity, file, rule), and explicit typing/constraints (use Protocols or TypedDict for summary). Consider immutability for exported reports, timezone-aware timestamps, and unit tests covering merge/conflict rules.

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


"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .code_issue import CodeIssue

__version__ = VERSION


@dataclass
class AggregatedReport:
    """Report aggregated from multiple sources.
    Attributes:
        sources: Source report paths.
        combined_issues: Combined issues from all sources.
        summary: Aggregation summary.
        generated_at: Generation timestamp.
    """

    sources: list[str] = field(default_factory=list)  # type: ignore[assignment]
    combined_issues: list[CodeIssue] = field(default_factory=list)  # type: ignore[assignment]
    summary: dict[str, Any] = field(default_factory=dict)  # type: ignore[assignment]
    generated_at: float = field(default_factory=time.time)  # type: ignore[assignment]
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .code_issue import CodeIssue

__version__ = VERSION


@dataclass
class AggregatedReport:
    """Report aggregated from multiple sources.
    Attributes:
        sources: Source report paths.
        combined_issues: Combined issues from all sources.
        summary: Aggregation summary.
        generated_at: Generation timestamp.
    """

    sources: list[str] = field(default_factory=list)  # type: ignore[assignment]
    combined_issues: list[CodeIssue] = field(default_factory=list)  # type: ignore[assignment]
    summary: dict[str, Any] = field(default_factory=dict)  # type: ignore[assignment]
    generated_at: float = field(default_factory=time.time)  # type: ignore[assignment]
