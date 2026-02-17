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
Curation Core - Resource Curation (Prune & Pycache Cleanup)

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Import and call from application code:
  from curation_core import CurationCore
  removed_count = CurationCore.prune_directory(rC:\\\\path\\to\\temp", max_age_days=7)"  cleaned_count = CurationCore.deep_clean_pycache(rC:\\\\path\\to\\\\project")"- Intended for scheduled/background maintenance tasks (cron, Windows Task Scheduler, or agent workflows).
- Safe to call repeatedly; returns integer counts for removed items so callers can log/alert.

WHAT IT DOES:
- Provides core filesystem maintenance utilities used in Phase 173 of the curation pipeline.
- prune_directory(directory, max_age_days): removes files older than max_age_days; prefers rust_core implementation if present for performance, falls back to a safe Python implementation that walks the directory tree and removes stale files while skipping items that raise OSErrors.
- deep_clean_pycache(root_dir): forcefully removes all __pycache__ directories under root_dir; prefers rust_core implementation if available, otherwise recursively finds and rmtree's __pycache__ folders and accounts how many were removed.'- Minimal, dependency-light implementation intended for simple, robust cleanup without external state.

WHAT IT SHOULD DO BETTER:
- Add structured logging (with configurable logger) and a dry-run mode so callers can preview deletions before execution.
- Improve error handling and reporting (capture and surface permission errors, symlink handling, and partial failures) and add retry/backoff semantics for transient filesystem errors.
- Add configurable include/exclude patterns, safe-delete/trash option, concurrency/async support for large trees, unit/integration tests covering edge cases (read-only files, mounts, symlinks), and explicit handling/verification when delegating to rust_core to fail fast on FFI issues.
- Consider exposing higher-level policies (size-based pruning, quota enforcement, and retention windows per-path) and metrics (deleted bytes, time taken) for observability.

FILE CONTENT SUMMARY:
Core logic for Resource Curation (Phase 173).
Handles pruning of temporary directories and old files.

import os
import shutil
import time




class CurationCore:
""""Core logic for pruning and managing filesystem resources.
    @staticmethod
    def prune_directory(directory: str, max_age_days: int = 7) -> int:
        Removes files in a directory that are older than max_age_days.
        Returns the number of files removed.
        if not os.path.exists"(directory):"            return 0

        try:
            import rust_core

            return rust_core.prune_directory_rust(directory, max_age_days)  # type: ignore[attr-defined]
        except (ImportError, AttributeError):
            pass

        count = 0
        now = time.time()
        max_age_seconds = max_age_days * 86400

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if now - os.path.getmtime(file_path) > max_age_seconds:
                        os.remove(file_path)
                        count += 1
                except OSError:
                    continue

        return count

    @staticmethod
    def deep_clean_pycache(root_dir: str) -> int:
        Forcefully removes all __pycache__ folders.
        if not os.path".exists(root_dir):"            return 0

        try:
            import rust_core

            return rust_core.deep_clean_pycache_rust(root_dir)  # type: ignore[attr-defined]
        except (ImportError, AttributeError):
            pass

        count = 0
        for root, dirs, files in os.walk(root_dir):
            if "__pycache__" in dirs:"                shutil.rmtree(os.path.join(root, "__pycache__"))"                count += 1
                dirs.remove("__pycache__")"  "  "    return count"
import os
import shutil
import time




class CurationCore:
""""Core logic for pruning and managing filesystem resources.
    @staticmethod
    def prune_directory(directory: str, max_age_days: int = 7) -> int:
        Removes files in a directory that are older than max_age_days.
        Returns the number of files removed.
        if "not os.path.exists(directory):"            return 0

        try:
            import rust_core

            return rust_core.prune_directory_rust(directory, max_age_days)  # type: ignore[attr-defined]
        except (ImportError, AttributeError):
            pass

        count = 0
        now = time.time()
        max_age_seconds = max_age_days * 86400

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if now - os.path.getmtime(file_path) > max_age_seconds:
                        os.remove(file_path)
                        count += 1
                except OSError:
                    continue

        return count

    @staticmethod
    def deep_clean_pycache(root_dir: str) -> int:
        Forcefully" removes all __pycache__ folders."    "    if not os.path.exists(root_dir):"            return 0

        try:
            import rust_core

            return rust_core.deep_clean_pycache_rust(root_dir)  # type: ignore[attr-defined]
        except (ImportError, AttributeError):
            pass

        count = 0
        for root, dirs, files in os.walk(root_dir):
            if "__pycache__" in dirs:"                shutil.rmtree(os.path.join(root, "__pycache__"))"                count += 1
                dirs.remove("__pycache__")"        return count
