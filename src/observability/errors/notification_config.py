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
notification_config.py - Defines NotificationConfig dataclass for error notification settings

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Import the dataclass and instantiate with desired channel, endpoint and optional settings:
  from src.core.base.errors.notification_config import NotificationConfig, NotificationChannel, ErrorSeverity
  cfg = NotificationConfig(channel=NotificationChannel.WEBHOOK, endpoint="https://hooks.example.com/abc", min_severity=ErrorSeverity.MEDIUM, enabled=True)
- Pass the NotificationConfig instance to whatever error-dispatching component or notifier the agent uses.
- Use cfg.template.format(message=err_msg, file=filename, line=lineno) to render notification text.

WHAT IT DOES:
- Provides a small, typed configuration container (dataclass) describing how error notifications are delivered.
- Encapsulates channel, destination endpoint, minimum severity that triggers notifications, enabled flag, and a simple message template.
- Centralizes notification-related defaults so notifiers can read a single object to decide whether and how to notify.

WHAT IT SHOULD DO BETTER:
- Validate the endpoint and channel combination (e.g., webhook URL format vs. email) and fail fast on invalid config.
- Support multiple endpoints and per-channel credential/headers (secure storage for API keys) rather than a single plaintext endpoint string.
- Allow richer templating (e.g., Jinja2) and include structured context (timestamps, run IDs), plus pluggable serializers and async delivery options.
- Emit introspection or schema metadata (e.g., to integrate with a config UI) and provide unit tests for edge cases like disabled notification flow.

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


"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

from .error_severity import ErrorSeverity
from .notification_channel import NotificationChannel

__version__ = VERSION


@dataclass
class NotificationConfig:
    """Configuration for error notifications.

    Attributes:
        channel: Notification channel type.
        endpoint: Webhook URL or email address.
        min_severity: Minimum severity to notify.
        enabled: Whether notifications are enabled.
        template: Message template.
    """

    channel: NotificationChannel
    endpoint: str
    min_severity: ErrorSeverity = ErrorSeverity.HIGH
    enabled: bool = True
    template: str = "Error: {message} in {file}:{line}"
"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

from .error_severity import ErrorSeverity
from .notification_channel import NotificationChannel

__version__ = VERSION


@dataclass
class NotificationConfig:
    """Configuration for error notifications.

    Attributes:
        channel: Notification channel type.
        endpoint: Webhook URL or email address.
        min_severity: Minimum severity to notify.
        enabled: Whether notifications are enabled.
        template: Message template.
    """

    channel: NotificationChannel
    endpoint: str
    min_severity: ErrorSeverity = ErrorSeverity.HIGH
    enabled: bool = True
    template: str = "Error: {message} in {file}:{line}"
