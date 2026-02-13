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

"""
[Module Title] - [Core Function]

storage_engine.py - Backup, snapshot, and compression engine

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate StatsBackupManager to create and list JSON backups written to disk:
  mgr = StatsBackupManager(backup_dir="backups")
  mgr.create_backup("run-2026-02-12", {"metrics": {...}})
- Use StatsSnapshotManager to persist in-memory snapshots (similar API; create_snapshot / list / restore).
- When available, rust_core will be used for accelerated JSON serialization and compression; otherwise the module falls back to pure-Python implementations.

WHAT IT DOES:
- Provides StatsBackupManager for creating, listing, loading from disk, and restoring named JSON backups with simple safe filename handling.
- Provides StatsSnapshotManager (partial in-file) to manage named in-memory snapshots with optional on-disk persistence.
- Detects an optional rust_core extension to accelerate serialization/compression and falls back to Python when unavailable.
- Uses pathlib, json, and zlib for file IO and compression, and preserves timestamps and minimal metadata per backup.

WHAT IT SHOULD DO BETTER:
- Harden error handling and surface informative exceptions instead of swallowing all errors in some disk operations.
- Use atomic file writes (temp-then-rename) and optional file locking to avoid partial writes and race conditions.
- Add optional encryption at rest and integrity checks (e.g., checksums or signatures) for backups and snapshots.
- Expand and complete StatsSnapshotManager implementation, ensure symmetry with backup APIs, and add async IO variants for large datasets.
- Add comprehensive unit tests for disk-fallback codepaths and the rust_core accelerated paths, and include type narrowing for more precise typing.
- Provide configuration hooks for compression level, JSON encoder customization, retention policies, and snapshot rotation.

FILE CONTENT SUMMARY:
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

"""
Storage engine.py module.
"""
# Backup, snapshot, and compression engine.
# Phase 16: Rust acceleration for JSON serialization and compression

from __future__ import annotations

import contextlib
import json
import logging
import zlib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .observability_core import StatsSnapshot

logger: logging.Logger = logging.getLogger(__name__)

# Phase 16: Rust acceleration imports
try:
    import rust_core

    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False
    logging.debug("rust_core not available, using Python fallback for StorageEngine")


@dataclass
class StatsBackup:
    """A persisted backup entry for StatsBackupManager."""

    name: str
    path: Path
    timestamp: str


class StatsBackupManager:
    """Manages backups of stats."""

    def __init__(self, backup_dir: str | Path | None = None) -> None:
        self.backup_dir: Path | None = Path(backup_dir) if backup_dir is not None else None
        if self.backup_dir:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.backups: dict[str, dict[str, Any]] = {}

    def _safe_name(self, name: str) -> str:
        return "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in name) or "backup"

    def create_backup(self, name: str, data: dict[str, Any]) -> StatsBackup:
        timestamp: str = datetime.now().isoformat()
        self.backups[name] = {"data": data, "timestamp": timestamp}
        path: Path = (
            (self.backup_dir / f"{self._safe_name(name)}.json")
            if self.backup_dir
            else Path(f"{self._safe_name(name)}.json")
        )
        if self.backup_dir:
            path.write_text(
                json.dumps({"name": name, "timestamp": timestamp, "data": data}, indent=2),
                encoding="utf-8",
            )
        return StatsBackup(name=name, path=path, timestamp=timestamp)

    def list_backups(self) -> list[StatsBackup]:
        """List all available backups."""
        def make_backup(item: tuple[str, dict[str, Any]]) -> StatsBackup:
            name, data = item
            path_obj = (
                self.backup_dir / f"{self._safe_name(name)}.json"
                if self.backup_dir
                else Path(f"{self._safe_name(name)}.json")
            )
            return StatsBackup(name=name, path=path_obj, timestamp=data.get("timestamp", ""))

        backups = list(map(make_backup, self.backups.items()))
        backups.extend(self._load_backups_from_disk())
        return backups

    def _load_backups_from_disk(self) -> list[StatsBackup]:
        """Helper to load backups from disk not already in memory."""
        if not self.backup_dir or not self.backup_dir.exists():
            return []

        def process_file(f: Path) -> StatsBackup | None:
            name = f.stem
            if name in self.backups:
                return None
            try:
                payload = json.loads(f.read_text(encoding="utf-8"))
                return StatsBackup(name=name, path=f, timestamp=payload.get("timestamp", ""))
            except Exception:
                return None

        return list(filter(None, map(process_file, self.backup_dir.glob("*.json"))))

    def restore(self, name: str) -> dict[str, Any] | None:
        if name in self.backups:
            return self.backups[name]["data"]

        path: Path | None = self.backup_dir / f"{self._safe_name(name)}.json" if self.backup_dir else None
        if path and path.exists():
            with contextlib.suppress(Exception):
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.backups[name] = {
                    "data": payload["data"],
                    "timestamp": payload["timestamp"],
                }
                return payload["data"]
        return None


class StatsSnapshotManager:
    """Manages snapshots of stats state."""

    def __init__(self, snapshot_dir: str | Path | None = None) -> None:
        self.snapshot_dir: Path | None = Path(snapshot_dir) if snapshot_dir is not None else None
        if self.snapshot_dir:
            self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self.snapshots: dict[str, StatsSnapshot] = {}

    def create_snapshot(self, name: str, data: dict[str, Any]) -> StatsSnapshot:
"""
# Backup, snapshot, and compression engine.
# Phase 16: Rust acceleration for JSON serialization and compression

