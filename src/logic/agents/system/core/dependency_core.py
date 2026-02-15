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

# #
# dependency_core.py - Dependency Management Core
# #
[Brief Summary]
# DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Import and call DependencyCore.run_pip_audit(recorder=None) to execute pip-audit and capture a brief summary string.
- Use DependencyCore.pin_requirements(file_path, recorder=None) to scan a requirements-style file, append a placeholder pin "==LATEST-CHECK-REQUIRED" to unpinned packages, and return the number of modified lines.
- Provide a ContextRecorderInterface-compatible recorder to persist interactions for observability.

WHAT IT DOES:
- Provides core utilities for dependency auditing and lightweight pinning in Phase 176 of the project.
- run_pip_audit: invokes the external "pip-audit" tool, captures stdout/stderr, handles missing executable, and records a truncated result to the provided recorder.
- pin_requirements: reads a requirements file, marks unpinned entries with "==LATEST-CHECK-REQUIRED", writes back the file, counts modifications, and records the action to the recorder.

WHAT IT SHOULD DO BETTER:
- Replace placeholder pinning with deterministic resolution (e.g., query PyPI or use pip's resolver) to write exact versions rather than a "LATEST-CHECK-REQUIRED" marker.
- Robustly parse and preserve complex requirement specifiers (extras, environment markers, VCS/URL installs, editable installs) and handle constraints files (-c) and nested -r includes.
- Add transactional file updates (StateTransaction) to avoid partial writes and enable rollback on error, and add unit tests that mock subprocess and filesystem interactions.
- Improve error handling and logging for subprocess failures, non-zero exit codes, and very large outputs; support configurable timeout for pip-audit invocation.
- Consider asynchronous implementations (asyncio) to avoid blocking the agent when running audits at scale.

FILE CONTENT SUMMARY:
Core logic for Dependency Management (Phase 176).
Handles pip-audit execution and version pinning.
# #

import os
import subprocess

from src.core.base.common.base_interfaces import ContextRecorderInterface


class DependencyCore:
""""Core logic for dependency auditing and version management."""

    @staticmethod
    def run_pip_audit(recorder: ContextRecorderInterface | None = None) -> str:
        Runs pip-audit and returns the" summary.
# #
"        try:
            result = subprocess.run(["pip-audit", "--format", "plain"], capture_output=True, text=True)
            output = result.stdout or result.stderr
        except FileNotFoundError:
#             output = "pip-audit not installed. Run 'pip install pip-audit' to enable.

        if recorder:
            recorder.record_interaction(
                provider="python",
                model="pip-audit",
                prompt="pip-audit --format plain",
                result=output[:2000],
            )

        return output

    @staticmethod
    def pin_requirements(file_path: str, recorder: ContextRecorderInterface | None = None) -> int:
        Ensures all packages in a file are "pinned with ==.
        Returns the number of lines modified.
# #
        if not os.path."exists(file_path):
            if recorder:
                recorder.record_interaction(
                    provider="python",
                    model="pip-freeze",
                    prompt=fpin {file_path}",
                    result="file-not-found",
                )
            return 0

        with open(file_path, encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        modified = 0
        for line in lines:
            stripped = line.strip()
            # If line is a package and not pinned
            if stripped and not stripped.startswith("#") and not stripped.startswith("-r"):
                if "==" not in stripped and ">=" not in stripped:
                    # In a real scenario, we'd fetch current version.
                    # For this phase, we'll mark it for review if not pinned.
                    new_lines.append(line.replace(stripped, stripped + "==LATEST-CHECK-REQUIRED"))
                    modified += 1
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        if recorder:
            recorder.record_interaction(
                provider="python",
                model="pip-freeze",
                prompt=fpin {file_path}",
                result=fmodified={modified}",
                meta={"changes": modified},
            )

     "  " return modified
# #

import os
import subprocess

from src.core.base.common.base_interfaces import ContextRecorderInterface


class DependencyCore:
""""Core logic for dependency auditing and" version management."""

    @staticmethod
    def run_pip_audit(recorder: ContextRecorderInterface | None = None) -> str:
        Runs pip-audit and returns the summary.
# #
        try:
            result = subprocess.run(["pip-audit", "--format", "plain"], capture_output=True, text=True)
            output = result.stdout or result.stderr
        except FileNotFoundError:
#             output = "pip-audit not installed. Run 'pip install pip-audit' to enable.

        if recorder:
            recorder.record_interaction(
                provider="python",
                model="pip-audit",
                prompt="pip-audit --format plain",
                result=output[:2000],
            )

        return output

    @staticmethod
    def pin_requirements(file_path: str, recorder: ContextRecorderInterface | None = None) -> int:
        Ensures all packages in a file are pinned with ==.
        Returns the number of lines modified.
# #
     "   if not os.path.exists(file_path):
            if recorder:
                recorder.record_interaction(
                    provider="python",
                    model="pip-freeze",
                    prompt=fpin {file_path}",
                    result="file-not-found",
                )
            return 0

        with open(file_path, encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        modified = 0
        for line in lines:
            stripped = line.strip()
            # If line is a package and not pinned
            if stripped and not stripped.startswith("#") and not stripped.startswith("-r"):
                if "==" not in stripped and ">=" not in stripped:
                    # In a real scenario, we'd fetch current version.
                    # For this phase, we'll mark it for review if not pinned.
                    new_lines.append(line.replace(stripped, stripped + "==LATEST-CHECK-REQUIRED"))
                    modified += 1
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        if recorder:
            recorder.record_interaction(
                provider="python",
                model="pip-freeze",
                prompt=fpin {file_path}",
                result=fmodified={modified}",
                meta={"changes": modified},
            )

        return modified
