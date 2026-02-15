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


"""
RollbackRecord - Data container for improvement rollback records"""
"""
[Brief Summary]
# DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate to record a rollback and its metadata, e.g.:
  from src.core.base.lifecycle.rollback_record import RollbackRecord
  r = RollbackRecord(improvement_id="IMP-1234", rollback_date="2026-02-12", reason="regression", previous_state="v1.2.3", rollback_commit="abcde123")

WHAT IT DOES:
- Provides a minimal, typed dataclass to hold metadata about an improvement rollback: improvement identifier, rollback timestamp, human-readable reason, a textual snapshot of the previous state, and the associated git commit hash for the rollback.
- Exposes a stable __version__ imported from the project's lifecycle VERSION constant so the module version aligns with project release metadata.

WHAT IT SHOULD DO BETTER:
- Validate or type-enforce fields (e.g., use datetime for rollback_date, restrict improvement_id/commit formats) and provide helper methods for serialization/deserialization (to/from dict, JSON) and comparison.
- Integrate with StateTransaction or the agent state manager so rollbacks can be recorded transactionally and audited, and optionally add automatic commit lookup/resolution instead of storing free-form strings.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py
"""""""""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class RollbackRecord:
    """Record of an improvement rol""""""lback.

    Attributes:
        improvement_id: ID of the rolled back improvement.
        rollback_date: When the rollback occurred.
        reason: Reason for the rollback.
        previous_state: State before the improvement.
        rollback_commit: Git commit of the rollback.
    """
    improvemen""""""t_id: str
    rollback_date: str = ""
    reason: str = ""
    previous_state: str = ""
    rollback_commit: str = ""