from __future__ import annotations

import contextlib
import json
import logging
import zlib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .observability_core import StatsSnapshot

logger: logging.Logger = logging.getLogger(__name__)

# Phase 16: Rust acceleration imports
try:
    import rust_core

    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False
    logging.debug("rust_core not available, using Python fallback for StorageEngine")


@dataclass
class StatsBackup:
    """A persisted backup entry for StatsBackupManager."""

    name: str
    path: Path
    timestamp: str


class StatsBackupManager:
    """Manages backups of stats."""

    def __init__(self, backup_dir: str | Path | None = None) -> None:
        self.backup_dir: Path | None = Path(backup_dir) if backup_dir is not None else None
        if self.backup_dir:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.backups: dict[str, dict[str, Any]] = {}

    def _safe_name(self, name: str) -> str:
        return "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in name) or "backup"

    def create_backup(self, name: str, data: dict[str, Any]) -> StatsBackup:
        timestamp: str = datetime.now().isoformat()
        self.backups[name] = {"data": data, "timestamp": timestamp}
        path: Path = (
            (self.backup_dir / f"{self._safe_name(name)}.json")
            if self.backup_dir
            else Path(f"{self._safe_name(name)}.json")
        )
        if self.backup_dir:
            path.write_text(
                json.dumps({"name": name, "timestamp": timestamp, "data": data}, indent=2),
                encoding="utf-8",
            )
        return StatsBackup(name=name, path=path, timestamp=timestamp)

    def list_backups(self) -> list[StatsBackup]:
        """List all available backups."""
        def make_backup(item: tuple[str, dict[str, Any]]) -> StatsBackup:
            name, data = item
            path_obj = (
                self.backup_dir / f"{self._safe_name(name)}.json"
                if self.backup_dir
                else Path(f"{self._safe_name(name)}.json")
            )
            return StatsBackup(name=name, path=path_obj, timestamp=data.get("timestamp", ""))

        backups = list(map(make_backup, self.backups.items()))
        backups.extend(self._load_backups_from_disk())
        return backups

    def _load_backups_from_disk(self) -> list[StatsBackup]:
        """Helper to load backups from disk not already in memory."""
        if not self.backup_dir or not self.backup_dir.exists():
            return []

        def process_file(f: Path) -> StatsBackup | None:
            name = f.stem
            if name in self.backups:
                return None
            try:
                payload = json.loads(f.read_text(encoding="utf-8"))
                return StatsBackup(name=name, path=f, timestamp=payload.get("timestamp", ""))
            except Exception:
                return None

        return list(filter(None, map(process_file, self.backup_dir.glob("*.json"))))

    def restore(self, name: str) -> dict[str, Any] | None:
        if name in self.backups:
            return self.backups[name]["data"]

        path: Path | None = self.backup_dir / f"{self._safe_name(name)}.json" if self.backup_dir else None
        if path and path.exists():
            with contextlib.suppress(Exception):
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.backups[name] = {
                    "data": payload["data"],
                    "timestamp": payload["timestamp"],
                }
                return payload["data"]
        return None


