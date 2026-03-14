#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/observability/reports/report_generator.description.md

# Description: src/observability/reports/report_generator.py

Module overview:
- Implements `ReportGenerator`, which parses Python source files and generates description, error, and improvement reports.
- Handles deduplication, JSONL export, and a simple dashboard generator.

Primary class:
- `ReportGenerator`: orchestrates iterating .py files, parsing AST, running compile checks, and writing report markdown files.

Behavioral notes:
- Uses `StructuredLogger` for logging.
- Writes three markdown outputs per processed file: `{stem}.description.md`, `{stem}.errors.md`, `{stem}.improvements.md`.
- Skips unchanged files by comparing a SHA of the source.
## Source: src-old/observability/reports/report_generator.improvements.md

# Improvements: src/observability/reports/report_generator.py

Potential improvements:
- Add unit tests for parsing edge cases, large files, and files with syntax errors.
- Expose smaller helper methods as public utilities to make them more testable (e.g., `_try_parse_python`).
- Allow injecting a custom AST visitor or ruleset for project-specific checks.
- Improve performance by parallelizing file processing (use `concurrent.futures` or `asyncio` with IO-bound operations).
- Add richer metadata to exported JSONL (git author, last modified time) and make deduplication pluggable.
- Avoid writing to the same output directory as source to make reports clearer and to avoid accidental source pollution.

LLM_CONTEXT_END
"""
from __future__ import annotations


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


r"""Report generation logic for agent source files."""
