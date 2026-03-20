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

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


def _rust_crdt_binary() -> Path:
    """Ensure the rust_core/crdt binary is built and return its path."""

    repo_root = Path(__file__).resolve().parents[2]
    crate = repo_root / "rust_core" / "crdt"
    binary_name = "rust_core_crdt.exe" if (Path().joinpath(".venv").exists() and __import__("sys").platform == "win32") else "rust_core_crdt"
    binary = crate / "target" / "release" / binary_name

    if not binary.exists():
        subprocess.run(["cargo", "build", "--release"], cwd=crate, check=True)

    return binary


def merge(left: dict, right: dict) -> dict:
    """Merge two JSON documents using the Rust CRDT prototype."""
    with tempfile.TemporaryDirectory() as td:
        left_file = Path(td) / "left.json"
        right_file = Path(td) / "right.json"
        left_file.write_text(json.dumps(left))
        right_file.write_text(json.dumps(right))

        binary = _rust_crdt_binary()
        result = subprocess.run(
            [
                str(binary),
                "merge",
                "--left",
                str(left_file),
                "--right",
                str(right_file),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        return json.loads(result.stdout)


def validate() -> None:
    """Validate this bridge module is loadable.

    This is used by repository-level quality checks.
    """
    return
