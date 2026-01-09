#!/usr/bin/env python3

import subprocess
import logging
from pathlib import Path
from typing import List, Optional

class AgentGitHandler:
    """Handles git operations for the Agent."""
    
    def __init__(self, repo_root: Path, no_git: bool = False, recorder=None) -> None:
        self.repo_root = repo_root
        self.no_git = no_git
        self.recorder = recorder

    def _record(self, action: str, result: str, meta: Optional[dict] = None) -> None:
        """Internal helper to record git operations if recorder is available."""
        if self.recorder:
            self.recorder.record_interaction(
                provider="Git",
                model="cli",
                prompt=action,
                result=result,
                meta=meta
            )

    def commit_changes(self, message: str, files: Optional[List[str]] = None) -> None:
        """Commit changes to the repository."""
        if self.no_git:
            logging.info(f"Skipping git commit: no_git=True. Message: {message}")
            return

        try:
            if files:
                for file in files:
                    subprocess.run(["git", "add", file], cwd=self.repo_root, check=True, capture_output=True)
            else:
                subprocess.run(["git", "add", "."], cwd=self.repo_root, check=True, capture_output=True)

            # Check if there are changes to commit
            status = subprocess.run(["git", "status", "--porcelain"], cwd=self.repo_root, capture_output=True, text=True).stdout.strip()
            if not status:
                logging.info("No changes to commit.")
                return

            subprocess.run(["git", "commit", "-m", message], cwd=self.repo_root, check=True, capture_output=True)
            logging.info(f"Successfully committed changes: {message}")
            self._record(f"commit: {message}", "success", {"files": files})
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip() if e.stderr else str(e)
            logging.error(f"Git commit failed: {err_msg}")
            self._record(f"commit: {message}", f"failed: {err_msg}")
        except Exception as e:
            logging.error(f"Error during git commit: {e}")
            self._record(f"commit: {message}", f"error: {str(e)}")

    def create_branch(self, branch_name: str) -> None:
        """Create and switch to a new branch."""
        if self.no_git: return
        try:
            subprocess.run(["git", "checkout", "-b", branch_name], cwd=self.repo_root, check=True, capture_output=True)
            logging.info(f"Created branch: {branch_name}")
        except Exception as e:
            logging.error(f"Failed to create branch {branch_name}: {e}")
