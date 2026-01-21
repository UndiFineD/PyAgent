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


"""Centralized connectivity management with TTL-based status caching."""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
import json
import logging
import time
import os
from pathlib import Path
from typing import Any

__version__ = VERSION


class ConnectivityManager:
    """Manages connection status for external APIs with persistent 15-minute TTL caching."""

    _instance = None

    def __new__(cls, *args, **kwargs) -> ConnectivityManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, workspace_root: str | None = None) -> None:
        # Only init once if it's a singleton
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.workspace_root = Path(workspace_root) if workspace_root else None
        self._conn_status_file = (
            self.workspace_root / "data/logs" / "connectivity_status.json"
            if self.workspace_root
            else None
        )
        self._ttl_success = 900  # 15 minutes for working endpoints
        self._ttl_failure = 120  # 2 minutes for failed endpoints (Phase 141 robustness)
        self._cache: dict[str, Any] = self._load_status()
        self._preferred_cache: dict[str, str] = self._cache.get("__preferred__", {})
        self._initialized = True

    def _load_status(self) -> dict[str, Any]:
        """Loads the connection status from disk."""
        if self._conn_status_file and self._conn_status_file.exists():
            try:
                with open(self._conn_status_file) as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_status(self) -> None:
        """Saves the connection status to disk."""
        if self._conn_status_file:
            try:
                os.makedirs(self._conn_status_file.parent, exist_ok=True)
                self._cache["__preferred__"] = self._preferred_cache
                with open(self._conn_status_file, "w") as f:
                    json.dump(self._cache, f)
            except Exception as e:
                logging.error(f"ConnectivityManager: Failed to save status: {e}")

    def get_preferred_endpoint(self, group: str) -> str | None:
        """Returns the last known working endpoint for a group if within TTL."""
        preferred = self._preferred_cache.get(group)
        if preferred and self.is_endpoint_available(preferred):
            return preferred
        return None

    def set_preferred_endpoint(self, group: str, endpoint_id: str) -> None:
        """Sets the preferred endpoint for a group."""
        if self._preferred_cache.get(group) != endpoint_id:
            self._preferred_cache[group] = endpoint_id
            self._save_status()

    def is_endpoint_available(self, endpoint_id: str) -> bool:
        """Checks if an endpoint is known to be available with differentiated TTLs (Phase 141)."""
        status = self._cache.get(endpoint_id)
        if status:
            elapsed = time.time() - status.get("timestamp", 0)
            is_working = status.get("working", False)

            target_ttl = self._ttl_success if is_working else self._ttl_failure

            if elapsed < target_ttl:
                if not is_working:
                    logging.debug(
                        f"ConnectivityManager: Skipping '{endpoint_id}' (cached offline, retrying in {int(target_ttl - elapsed)}s)"
                    )
                return is_working
        return True  # Default to True or if TTL expired

    def update_status(self, endpoint_id: str, working: bool) -> None:
        """Updates and persists the status for an endpoint."""
        status = self._cache.get(endpoint_id, {})
        status.update({"working": working, "timestamp": time.time()})
        self._cache[endpoint_id] = status
        self._save_status()

    def track_tps(self, endpoint_id: str, token_count: int, duration: float) -> None:
        """Tracks tokens per second for an endpoint (Phase 144)."""
        if duration <= 0:
            return

        tps = token_count / duration
        status = self._cache.get(endpoint_id, {})

        # Simple moving average (alpha 0.3)
        old_tps = status.get("avg_tps", tps)
        new_tps = (0.7 * old_tps) + (0.3 * tps)

        status["avg_tps"] = round(new_tps, 2)
        status["last_tps"] = round(tps, 2)
        status["total_tokens"] = status.get("total_tokens", 0) + token_count

        self._cache[endpoint_id] = status
        logging.debug(
            f"ConnectivityManager: Endpoint '{endpoint_id}' TPS tracked: {status['last_tps']} (avg: {status['avg_tps']})"
        )
        self._save_status()

    def get_tps_stats(self, endpoint_id: str) -> dict[str, Any]:
        """Returns TPS statistics for an endpoint."""
        status = self._cache.get(endpoint_id, {})
        return {
            "avg_tps": status.get("avg_tps", 0),
            "last_tps": status.get("last_tps", 0),
            "total_tokens": status.get("total_tokens", 0),
        }

    def is_online(self, endpoint: str) -> bool:
        """Compatibility alias for is_endpoint_available."""
        return self.is_endpoint_available(endpoint)

    def set_status(self, endpoint: str, online: bool) -> None:
        """Compatibility alias for update_status."""
        self.update_status(endpoint, online)

    def check_and_execute(
        self, endpoint_id: str, func: callable, *args, **kwargs
    ) -> Any:
        """Executes a function only if endpoint is available, updating status on failure."""
        if not self.is_endpoint_available(endpoint_id):
            return None

        try:
            result = func(*args, **kwargs)
            self.update_status(endpoint_id, True)
            return result
        except Exception as e:
            logging.warning(
                f"ConnectivityManager: Endpoint '{endpoint_id}' failed: {e}"
            )
            self.update_status(endpoint_id, False)
            raise e
