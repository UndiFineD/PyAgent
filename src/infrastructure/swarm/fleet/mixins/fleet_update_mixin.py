
"""
Fleet update mixin.py module.
"""
# Copyright 2026 PyAgent Authors
# Phase 322: Fleet Autonomous Update Mixin

from __future__ import annotations

import subprocess
import threading
import time
from pathlib import Path

from src.observability.structured_logger import StructuredLogger

logger = StructuredLogger(__name__)


class FleetUpdateMixin:
    """
    Mixin for FleetManager to support autonomous periodic updates.
    Checks for repository updates every 15 minutes.
    """

    def init_update_service(self, interval_seconds: int = 900):
        """Initializes the periodic repository update cycle."""
        self._update_interval = interval_seconds
        self._updater_thread = threading.Thread(target=self._update_loop, name="FleetAutoUpdater", daemon=True)
        self._updater_thread.start()
        logger.info(f"FleetUpdateMixin: Auto-update service started with {interval_seconds}s interval.")

    def _update_loop(self):
        """Background thread loop for git operations."""
        # Initial short delay to let the system stabilize
        time.sleep(30)

        while not getattr(self, "kill_switch", False):
            try:
                self._run_git_pull()
            except (subprocess.SubprocessError, OSError, RuntimeError) as e:
                logger.error(f"FleetUpdateMixin: Update check failed: {e}")

            # Sleep in small increments to respond faster to kill_switch
            for _ in range(self._update_interval // 5):
                if getattr(self, "kill_switch", False):
                    break
                time.sleep(5)

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
                logger.info(f"FleetUpdateMixin: Successfully updated PyAgent.\n{result.stdout}")
                # Future: trigger post-update migration or reload logic
            else:
                # Common issue: local changes. We don't want to force pull and lose user work
                # unless explicitly requested, so we just log the failure.
                logger.error(f"FleetUpdateMixin: Git pull failed (exit {result.returncode}): {result.stderr}")

        except FileNotFoundError:
            logger.error("FleetUpdateMixin: 'git' command not found. Cannot perform auto-update.")
        except (subprocess.SubprocessError, OSError, ValueError) as e:
            logger.error(f"FleetUpdateMixin: Unexpected error during git pull: {e}")
