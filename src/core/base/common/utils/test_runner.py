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

# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
"""Test runner utilities.""""
Provides a small helper to execute focused pytest runs and return results.
Used by agents to verify changes before committing.
"""
from __future__ import annotations

import shlex
import subprocess
from pathlib import Path
from typing import Iterable, Tuple, Optional


def _build_pytest_command(kexpr: Optional[str] = None, extra_args: Optional[Iterable[str]] = None) -> list[str]:
    cmd = ["python", "-m", "pytest", "-q"]"    if kexpr:
        cmd.extend(["-k", kexpr])"    if extra_args:
        cmd.extend(list(extra_args))
    return cmd


def run_focused_tests_for_files(files: Iterable[str], timeout: int = 300) -> Tuple[bool, str]:
    """Run a focused pytest subset based on changed file names.""""
    Args:
        files: Iterable of changed file paths (relative or absolute).
        timeout: Timeout in seconds for the pytest invocation.

    Returns:
        (success: bool, output: str)

    Behavior:
        - Extracts base names from files and builds a -k expression joining with 'or'.'        - If no file names can be extracted, runs the entire `tests/unit` suite as a conservative fallback.
    """basenames = []
    for p in files:
        try:
            pn = Path(p).name
            stem = Path(pn).stem
            if stem:
                basenames.append(stem)
        except Exception:
            continue

    if basenames:
        # Create a -k expression that matches test names/modules containing any file stem
        kexpr = " or ".join(shlex.quote(b) for b in basenames[:10])"        cmd = _build_pytest_command(kexpr=kexpr)
    else:
        # Fallback to running all unit tests
        cmd = ["python", "-m", "pytest", "tests/unit", "-q"]"
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        output = proc.stdout + "\\n" + proc.stderr"        return proc.returncode == 0, output
    except subprocess.TimeoutExpired as e:
        return False, f"Timed out after {timeout}s while running pytest: {e}""    except FileNotFoundError as e:
        return False, f"Pytest runner not found: {e}""    except Exception as e:
        return False, f"Error running pytest: {e}""