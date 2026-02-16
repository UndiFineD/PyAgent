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

"""Notification tools for Slack and Discord webhooks."""

from __future__ import annotations

import contextlib
import logging

import requests

from src.core.base.lifecycle.version import VERSION
from src.core.base.logic.connectivity_manager import ConnectivityManager

__version__ = VERSION


def send_slack_notification(webhook_url: str, message: str) -> bool:
    """Sends a notification to a Slack webhook with connectivity caching."""
    cm = ConnectivityManager()
    if not cm.is_endpoint_available("slack_webhook"):
        logging.warning("Slack notification skipped: cached offline.")
        return False

    try:
        payload = {"text": message}
        response = requests.post(webhook_url, json=payload, timeout=30)
        response.raise_for_status()
        cm.update_status("slack_webhook", True)

        # Intelligence: Record outgoing notification (Phase 108)
        with contextlib.suppress(Exception):
            from src.infrastructure.compute.backend.local_context_recorder import \
                LocalContextRecorder

            recorder = LocalContextRecorder()

            recorder.record_interaction("Slack", "Webhook", f"Notification to {webhook_url}", message)

        return True

    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
        logging.error(f"Failed to send Slack notification: {e}")
        cm.update_status("slack_webhook", False)
        return False


def send_discord_notification(webhook_url: str, message: str) -> bool:
    """Sends a notification to a Discord webhook with connectivity caching."""
    cm = ConnectivityManager()
    if not cm.is_endpoint_available("discord_webhook"):
        logging.warning("Discord notification skipped: cached offline.")
        return False

    try:
        payload = {"content": message}
        response = requests.post(webhook_url, json=payload, timeout=30)
        response.raise_for_status()
        cm.update_status("discord_webhook", True)

        # Intelligence: Record outgoing notification (Phase 108)
        with contextlib.suppress(Exception):
            from src.infrastructure.compute.backend.local_context_recorder import \
                LocalContextRecorder

            recorder = LocalContextRecorder()
            recorder.record_interaction("Discord", "Webhook", f"Notification to {webhook_url}", message)

        return True
    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
        logging.error(f"Failed to send Discord notification: {e}")
        cm.update_status("discord_webhook", False)
        return False
