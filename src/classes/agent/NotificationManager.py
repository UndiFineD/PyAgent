#!/usr/bin/env python3

from __future__ import annotations
import logging
import time
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional

# Infrastructure
from src.classes.backend.LocalContextRecorder import LocalContextRecorder
from src.classes.base_agent.ConnectivityManager import ConnectivityManager

# Optional dependency
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    requests = None

class NotificationManager:
    """Manages event notifications via webhooks and internal callbacks."""

    def __init__(self, workspace_root: Optional[str] = None, recorder: Optional[LocalContextRecorder] = None) -> None:
        self.webhooks: List[str] = []
        self.callbacks: List[Callable[[str, Dict[str, Any]], None]] = []
        # Phase 108: Resilience management
        self.workspace_root = workspace_root
        self.recorder = recorder
        self.connectivity = ConnectivityManager(workspace_root)

    def _is_webhook_working(self, url: str) -> bool:
        import urllib.parse
        domain = urllib.parse.urlparse(url).netloc
        return self.connectivity.is_endpoint_available(domain or url)

    def _update_status(self, url: str, working: bool) -> None:
        import urllib.parse
        domain = urllib.parse.urlparse(url).netloc
        self.connectivity.update_status(domain or url, working)

    def register_webhook(self, url: str) -> None:
        self.webhooks.append(url)
        logging.info(f"Registered webhook: {url}")

    def register_callback(self, callback: Callable[[str, Dict[str, Any]], None]) -> None:
        self.callbacks.append(callback)
        name = getattr(callback, '__name__', repr(callback))
        logging.info(f"Registered callback: {name}")

    def notify(self, event_name: str, event_data: Dict[str, Any]) -> None:
        """Executes callbacks and sends webhooks for an event."""
        if self.recorder:
            self.recorder.record_lesson("event_notify", {"event": event_name, "data_keys": list(event_data.keys())})
        self._execute_callbacks(event_name, event_data)
        self._send_webhooks(event_name, event_data)

    def _execute_callbacks(self, event_name: str, event_data: Dict[str, Any]) -> None:
        for callback in self.callbacks:
            try:
                callback(event_name, event_data)
            except Exception as e:
                logging.warning(f"Callback failed: {e}")

    def _send_webhooks(self, event_name: str, event_data: Dict[str, Any]) -> None:
        if not HAS_REQUESTS or requests is None or not self.webhooks:
            return

        payload = {
            'event': event_name,
            'timestamp': time.time(),
            'data': event_data
        }

        for url in self.webhooks:
            if not self._is_webhook_working(url):
                continue

            try:
                # Fire and forget (ideally should be async or in a thread)
                response = requests.post(url, json=payload, timeout=5)
                response.raise_for_status()
                self._update_status(url, True)
            except Exception as e:
                logging.warning(f"Webhook failed for {url}: {e}")
                self._update_status(url, False)
                if self.recorder:
                    self.recorder.record_lesson("webhook_failure", {"url": url, "error": str(e)})
