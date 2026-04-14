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

"""Smoke test for the rust_core/crdt crate.

This test builds the crate and verifies the merge command produces a JSON output
that contains both inputs.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_rust_crdt_merge_binary_merges_json(tmp_path):
    """Test that the Rust CRDT merge binary can merge two JSON documents correctly."""
    root = Path(__file__).resolve().parents[1]
    crate = root / "rust_core" / "crdt"

    subprocess.run(["cargo", "build", "--release"], cwd=crate, check=True)

    binary_name = "rust_core_crdt.exe" if sys.platform == "win32" else "rust_core_crdt"
    binary = crate / "target" / "release" / binary_name
    assert binary.exists(), "Expected built binary to exist"

    left = {"a": 1}
    right = {"b": 2}
    left_file = tmp_path / "left.json"
    right_file = tmp_path / "right.json"
    left_file.write_text(json.dumps(left))
    right_file.write_text(json.dumps(right))

    result = subprocess.run(
        [str(binary), "merge", "--left", str(left_file), "--right", str(right_file)],
        capture_output=True,
        text=True,
        check=True,
    )

    data = json.loads(result.stdout)
    assert data["a"] == 1
    assert data["b"] == 2
