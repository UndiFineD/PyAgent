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

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_stats.py"""



from .StatsBackup import StatsBackup

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import json



































class StatsBackupManager:
    """Manages backups of stats."""

    def __init__(self, backup_dir: Optional[Union[str, Path]] = None) -> None:
        self.backup_dir: Optional[Path] = Path(backup_dir) if backup_dir is not None else None
        if self.backup_dir is not None:
            self.backup_dir.mkdir(parents=True, exist_ok=True)

        self.backups: Dict[str, Dict[str, Any]] = {}

    def _safe_backup_name(self, name: str) -> str:
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
        safe = "".join(ch if ch in allowed else "_" for ch in name)
        return safe or "backup"

    def _backup_path(self, name: str) -> Optional[Path]:
        if self.backup_dir is None:
            return None
        safe_name = self._safe_backup_name(name)
        return self.backup_dir / f"{safe_name}.json"

    def create_backup(self, name: str, data: Dict[str, Any]) -> StatsBackup:
        """Create a backup and persist to disk when configured."""
        timestamp = datetime.now().isoformat()
        self.backups[name] = {"data": data, "timestamp": timestamp}

        path = self._backup_path(name) or Path(f"{self._safe_backup_name(name)}.json")
        payload: Dict[str, Any] = {"name": name, "timestamp": timestamp, "data": data}
        if self.backup_dir is not None:
            path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

        return StatsBackup(name=name, path=path, timestamp=timestamp)

    def restore(self, name: str) -> Optional[Dict[str, Any]]:
        """Restore a backup by name (test compatibility)."""
        restored = self.restore_backup(name)
        if restored is not None:
            return restored

        path = self._backup_path(name)
        if path is not None and path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                data = payload.get("data")
                if isinstance(data, dict):
                    self.backups[name] = {"data": data, "timestamp": str(payload.get("timestamp") or "")}
                    return data
            except Exception:
                return None
        return None

    def restore_backup(self, name: str) -> Optional[Dict[str, Any]]:
        """Restore from in-memory backup."""
        if name in self.backups:
            val = self.backups[name]["data"]
            if isinstance(val, dict):
                return val  # type: ignore
        return None

    def list_backups(self) -> List[str]:
        """List all backups."""
        names = set(self.backups.keys())
        if self.backup_dir is not None:
            for candidate in self.backup_dir.glob("*.json"):
                if candidate.is_file():
                    names.add(candidate.stem)
        return sorted(names)
