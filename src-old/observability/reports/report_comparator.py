#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/observability/reports/report_comparator.description.md

# Description: src/observability/reports/report_comparator.py

Module overview:
- `ReportComparator` compares two report contents and returns a `ReportComparison` with added/removed/unchanged counts.
- Uses simple line-item extraction for markdown lists to determine differences.

Behavioral notes:
- Default `reports_dir` uses project `src/` root.
- The `_extract_items` method looks for markdown list items starting with `- `.
## Source: src-old/observability/reports/report_comparator.improvements.md

# Improvements: src/observability/reports/report_comparator.py

Potential improvements:
- Add unit tests that compare real report snippets and verify reported diffs.
- Improve diff detection to handle markdown variations and ignore ordering when appropriate.
- Provide options to produce unified diffs or side-by-side comparisons as output.

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


r"""Auto-extracted class from generate_agent_reports.py"""