class StatsSnapshotManager:
    """Manages snapshots of stats state."""

    def __init__(self, snapshot_dir: str | Path | None = None) -> None:
        self.snapshot_dir: Path | None = Path(snapshot_dir) if snapshot_dir is not None else None
        if self.snapshot_dir:
            self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self.snapshots: dict[str, StatsSnapshot] = {}

    def create_snapshot(self, name: str, data: dict[str, Any]) -> StatsSnapshot:
        snapshot = StatsSnapshot(name=name, data=data, timestamp=datetime.now().isoformat())
        self.snapshots[name] = snapshot
        if self.snapshot_dir:
            path: Path = self.snapshot_dir / f"{name}.json"
            path.write_text(
                json.dumps(
                    {"name": name, "timestamp": snapshot.timestamp, "data": data},
                    indent=2,
                ),
                encoding="utf-8",
            )
        return snapshot

    def list_snapshots(self) -> list[StatsSnapshot]:
        """List all available snapshots."""
        snapshots = list(self.snapshots.values())
        snapshots.extend(self._load_snapshots_from_disk())
        return snapshots

    def _load_snapshots_from_disk(self) -> list[StatsSnapshot]:
        """Helper to load snapshots from disk not already in memory."""
        if not self.snapshot_dir or not self.snapshot_dir.exists():
            return []

        def process_snap(f: Path) -> StatsSnapshot | None:
            name = f.stem
            if name in self.snapshots:
                return None
            try:
                payload = json.loads(f.read_text(encoding="utf-8"))
                return StatsSnapshot(
                    name=payload.get("name", name),
                    data=payload.get("data", {}),
                    timestamp=payload.get("timestamp", ""),
                )
            except Exception:
                return None

        return list(filter(None, map(process_snap, self.snapshot_dir.glob("*.json"))))

    def restore_snapshot(self, name: str) -> dict[str, Any] | None:
        """Restore a snapshot by name."""
        if name in self.snapshots:
            return self.snapshots[name].data

        if self.snapshot_dir:
            path: Path = self.snapshot_dir / f"{name}.json"

            if path.exists():
                with contextlib.suppress(Exception):
                    payload = json.loads(path.read_text(encoding="utf-8"))
                    data = payload.get("data", {})
                    snap = StatsSnapshot(
                        name=payload.get("name", name),
                        data=data,
                        timestamp=payload.get("timestamp", ""),
                    )
                    self.snapshots[name] = snap
                    return data
        return None


class StatsCompressor:
    """Compresses metric data."""

    def compress(self, data: Any) -> bytes:
        # Phase 16: Try Rust-accelerated JSON serialization + compression
        if _RUST_AVAILABLE and hasattr(rust_core, "compress_json_rust"):
            with contextlib.suppress(Exception):
                if not isinstance(data, (bytes, bytearray)):
                    result = rust_core.compress_json_rust(data)
                    if result:
                        return result

        payload: bytes = (
            (b"b" + bytes(data)) if isinstance(data, (bytes, bytearray)) else (b"j" + json.dumps(data).encode("utf-8"))
        )
        return zlib.compress(payload)

    def decompress(self, data: bytes) -> Any:
        # Phase 16: Try Rust-accelerated decompression + JSON parsing
        if _RUST_AVAILABLE and hasattr(rust_core, "decompress_json_rust"):
            with contextlib.suppress(Exception):
                result = rust_core.decompress_json_rust(data)
                if result is not None:
                    return result

        payload: bytes = zlib.decompress(data)
        tag, body = payload[:1], payload[1:]
        if tag == b"b":
            return body
        if tag == b"j":
            return json.loads(body.decode("utf-8"))
        try:
            return json.loads(payload.decode("utf-8"))
        except json.JSONDecodeError:  # pylint: disable=broad-exception-caught, unused-variable
            import traceback
            traceback.print_exc()
            return payload
