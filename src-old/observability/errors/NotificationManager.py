#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/observability/errors/NotificationManager.description.md

# NotificationManager

**File**: `src\observability\errors\NotificationManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 101  
**Complexity**: 7 (moderate)

## Overview

Auto-extracted class from agent_errors.py

## Classes (1)

### `NotificationManager`

Manages error notifications to various channels.

Supports Slack, Teams, Email, Webhooks, and Discord notifications
with configurable severity thresholds.

Attributes:
    configs: List of notification configurations.

**Methods** (7):
- `__init__(self)`
- `add_config(self, config)`
- `remove_config(self, channel)`
- `notify(self, error)`
- `_format_message(self, error, template)`
- `_send(self, config, message)`
- `get_configs(self)`

## Dependencies

**Imports** (7):
- `ErrorEntry.ErrorEntry`
- `NotificationChannel.NotificationChannel`
- `NotificationConfig.NotificationConfig`
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/observability/errors/NotificationManager.improvements.md

# Improvements for NotificationManager

**File**: `src\observability\errors\NotificationManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 101 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `NotificationManager_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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

from src.core.base.version import VERSION
from .ErrorEntry import ErrorEntry
from .NotificationChannel import NotificationChannel
from .NotificationConfig import NotificationConfig
from typing import List
import logging

__version__ = VERSION


class NotificationManager:
    """Manages error notifications to various channels.

    Supports Slack, Teams, Email, Webhooks, and Discord notifications
    with configurable severity thresholds.

    Attributes:
        configs: List of notification configurations.
    """

    def __init__(self) -> None:
        """Initialize the notification manager."""
        self.configs: list[NotificationConfig] = []

    def add_config(self, config: NotificationConfig) -> None:
        """Add a notification configuration.

        Args:
            config: The notification configuration to add.
        """
        self.configs.append(config)

    def remove_config(self, channel: NotificationChannel) -> bool:
        """Remove a notification configuration by channel.

        Args:
            channel: The channel type to remove.

        Returns:
            True if removed, False if not found.
        """
        for i, cfg in enumerate(self.configs):
            if cfg.channel == channel:
                del self.configs[i]
                return True
        return False

    def notify(self, error: ErrorEntry) -> list[str]:
        """Send notifications for an error.

        Args:
            error: The error to notify about.

        Returns:
            List of channels that were notified.
        """
        notified: list[str] = []
        for config in self.configs:
            if not config.enabled:
                continue
            if error.severity.value >= config.min_severity.value:
                message = self._format_message(error, config.template)
                if self._send(config, message):
                    notified.append(config.channel.value)
        return notified

    def _format_message(self, error: ErrorEntry, template: str) -> str:
        """Format notification message from template."""
        return template.format(
            message=error.message,
            file=error.file_path,
            line=error.line_number,
            severity=error.severity.name,
            category=error.category.value,
        )

    def _send(self, config: NotificationConfig, message: str) -> bool:
        """Send a notification (stub for actual implementation)."""
        logging.info(f"Notification to {config.channel.value}: {message}")
        return True

    def get_configs(self) -> list[NotificationConfig]:
        """Get all notification configurations."""
        return self.configs
