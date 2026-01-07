#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from queue import PriorityQueue
from typing import Any, Callable, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import os
import re
import subprocess
import threading
import time
import uuid

class ConfigHotReloader:
    """Hot-reloads backend configuration without restart.

    Monitors configuration sources and applies changes dynamically.

    Example:
        reloader=ConfigHotReloader()
        reloader.set_config("timeout_s", 60)
        reloader.watch_env("DV_AGENT_TIMEOUT")

        # Config changes take effect immediately
        print(reloader.get_config("timeout_s"))
    """

    def __init__(self) -> None:
        """Initialize config hot reloader."""
        self._config: Dict[str, Any] = {}
        self._env_watches: Dict[str, str] = {}  # config_key -> env_var
        self._callbacks: List[Callable[[str, Any], None]] = []
        self._lock = threading.Lock()
        self._last_reload = time.time()

    def set_config(self, key: str, value: Any) -> None:
        """Set configuration value.

        Args:
            key: Configuration key.
            value: Configuration value.
        """
        with self._lock:
            old_value = self._config.get(key)
            self._config[key] = value

            if old_value != value:
                for callback in self._callbacks:
                    try:
                        callback(key, value)
                    except Exception as e:
                        logging.warning(f"Config callback error: {e}")

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key.
            default: Default if not found.

        Returns:
            Any: Configuration value.
        """
        self._check_env_changes()

        with self._lock:
            return self._config.get(key, default)

    def watch_env(self, env_var: str, config_key: Optional[str] = None) -> None:
        """Watch environment variable for changes.

        Args:
            env_var: Environment variable name.
            config_key: Config key to update (defaults to env_var).
        """
        with self._lock:
            self._env_watches[config_key or env_var] = env_var

        # Load initial value
        value = os.environ.get(env_var)
        if value is not None:
            self.set_config(config_key or env_var, value)

    def _check_env_changes(self) -> None:
        """Check for environment variable changes."""
        with self._lock:
            for config_key, env_var in self._env_watches.items():
                env_value = os.environ.get(env_var)
                if env_value is not None and self._config.get(config_key) != env_value:
                    self._config[config_key] = env_value
                    logging.debug(f"Config hot-reloaded: {config_key} from {env_var}")

    def on_change(self, callback: Callable[[str, Any], None]) -> None:
        """Register callback for config changes.

        Args:
            callback: Function(key, value) called on changes.
        """
        with self._lock:
            self._callbacks.append(callback)

    def reload_all(self) -> int:
        """Force reload all watched configs.

        Returns:
            int: Number of configs reloaded.
        """
        count = 0
        with self._lock:
            for config_key, env_var in self._env_watches.items():
                env_value = os.environ.get(env_var)
                if env_value is not None:
                    self._config[config_key] = env_value
                    count += 1
            self._last_reload = time.time()
        return count
