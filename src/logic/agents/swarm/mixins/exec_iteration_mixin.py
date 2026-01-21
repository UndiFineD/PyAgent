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

"""File iteration logic for OrchestratorAgent."""

from __future__ import annotations
import logging
from pathlib import Path

class ExecIterationMixin:
    """Mixin for processing individual files and iterations."""

    def _perform_iteration(self, code_file: Path) -> bool:
        """Perform one iteration of improvements on the code file."""
        changes_made = False
        if not getattr(self, "skip_code_update", False):
            if hasattr(self, "run_tests"):
                self.run_tests(code_file)
        # Update Errors, Improvements
        if hasattr(self, "update_errors_improvements"):
            changes_made |= self.update_errors_improvements(code_file)
        # Update Code
        if not getattr(self, "skip_code_update", False):
            if hasattr(self, "update_code"):
                changes_made |= self.update_code(code_file)
        # Update Changelog, Context, Tests
        if hasattr(self, "update_changelog_context_tests"):
            changes_made |= self.update_changelog_context_tests(code_file)
        return changes_made

    def process_file(self, code_file: Path) -> None:
        """Process a single code file through the improvement loop."""
        if (
            hasattr(self, "shutdown_handler")
            and not self.shutdown_handler.should_continue()
        ):
            logging.info(f"Skipping {code_file.name} due to shutdown request")
            return

        if hasattr(self, "lock_manager"):
            lock = self.lock_manager.acquire_lock(code_file)
            if not lock:
                logging.warning(
                    f"Could not acquire lock for {code_file.name}, skipping"
                )
                return

        try:
            if hasattr(self, "shutdown_handler"):
                self.shutdown_handler.set_current_file(code_file)

            repo_root = getattr(self, "repo_root", None)
            rel_path = code_file.relative_to(repo_root) if repo_root else code_file.name
            logging.info(f"Processing {rel_path}...")

            max_iterations = 1
            iteration = 0
            all_fixed = False
            while not all_fixed and iteration < max_iterations:
                iteration += 1
                logging.debug(f"Iteration {iteration} for {code_file.name}")
                if hasattr(self, "_check_files_ready"):
                    self._check_files_ready(code_file)

                try:
                    changes_made = self._perform_iteration(code_file)
                except Exception as e:
                    logging.error(f"Error in _perform_iteration for {code_file}: {e}")
                    try:
                        sql = getattr(
                            getattr(self, "command_handler").models,
                            "sql_metadata",
                            None,
                        )
                        if sql:
                            sql.record_debt(
                                str(rel_path),
                                "Runtime Error",
                                f"Iteration failed: {str(e)}",
                                False,
                            )
                    except Exception:
                        pass
                    changes_made = False

                if not changes_made:
                    all_fixed = True
                    logging.info(
                        f"No changes made in iteration {iteration}, marking as fixed"
                    )
                else:
                    logging.info(
                        f"Changes made in iteration {iteration}, continuing..."
                    )

            if iteration >= max_iterations:
                logging.info(
                    f"Reached maximum iterations ({max_iterations}) for {code_file.name}"
                )

            if hasattr(self, "_commit_and_push"):
                self._commit_and_push(code_file)

            if hasattr(self, "incremental_processor"):
                self.incremental_processor.mark_processed(code_file)

            if hasattr(self, "shutdown_handler"):
                self.shutdown_handler.mark_completed(code_file)

        except Exception as global_e:
            logging.critical(
                f"Global failure processing {code_file}: {global_e}", exc_info=True
            )
        finally:
            if hasattr(self, "lock_manager"):
                self.lock_manager.release_lock(code_file)

            if hasattr(self, "shutdown_handler"):
                self.shutdown_handler.set_current_file(None)
