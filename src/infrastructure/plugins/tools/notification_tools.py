#!/usr/bin/env python3

"""Notification tools for Slack and Discord webhooks."""

import requests
import logging
from src.core.base.ConnectivityManager import ConnectivityManager

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
