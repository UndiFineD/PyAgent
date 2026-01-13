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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Notification tools for Slack and Discord webhooks."""

from __future__ import annotations
from src.core.base.version import VERSION
import requests
import logging
from src.core.base.ConnectivityManager import ConnectivityManager

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
        try:
            from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder
            recorder = LocalContextRecorder()
            recorder.record_interaction("Slack", "Webhook", f"Notification to {webhook_url}", message)
        except Exception:
            pass

        return True
    except Exception as e:
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
        try:
            from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder
            recorder = LocalContextRecorder()
            recorder.record_interaction("Discord", "Webhook", f"Notification to {webhook_url}", message)
        except Exception:
            pass

        return True
    except Exception as e:
        logging.error(f"Failed to send Discord notification: {e}")
        cm.update_status("discord_webhook", False)
        return False