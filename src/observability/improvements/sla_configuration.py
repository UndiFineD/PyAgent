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
from src.core.base.version import VERSION
from .SLALevel import SLALevel
from dataclasses import dataclass, field
from typing import List

__version__ = VERSION

@dataclass
class SLAConfiguration:
    """SLA configuration for improvements.

    Attributes:
        level: SLA priority level.
        max_hours: Maximum hours to resolution.
        escalation_hours: Hours before escalation.
        notification_emails: Emails to notify.
    """
    level: SLALevel
    max_hours: int
    escalation_hours: int
    notification_emails: list[str] = field(default_factory=list)  # type: ignore[assignment]