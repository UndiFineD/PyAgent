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
Notification Channel - Enumeration of notification channel types

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Import the enum and compare or serialize channel values.
  Example:
    from src.core.base.notification_channel import NotificationChannel
    channel = NotificationChannel.SLACK
    if channel == NotificationChannel.SLACK:
        handle_slack(channel.value)
    # or construct from string:
    NotificationChannel("email")

WHAT IT DOES:
- Defines a lightweight enum, NotificationChannel, that centralizes canonical channel identifiers used across the codebase (slack, teams, email, webhook, discord) and exposes module __version__ from the project's VERSION.

WHAT IT SHOULD DO BETTER:
- Add richer metadata per channel (display name, default configuration keys, required credentials) and helper methods for normalization, validation, and serialization.
- Provide case-insensitive construction, explicit unit tests, and documentation linking enum members to channel-specific sender implementations or configuration entries.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_errors.py
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class NotificationChannel(Enum):
    """Notification channel types."""

    SLACK = "slack"
    TEAMS = "teams"
    EMAIL = "email"
    WEBHOOK = "webhook"
    DISCORD = "discord"
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class NotificationChannel(Enum):
    """Notification channel types."""

    SLACK = "slack"
    TEAMS = "teams"
    EMAIL = "email"
    WEBHOOK = "webhook"
    DISCORD = "discord"
