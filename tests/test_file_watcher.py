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

import asyncio
import json
import os
import tempfile
import time
from unittest.mock import MagicMock, patch

import pytest

import src.tools.FileWatcher as fw_module
from src.tools.FileWatcher import FileWatcher, _python_scan


# ---------------------------------------------------------------------------
# Test 1 — Rust path: scan_changed_files is called when _HAS_RUST is True
# ---------------------------------------------------------------------------

def test_filewatcher_scan_uses_rust_when_available():
    """When _HAS_RUST is True, _poll uses rust_core.scan_changed_files."""
    fake_rust = MagicMock()
    fake_rust.scan_changed_files.return_value = json.dumps(["/some/file.py"])

    with patch.object(fw_module, "_HAS_RUST", True), \
         patch.object(fw_module, "_rust_core", fake_rust):

        watcher = FileWatcher("/tmp", interval_s=100)

        async def run():
            # Manually call one iteration of _poll's body
            now_ms = time.time() * 1000
            raw = fake_rust.scan_changed_files(watcher.root, int(watcher._last_ms))
            changed = json.loads(raw)
            watcher._pending.update(changed)
            watcher._last_ms = now_ms

        asyncio.run(run())

    assert "/some/file.py" in watcher._pending
    fake_rust.scan_changed_files.assert_called_once()


# ---------------------------------------------------------------------------
# Test 2 — Python fallback: _python_scan returns modified files
# ---------------------------------------------------------------------------

def test_filewatcher_scan_falls_back_to_python():
    """_python_scan should return files modified after since_ms."""
    with tempfile.TemporaryDirectory() as tmpdir:
        fpath = os.path.join(tmpdir, "changed.txt")
        # Create the file
        with open(fpath, "w") as f:
            f.write("hello")
        # since_ms is in the past (1 second ago)
        since_ms = (time.time() - 1) * 1000
        result = asyncio.run(_python_scan(tmpdir, since_ms))
        assert fpath in result


# ---------------------------------------------------------------------------
# Test 3 — get_changes returns accumulated entries and clears the set
# ---------------------------------------------------------------------------

def test_get_changes_returns_and_clears():
    """get_changes() returns pending paths then clears the set."""
    watcher = FileWatcher("/tmp", interval_s=100)
    watcher._pending = {"/a/b.py", "/c/d.py"}

    result = asyncio.run(watcher.get_changes())
    assert set(result) == {"/a/b.py", "/c/d.py"}

    result2 = asyncio.run(watcher.get_changes())
    assert result2 == []


# ---------------------------------------------------------------------------
# Test 4 — _python_scan on non-existent root returns empty list (no crash)
# ---------------------------------------------------------------------------

def test_invalid_root_returns_empty():
    """_python_scan on a non-existent directory should return [] without error."""
    result = asyncio.run(_python_scan("/this/path/does/not/exist/ever", 0))
    assert result == []


# ---------------------------------------------------------------------------
# Test 5 — start/stop lifecycle: task is created and then cancelled
# ---------------------------------------------------------------------------

def test_start_stop_lifecycle():
    """start() creates an asyncio Task; stop() cancels it."""

    async def run():
        watcher = FileWatcher("/tmp", interval_s=9999)
        await watcher.start()
        assert watcher._task is not None
        assert not watcher._task.done()
        await watcher.stop()
        assert watcher._task.done()

    asyncio.run(run())
