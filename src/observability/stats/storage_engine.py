#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Backup, snapshot, and compression engine.

from __future__ import annotations
import json
import logging
import zlib
from datetime import datetime
from pathlib import Path
from typing import Any
from dataclasses import dataclass
from .observability_core import StatsSnapshot

logger = logging.getLogger(__name__)











@dataclass
class StatsBackup:





    """A persisted backup entry for StatsBackupManager."""
    name: str
    path: Path
    timestamp: str






class StatsBackupManager:
    """Manages backups of stats."""
    def __init__(self, backup_dir: str | Path | None = None) -> None:
        self.backup_dir = Path(backup_dir) if backup_dir is not None else None
        if self.backup_dir:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.backups: dict[str, dict[str, Any]] = {}

    def _safe_name(self, name: str) -> str:
        return "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in name) or "backup"

    def create_backup(self, name: str, data: dict[str, Any]) -> StatsBackup:
        timestamp = datetime.now().isoformat()
        self.backups[name] = {"data": data, "timestamp": timestamp}
        path = (self.backup_dir / f"{self._safe_name(name)}.json") if self.backup_dir else Path(f"{self._safe_name(name)}.json")
        if self.backup_dir:
            path.write_text(json.dumps({"name": name, "timestamp": timestamp, "data": data}, indent=2), encoding="utf-8")
        return StatsBackup(name=name, path=path, timestamp=timestamp)

    def list_backups(self) -> list[StatsBackup]:
        """List all available backups."""
        backups = []
        # Add in-memory backups
        for name, data in self.backups.items():
            path_obj = self.backup_dir / f"{self._safe_name(name)}.json" if self.backup_dir else Path(f"{self._safe_name(name)}.json")
            backups.append(StatsBackup(name=name, path=path_obj, timestamp=data.get("timestamp", "")))

        # Add from disk if not already present
        if self.backup_dir and self.backup_dir.exists():
            for f in self.backup_dir.glob("*.json"):
                name = f.stem
                if name not in self.backups:





                     try:
                        payload = json.loads(f.read_text(encoding="utf-8"))
                        backups.append(StatsBackup(name=name, path=f, timestamp=payload.get("timestamp", "")))
                     except Exception:
                        pass
        return backups

    def restore(self, name: str) -> dict[str, Any] | None:
        if name in self.backups:
            return self.backups[name]["data"]





        path = self.backup_dir / f"{self._safe_name(name)}.json" if self.backup_dir else None
        if path and path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.backups[name] = {"data": payload["data"], "timestamp": payload["timestamp"]}
                return payload["data"]
            except Exception:
                pass
        return None






class StatsSnapshotManager:
    """Manages snapshots of stats state."""
    def __init__(self, snapshot_dir: str | Path | None = None) -> None:
        self.snapshot_dir = Path(snapshot_dir) if snapshot_dir is not None else None
        if self.snapshot_dir:
            self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self.snapshots: dict[str, StatsSnapshot] = {}

    def create_snapshot(self, name: str, data: dict[str, Any]) -> StatsSnapshot:
        snapshot = StatsSnapshot(name=name, data=data, timestamp=datetime.now().isoformat())
        self.snapshots[name] = snapshot
        if self.snapshot_dir:
            path = self.snapshot_dir / f"{name}.json"
            path.write_text(json.dumps({"name": name, "timestamp": snapshot.timestamp, "data": data}, indent=2), encoding="utf-8")
        return snapshot

    def list_snapshots(self) -> list[StatsSnapshot]:
        """List all available snapshots."""
        snapshots = []
        for name, snap in self.snapshots.items():
            snapshots.append(snap)

        if self.snapshot_dir and self.snapshot_dir.exists():
            for f in self.snapshot_dir.glob("*.json"):
                 name = f.stem
                 if name not in self.snapshots:
                     try:
                         payload = json.loads(f.read_text(encoding="utf-8"))
                         # Assuming payload has data, timestamp, name
                         snapshots.append(StatsSnapshot(





                             name=payload.get("name", name),
                             data=payload.get("data", {}),
                             timestamp=payload.get("timestamp", "")
                         ))
                     except Exception:
                         pass
        return snapshots

    def restore_snapshot(self, name: str) -> dict[str, Any] | None:
        """Restore a snapshot by name."""
        if name in self.snapshots:
            return self.snapshots[name].data

        if self.snapshot_dir:
            path = self.snapshot_dir / f"{name}.json"





            if path.exists():
                try:
                    payload = json.loads(path.read_text(encoding="utf-8"))
                    data = payload.get("data", {})
                    snap = StatsSnapshot(
                             name=payload.get("name", name),
                             data=data,
                             timestamp=payload.get("timestamp", "")
                    )
                    self.snapshots[name] = snap
                    return data
                except Exception:
                    pass
        return None






class StatsCompressor:
    """Compresses metric data."""
    def compress(self, data: Any) -> bytes:
        payload = (b"b" + bytes(data)) if isinstance(data, (bytes, bytearray)) else (b"j" + json.dumps(data).encode("utf-8"))
        return zlib.compress(payload)

    def decompress(self, data: bytes) -> Any:
        payload = zlib.decompress(data)
        tag, body = payload[:1], payload[1:]
        if tag == b"b": return body
        if tag == b"j": return json.loads(body.decode("utf-8"))
        try: return json.loads(payload.decode("utf-8"))
        except Exception: return payload
