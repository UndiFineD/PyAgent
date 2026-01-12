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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_improvements.py"""



from .Improvement import Improvement
from .SLAConfiguration import SLAConfiguration
from .SLALevel import SLALevel
from .SLAPolicy import SLAPolicy

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, cast
import hashlib
import json
import logging
import re
import subprocess
import time



































class SLAManager:
    """Manages SLAs for improvements.

    Tracks SLA compliance and triggers escalations.

    Attributes:
        sla_configs: SLA configurations by level.
        tracked: Map of improvement IDs to SLA tracking data.
    """

    def __init__(self) -> None:
        """Initialize SLA manager."""
        self.sla_configs: Dict[SLALevel, SLAConfiguration] = {}
        self.tracked: Dict[str, Dict[str, Any]] = {}
        # Compatibility API expected by tests.
        self.sla_policies: Dict[str, SLAPolicy] = {}
        self._setup_default_slas()

    def set_policy(self, name: str, response_hours: int = 0, resolution_hours: int = 0) -> None:
        """Set a named SLA policy (compatibility API)."""
        self.sla_policies[name] = SLAPolicy(
            name=name,
            response_hours=int(response_hours or 0),
            resolution_hours=int(resolution_hours or 0),
        )

    def get_policy(self, name: str) -> Optional[SLAPolicy]:
        """Get a named SLA policy (compatibility API)."""
        return self.sla_policies.get(name)

    def check_violations(self, improvements: List[Improvement], priority: str) -> List[Improvement]:
        """Return improvements that violate the given named SLA policy."""
        policy = self.sla_policies.get(priority)
        if not policy or policy.resolution_hours <= 0:
            return []

        now = datetime.now()
        violating: List[Improvement] = []
        for imp in improvements:
            created = getattr(imp, "created_at", "")
            created_dt: Optional[datetime] = None
            if isinstance(created, datetime):
                created_dt = created
            else:
                try:
                    created_dt = datetime.fromisoformat(str(created))
                except Exception:
                    created_dt = None

            if not created_dt:
                continue

            age_hours = (now - created_dt).total_seconds() / 3600.0
            if age_hours > policy.resolution_hours:
                violating.append(imp)
        return violating

    def _setup_default_slas(self) -> None:
        """Set up default SLA configurations."""
        defaults = [
            (SLALevel.P0, 24, 12),
            (SLALevel.P1, 72, 48),
            (SLALevel.P2, 168, 120),
            (SLALevel.P3, 336, 240),
            (SLALevel.P4, 720, 480),
        ]
        for level, max_h, esc_h in defaults:
            self.sla_configs[level] = SLAConfiguration(
                level=level,
                max_hours=max_h,
                escalation_hours=esc_h
            )

    def assign_sla(
        self, improvement: Improvement, level: SLALevel
    ) -> None:
        """Assign an SLA to an improvement.

        Args:
            improvement: The improvement to track.
            level: SLA priority level.
        """
        config = self.sla_configs.get(level)
        if not config:
            return

        self.tracked[improvement.id] = {
            "level": level,
            "start_time": datetime.now().isoformat(),
            "deadline": (datetime.now() +
                         timedelta(hours=config.max_hours)).isoformat(),
            "escalation_time": (datetime.now() +
                                timedelta(hours=config.escalation_hours)).isoformat()
        }

    def check_sla_status(
        self, improvement_id: str
    ) -> Dict[str, Any]:
        """Check SLA status for an improvement."""
        if improvement_id not in self.tracked:
            return {"status": "not_tracked"}

        tracking = self.tracked[improvement_id]
        now = datetime.now().isoformat()

        if now > tracking["deadline"]:
            return {"status": "breached", **tracking}
        elif now > tracking["escalation_time"]:
            return {"status": "escalation_needed", **tracking}
        else:
            return {"status": "on_track", **tracking}

    def get_breached(self) -> List[str]:
        """Get all breached improvement IDs."""
        now = datetime.now().isoformat()
        return [
            imp_id for imp_id, tracking in self.tracked.items()
            if now > tracking["deadline"]
        ]

    def get_sla_compliance_rate(self) -> float:
        """Calculate SLA compliance rate."""
        if not self.tracked:
            return 100.0
        breached = len(self.get_breached())
        return ((len(self.tracked) - breached) / len(self.tracked)) * 100
