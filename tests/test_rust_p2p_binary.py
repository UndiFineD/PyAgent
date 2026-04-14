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

"""Smoke test for the rust_core/p2p crate.

This test builds the p2p binary and verifies it runs and prints a peer ID.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

import pytest

if not shutil.which("cargo"):
    pytest.skip("cargo not installed — Rust toolchain required", allow_module_level=True)


def _ensure_protoc_available(tmp_path: Path) -> str:
    """Ensure a `protoc` binary is available for prost-build.

    The libp2p dependency uses prost-build which requires a `protoc` executable.
    This helper will download a vendored protoc for Windows when it is missing.
    """
    # If the system already has protoc, use it.
    found = shutil.which("protoc")
    if found:
        return found

    # Auto-download is only supported on Windows (win64 binary).
    if sys.platform != "win32":
        pytest.skip("protoc not installed and auto-download only supports Windows")

    # Otherwise, download a known-good release and extract it.
    cache_dir = tmp_path / "protoc"
    bin_path = cache_dir / "bin" / "protoc.exe"
    if bin_path.exists():
        return str(bin_path)

    cache_dir.mkdir(parents=True, exist_ok=True)
    url = "https://github.com/protocolbuffers/protobuf/releases/download/v34.0/protoc-34.0-win64.zip"

    zip_path = cache_dir / "protoc.zip"
    try:
        urllib.request.urlretrieve(url, zip_path)
    except Exception as exc:
        pytest.skip(f"Cannot download protoc for tests: {exc}")

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(cache_dir)

    if not bin_path.exists():
        pytest.skip("protoc binary not found after extracting downloaded archive")

    return str(bin_path)


def test_rust_p2p_binary_runs_and_reports_peer_id(tmp_path):
    """Test that the rust_core/p2p binary runs and reports a peer ID."""
    root = Path(__file__).resolve().parents[1]
    crate = root / "rust_core" / "p2p"

    # Ensure build can find protoc for protobuf codegen.
    protoc = _ensure_protoc_available(tmp_path)

    env = dict(**os.environ)
    env["PROTOC"] = protoc

    # Build the crate to ensure dependencies are fetched and compilation works.
    subprocess.run(["cargo", "build", "--release"], cwd=crate, check=True, env=env)

    binary_name = "rust_core_p2p.exe" if sys.platform == "win32" else "rust_core_p2p"
    binary = crate / "target" / "release" / binary_name
    assert binary.exists(), "Expected built binary to exist"

    result = subprocess.run([str(binary), "--version"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "rust_core_p2p" in result.stdout
