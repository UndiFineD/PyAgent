#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from .StatsSnapshot import StatsSnapshot

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import json

class StatsSnapshotManager:
    """Manages snapshots of stats state.

    Compatibility:
    - Tests expect `__init__(snapshot_dir=...)`.
    - `create_snapshot()` returns an object with `.name` and `.data`.
    - When `snapshot_dir` is provided, snapshots are persisted to JSON files.
    """

    def __init__(self, snapshot_dir: Optional[Union[str, Path]] = None) -> None:
        self.snapshot_dir: Optional[Path] = Path(snapshot_dir) if snapshot_dir is not None else None
        if self.snapshot_dir is not None:
            self.snapshot_dir.mkdir(parents=True, exist_ok=True)

        self.snapshots: Dict[str, StatsSnapshot] = {}

    def _safe_snapshot_name(self, name: str) -> str:
        # Prevent path traversal and keep filenames portable.
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
        safe = "".join(ch if ch in allowed else "_" for ch in name)
        return safe or "snapshot"

    def _snapshot_path(self, name: str) -> Optional[Path]:
        if self.snapshot_dir is None:
            return None
        safe_name = self._safe_snapshot_name(name)
        return self.snapshot_dir / f"{safe_name}.json"

    def create_snapshot(self, name: str, data: Dict[str, Any]) -> StatsSnapshot:
        """Create a snapshot."""
        snapshot = StatsSnapshot(name=name, data=data, timestamp=datetime.now().isoformat())
        self.snapshots[name] = snapshot

        path = self._snapshot_path(name)
        if path is not None:
            payload = {"name": snapshot.name, "timestamp": snapshot.timestamp, "data": snapshot.data}
            path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

        return snapshot

    def restore_snapshot(self, name: str) -> Optional[Dict[str, Any]]:
        """Restore a snapshot."""
        if name in self.snapshots:
            return self.snapshots[name].data

        path = self._snapshot_path(name)
        if path is not None and path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                data = payload.get("data")
                if isinstance(data, dict):
                    timestamp = str(payload.get("timestamp") or "")
                    snapshot = StatsSnapshot(name=str(payload.get("name") or name), data=data, timestamp=timestamp)
                    self.snapshots[name] = snapshot
                    return data
            except Exception:
                return None

        return None

    def list_snapshots(self) -> List[str]:
        """List all snapshots."""
        names = set(self.snapshots.keys())
        if self.snapshot_dir is not None:
            for candidate in self.snapshot_dir.glob("*.json"):
                if candidate.is_file():
                    names.add(candidate.stem)
        return sorted(names)
