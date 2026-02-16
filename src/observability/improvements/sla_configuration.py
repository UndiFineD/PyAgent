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
SLA Configuration - SLAConfiguration dataclass"""
# DATE: 2026-02-12"""
# AUTHOR: Keimpe de Jong
USAGE:
- Import and instantiate to centralize SLA parameters for an improvement/task:
  from src.core.improvements.sla_configuration import SLAConfiguration
  from src.core.improvements.sla_level import SLALevel
  cfg = SLAConfiguration(level=SLALevel.HIGH, max_hours=24, escalation_hours=6, notification_emails=["oncall@example.com"])
- Use cfg.max_hours, cfg.escalation_hours and cfg.notification_emails when determining deadlines, escalations and alert recipients.
- Persist or serialize via asdict(cfg) (dataclasses.asdict) or add explicit to_dict/from_dict helpers for storage/transport.

WHAT IT DOES:
- Defines a small, strongly-typed configuration object for Service Level Agreement parameters used by improvement workflows.
- Encapsulates SLA level (SLALevel), maximum resolution hours, escalation trigger hours, and notification email recipients.
- Exposes a simple dataclass structure that's trivial to instantiate, inspect, and pass through the codebase.

WHAT IT SHOULD DO BETTER:
- Add validation: ensure max_hours > 0, escalation_hours >= 0 and escalation_hours < max_hours, and validate email formats.
- Provide serialization helpers (to_dict/from_dict/JSON) and clear defaults for common SLA profiles to reduce caller boilerplate.
- Consider immutability (frozen dataclass) or explicit mutation methods, add type-checked collections (tuple[str, ...]) and runtime type enforcement, plus comprehensive unit tests and doc examples.
- Consider using timedelta for durations and timezone-aware handling if SLA logic later depends on business hours or calendar-awareness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from src.core.base.lifecycle.version import VERSION
from .sla_level import SLALevel

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
