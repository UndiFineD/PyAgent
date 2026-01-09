#!/usr/bin/env python3

from __future__ import annotations
import logging
import time
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional

# Optional dependency
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    requests = None

class NotificationManager:
    """Manages event notifications via webhooks and internal callbacks."""

    def __init__(self, workspace_root: Optional[str] = None) -> None:
        self.webhooks: List[str] = []
        self.callbacks: List[Callable[[str, Dict[str, Any]], None]] = []
        # Phase 108: Resilience Cache for Webhooks
        self.workspace_root = workspace_root
        self._status_file = Path(workspace_root) / "logs" / "webhook_status.json" if workspace_root else None
        self._cache_ttl = 900 # 15 minutes
        self._status_cache: Dict[str, Dict[str, Any]] = self._load_status()

    def _load_status(self) -> Dict[str, Any]:
        if self._status_file and self._status_file.exists():
            try:
                with open(self._status_file, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_status(self) -> None:
        if self._status_file:
            try:
                os.makedirs(self._status_file.parent, exist_ok=True)
                with open(self._status_file, "w") as f:
                    json.dump(self._status_cache, f)
            except Exception:
                pass

    def _is_webhook_working(self, url: str) -> bool:
        status = self._status_cache.get(url)
        if status:
            elapsed = time.time() - status.get("timestamp", 0)
            if elapsed < self._cache_ttl:
                return status.get("working", True)
        return True

    def _update_status(self, url: str, working: bool) -> None:
        self._status_cache[url] = {"working": working, "timestamp": time.time()}
        self._save_status()

    def register_webhook(self, url: str) -> None:
        self.webhooks.append(url)
        logging.info(f"Registered webhook: {url}")

    def register_callback(self, callback: Callable[[str, Dict[str, Any]], None]) -> None:
        self.callbacks.append(callback)
        name = getattr(callback, '__name__', repr(callback))
        logging.info(f"Registered callback: {name}")

    def notify(self, event_name: str, event_data: Dict[str, Any]) -> None:
        """Executes callbacks and sends webhooks for an event."""
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
