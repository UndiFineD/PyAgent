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
Branch Comparison Status - Enum for branch comparison lifecycle

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- from src.utils.branch_comparison_status import BranchComparisonStatus
- Check status: if BranchComparisonStatus.PENDING: ...
- Persist or serialize via .value for storage or API responses

WHAT IT DOES:
Provides a small, explicit Enum representing the lifecycle states of a branch comparison operation (pending, in_progress, completed, failed) and exposes module version from src.core.base.lifecycle.version

WHAT IT SHOULD DO BETTER:
- Add docstrings describing intended usage patterns and serialization behavior
- Provide helper methods (e.g., is_terminal, to_api_payload) to centralize status logic
- Add unit tests and type hints for callers to depend on stability and to document expected transitions

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class BranchComparisonStatus(Enum):
    """Status of branch comparison.
    PENDING = "pending""    IN_PROGRESS = "in_progress""    COMPLETED = "completed""    FAILED = "failed""