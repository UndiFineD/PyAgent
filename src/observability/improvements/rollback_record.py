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
from src.core.base.lifecycle.version import VERSION
from dataclasses import dataclass

__version__ = VERSION


@dataclass
class RollbackRecord:
    """Record of an improvement rollback.

    Attributes:
        improvement_id: ID of the rolled back improvement.
        rollback_date: When the rollback occurred.
        reason: Reason for the rollback.
        previous_state: State before the improvement.
        rollback_commit: Git commit of the rollback.
    """

    improvement_id: str
    rollback_date: str = ""
    reason: str = ""
    previous_state: str = ""
    rollback_commit: str = ""
