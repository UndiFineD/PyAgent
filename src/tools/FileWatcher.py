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
import time
from pathlib import Path
from typing import Optional

try:
    import rust_core as _rust_core
    _HAS_RUST = hasattr(_rust_core, "scan_changed_files")
except ImportError:
    _rust_core = None  # type: ignore[assignment]
    _HAS_RUST = False


def _python_scan_sync(root: str, since_ms: float) -> list:
    """Pure-Python fallback (sync, run in thread): walk the tree and return files newer than since_ms."""
    changed = []
    cutoff = since_ms / 1000.0
    for dirpath, _dirnames, filenames in os.walk(root):
        for fname in filenames:
            path = os.path.join(dirpath, fname)
            try:
                if os.path.getmtime(path) > cutoff:
                    changed.append(path)
            except OSError:
                pass
    return changed


async def _python_scan(root: str, since_ms: float) -> list:
    """Async wrapper: run the sync os.walk in a thread pool to avoid blocking the event loop."""
    return await asyncio.to_thread(_python_scan_sync, root, since_ms)


class FileWatcher:
    """Async filesystem watcher that uses the Rust scan_changed_files accelerator when
    available and falls back to a pure-Python os.walk implementation otherwise.

    Usage::

        watcher = FileWatcher("/path/to/root", interval_s=1.0)
        await watcher.start()
        ...
        changes = await watcher.get_changes()   # list of changed paths; clears the set
        await watcher.stop()
    """

    def __init__(self, root: str, interval_s: float = 1.0) -> None:
        self.root = str(Path(root).resolve())
        self.interval_s = interval_s
        self._last_ms: float = time.time() * 1000
        self._pending: set = set()
        self._task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        self._task = asyncio.create_task(self._poll())

    async def stop(self) -> None:
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def get_changes(self) -> list:
        """Return accumulated changed paths and clear the internal set."""
        result = list(self._pending)
        self._pending.clear()
        return result

    async def _poll(self) -> None:
        while True:
            await asyncio.sleep(self.interval_s)
            now_ms = time.time() * 1000
            if _HAS_RUST:
                raw = _rust_core.scan_changed_files(self.root, int(self._last_ms))
                changed = json.loads(raw)
            else:
                changed = await _python_scan(self.root, self._last_ms)
            self._pending.update(changed)
            self._last_ms = now_ms
