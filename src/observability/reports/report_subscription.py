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
ReportSubscription - Subscription model for report delivery

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate to represent a user's subscription: ReportSubscription(subscriber_id="user-123", email="me@example.com")
- Configure frequency and report types: frequency=SubscriptionFrequency.WEEKLY, report_types=[ReportType.SUMMARY]
- Use as a DTO for persistence, serialization (e.g., dataclasses.asdict), or delivery logic in report generation pipelines

WHAT IT DOES:
Defines a small dataclass representing a subscription for automated report delivery, including subscriber identity, delivery email, frequency (default DAILY), selected report types, file inclusion patterns, and an enabled flag.

WHAT IT SHOULD DO BETTER:
- Add input validation (email format, non-empty subscriber_id), immutability options, and richer typing (e.g., Sequence/Set for report_types and file_patterns).
- Provide convenience methods for serialization/deserialization, equality/keying for de-duplication, and secure handling of contact details.
- Integrate validation and lifecycle hooks (activation/expirations), tests, and documentation of expected ReportType values and pattern semantics.

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

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

from .report_type import ReportType
from .subscription_frequency import SubscriptionFrequency

__version__ = VERSION


@dataclass
class ReportSubscription:
    """Subscription for report delivery.
    Attributes:
        subscriber_id: Unique subscriber identifier.
        email: Email address for delivery.
        frequency: Delivery frequency.
        report_types: Types of reports to receive.
        file_patterns: Patterns for files to include.
        enabled: Whether subscription is active.
    """

    subscriber_id: str
    email: str
    frequency: SubscriptionFrequency = SubscriptionFrequency.DAILY
    report_types: list[ReportType] = field(default_factory=list)  # type: ignore[assignment]
    file_patterns: list[str] = field(default_factory=list)  # type: ignore[assignment]
    enabled: bool = True
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

from .report_type import ReportType
from .subscription_frequency import SubscriptionFrequency

__version__ = VERSION


@dataclass
class ReportSubscription:
    """Subscription for report delivery.
    Attributes:
        subscriber_id: Unique subscriber identifier.
        email: Email address for delivery.
        frequency: Delivery frequency.
        report_types: Types of reports to receive.
        file_patterns: Patterns for files to include.
        enabled: Whether subscription is active.
    """

    subscriber_id: str
    email: str
    frequency: SubscriptionFrequency = SubscriptionFrequency.DAILY
    report_types: list[ReportType] = field(default_factory=list)  # type: ignore[assignment]
    file_patterns: list[str] = field(default_factory=list)  # type: ignore[assignment]
    enabled: bool = True
