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
[Module Title] - SubscriptionFrequency enum for report scheduling

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- from src.core.models.subscription_frequency import SubscriptionFrequency
- use SubscriptionFrequency.IMMEDIATE / .HOURLY / .DAILY / .WEEKLY in subscription records or scheduling logic
- compare with value strings via .value or use in type hints: def schedule(freq: SubscriptionFrequency): ...

WHAT IT DOES:
- Defines a small Enum representing allowed report subscription frequencies
- Exposes module __version__ from src.core.base.lifecycle.version.VERSION so package tooling can detect the module version
- Keeps frequency values as simple lowercase strings for storage/serialization

WHAT IT SHOULD DO BETTER:
- Add a detailed module docstring and per-member docstrings explaining semantic differences (e.g., DAILY vs WEEKLY anchor times)
- Provide utility helpers mapping frequencies to concrete scheduling rules (cron expressions, timedelta) and timezone-aware semantics
- Add validation, unit tests, and integration with the scheduler service and serialization formats (JSON schema, DB enums) to avoid divergent string usages

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

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class SubscriptionFrequency(Enum):
    """Frequency for report subscriptions."""

    IMMEDIATE = "immediate"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class SubscriptionFrequency(Enum):
    """Frequency for report subscriptions."""

    IMMEDIATE = "immediate"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
