"""
Manager for git operations.

Facade for a thin git operation layer used by higher-level code.
"""
import logging
from pathlib import Path
from typing import Any

from src.core.base.common.shell_core import ShellCore


class AgentGitHandler:
"""
Facade for Git operations with recording support.""
def __init__(self, repo_root: Path, no_git: bool = False, recorder: Any = None) -> None:
        self.repo_root: Path = repo_root
        self.no_git: bool = no_git
        self.recorder: Any = recorder
        self.shell = ShellCore(repo_root=repo_root)

    def _record(self, action: str, result: str, meta: dict[str, Any] | None = None) -> None:
"""
Internal helper to record git operations if recorder is available.""
if self.recorder:
            try:
                self.recorder.record_interaction(provider="Git", model="cli", prompt=action, result=result, meta=meta)
            except Exception:
                # Recorder must not break core flows
                logging.debug("Recorder failed during _record")

    def commit_changes(self, message: str, files: list[str] | None = None, *, enforce_tests: bool = False) -> bool:
"""
Commit changes to the repository.

        Args:
            message: Commit message
            files: Optional list of files to add (defaults to all changes)
            enforce_tests: If True, run focused tests for changed files before committing and abort if tests fail.

        Returns:
            True if commit succeeded, False otherwise.
"""
if self.no_git:
            logging.info("Skipping git commit: no_git=True. Message: %s", message)
            return False

        try:
            if files:
                for file in files:
                    self.shell.execute(["git", "add", file], check=True)
            else:
                self.shell.execute(["git", "add", "."], check=True)

            # Optionally run focused tests on changed files before committing
            if enforce_tests:
                try:
                    from .test_runner import run_focused_tests_for_files
                except Exception:
                    logging.error("Test runner unavailable; aborting commit due to enforce_tests=True")
                    return False

                file_list = files or []
                success, output = run_focused_tests_for_files(file_list)
                if not success:
                    logging.error("Focused tests failed; aborting commit. Output:\n%s", output)
                    self._record(f"commit: {message}", f"tests_failed: {output}")
                    # Revert staged changes (best effort)
                    try:
                        self.shell.execute(["git", "reset", "HEAD", "--"], check=True)
                    except Exception:
                        pass
                    return False

            # Check if there are changes to commit
            res = self.shell.execute(["git", "status", "--porcelain"])
            status = getattr(res, "stdout", "").strip()

            if not status:
                logging.info("No changes to commit.")
                return False

            res = self.shell.execute(["git", "commit", "-m", message], check=True)
            logging.info("Successfully committed changes: %s", message)
            self._record(f"commit: {message}", "success", {"files": files})
            return True
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error("Error during git commit: %s", e)
            try:
                self._record(f"commit: {message}", f"error: {str(e)}")
            except Exception:
                pass
            return False

    def create_branch(self, branch_name: str) -> bool:
        ""
Create and switch to a new branch.""
if self.no_git:
            return False
        try:
            self.shell.execute(["git", "checkout", "-b", branch_name], check=True)
            logging.info("Created branch: %s", branch_name)
            return True
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error("Failed to create branch %s: %s", branch_name, e)
            return False
