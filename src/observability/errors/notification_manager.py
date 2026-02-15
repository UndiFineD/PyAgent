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
notification_manager.py - Error Notification Facade

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Preferred: from src.core.base.common import notification_manager; nm = notification_manager.NotificationManager()
- Alternate: from src.core.base.common.utils.notification_manager import NotificationManager
- Typical calls: nm.notify_error("message", exc=exception, context={"agent": "AgentName"}) or use nm.send(notification) depending on underlying API.

WHAT IT DOES:
Provides a concise public facade that re-exports the NotificationManager implementation from src.core.base.common.utils.notification_manager so callers can import a stable symbol from src.core.base.common.notification_manager; it centralizes the import path and surface area for error/alert notifications without adding runtime behavior.

WHAT IT SHOULD DO BETTER:
- Add a clear module-level docstring describing intent and public contract (expected NotificationManager methods and semantics).
- Document typical usage patterns and the expected notification payload shape (fields, optional context, severity levels).
- Consider exposing a lightweight factory/helper (e.g., get_global_notification_manager()) or lazy import to simplify tests and avoid circular imports; add unit tests and type hints for the re-export to improve discoverability.

FILE CONTENT SUMMARY:
Manager for error notifications.
(Facade for src.core.base.common.utils.notification_manager)
"""

from src.core.base.common.utils.notification_manager import NotificationManager

__all__ = ["NotificationManager"]
"""

from src.core.base.common.utils.notification_manager import NotificationManager

__all__ = ["NotificationManager"]
