#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Fleet update mixin.py module.
# Phase 322: Fleet Autonomous Update Mixin
"""

from __future__ import annotations

import subprocess
import threading
from pathlib import Path
from typing import Callable

from src.observability.structured_logger import StructuredLogger

logger = StructuredLogger(__name__)



class FleetUpdateMixin:
    """
    Mixin for FleetManager to support autonomous periodic updates.
    Checks for repository updates every 15 minutes.
    """
    def init_update_service(self, interval_seconds: int = 900, sleep_fn: Callable[[float], None] | None = None):
        """Initializes the periodic repository update cycle.
        `sleep_fn` may be supplied to make the background loop testable and
        interruptible. By default the mixin uses an internal `threading.Event`
        which allows a fast wake-up when `stop_update_service` is called.
        """
        self._update_interval = interval_seconds
        # Kill event allows responsive interruption of sleeps
        self._kill_event = threading.Event()
        if sleep_fn is None:
            def _wait(secs: float) -> None:
                self._kill_event.wait(secs)

            self._sleep_fn = _wait
        else:
            self._sleep_fn = sleep_fn

        self._updater_thread = threading.Thread(target=self._update_loop, name="FleetAutoUpdater", daemon=True)
        self._updater_thread.start()
        logger.info(f"FleetUpdateMixin: Auto-update service started with {interval_seconds}s interval.")

    def stop_update_service(self) -> None:
        """Stop the background update thread cleanly."""
        self._kill_event.set()
        self.kill_switch = True
        t = getattr(self, "_updater_thread", None)
        if t is not None and getattr(t, "is_alive", lambda: False)():
            try:
                t.join(timeout=2.0)
            except Exception:
                logger.debug("FleetUpdateMixin: updater thread did not join cleanly")


    def _update_loop(self):
        """Background thread loop for git operations."""
        # Initial short delay to let the system stabilize
        self._sleep_fn(30)

        while not getattr(self, "kill_switch", False) and not getattr(self, "_kill_event", threading.Event()).is_set():
            try:
                self._run_git_pull()
            except (subprocess.SubprocessError, OSError, RuntimeError) as e:
                logger.error(f"FleetUpdateMixin: Update check failed: {e}")
            # Sleep in small increments to respond faster to kill_switch
            for _ in range(max(1, self._update_interval // 5)):
                if getattr(self, "kill_switch", False) or getattr(self, "_kill_event", threading.Event()).is_set():
                    break
                self._sleep_fn(5)

    def _run_git_pull(self):
        """Executes the git pull command."""
        workspace_path = getattr(self, "workspace_root", Path.cwd())
        # Check if it's a git repo
        git_dir = workspace_path / ".git"
        if not git_dir.exists():
            logger.warning(f"FleetUpdateMixin: {workspace_path} is not a git repository. Skipping update.")
            return

        logger.info("FleetUpdateMixin: Checking for updates from https://github.com/UndiFineD/PyAgent...")
        try:
            # specifically pull from the repo requested by the user
            result = subprocess.run(
                ["git", "pull", "https://github.com/UndiFineD/PyAgent", "main"],
                cwd=str(workspace_path),
                capture_output=True,
                text=True,
                check=False,
            )

            if "Already up to date" in result.stdout:
                logger.info("FleetUpdateMixin: System is already up to date.")
            elif result.returncode == 0:
                logger.info(f"FleetUpdateMixin: Successfully updated PyAgent.\\n{result.stdout}")
                # Future: trigger post-update migration or reload logic
            else:
                # Common issue: local changes. We don't want to force pull and lose user work
                # # unless explicitly requested, so we just log the failure.
                logger.error(f"FleetUpdateMixin: Git pull failed (exit {result.returncode}): {result.stderr}")
        except FileNotFoundError:
            logger.error("FleetUpdateMixin: 'git' command not found. Cannot perform auto-update.")
        except (subprocess.SubprocessError, OSError, ValueError) as e:
            logger.error(f"FleetUpdateMixin: Unexpected error during git pull: {e}")
