#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0

"""Distributed Foreach coordinator and worker helpers.

This module contains a lightweight Worker implementation used by the Foreach
Coordinator to claim shards, acquire per-file locks, and report status to the
scratch area (or recorder). The implementation is intentionally small and
synchronous to make dry-run and staged runs deterministic and easy to test.
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.core.base.common.file_system_core import FileSystemCore
from src.core.base.common.utils.file_lock_manager import FileLockManager

logger = logging.getLogger("pyagent.foreach")


class WorkerClaimError(Exception):
    pass


class Worker:
    """A simple worker that claims a shard, acquires locks, and reports status.

    This is a synchronous helper designed for staged runs and unit tests.
    """

    def __init__(
        self,
        worker_id: str,
        scratch_dir: str | Path = "scratch/foreach_shards",
        file_lock_manager: Optional[FileLockManager] = None,
        worker_timeout: int = 60,
        shard_lock_prefix: str = "foreach",
        conflict_strategy: str = "requeue",
    ) -> None:
        self.worker_id = worker_id
        self.scratch_dir = Path(scratch_dir)
        self._fs = FileSystemCore()
        self._fs.ensure_directory(self.scratch_dir)
        self.locker = file_lock_manager or FileLockManager()
        self.worker_timeout = worker_timeout
        self.acquired_locks: List[str] = []
        self.shard_lock_prefix = shard_lock_prefix
        self.conflict_strategy = conflict_strategy

    def _status_path(self) -> Path:
        return self.scratch_dir / f"{self.worker_id}.status.json"

    def _write_status(self, status: str, detail: Dict[str, Any] | None = None) -> None:
        payload = {
            "worker": self.worker_id,
            "status": status,
            "timestamp": time.time(),
            "detail": detail or {},
        }
        try:
            self._fs.atomic_write(self._status_path(), json.dumps(payload, indent=2))
        except Exception as e:  # pragma: no cover - best-effort status write
            logger.debug("Failed to write worker status: %s", e)

    def load_manifest(self, manifest_path: str | Path) -> Dict[str, Any]:
        p = Path(manifest_path)
        content = p.read_text()
        return json.loads(content)

    def _lock_id_for_file(self, file_path: str) -> str:
        # deterministic lock id composed of prefix and normalized path
        return f"{self.shard_lock_prefix}:{file_path}"

    def claim_shard(self, manifest_path: str | Path) -> bool:
        """Claim the shard assigned to this worker and attempt to acquire file locks.

        Returns True if all locks were acquired and the shard is claimed. On
        failure it sets a status file describing the reason.
        """
        manifest = self.load_manifest(manifest_path)
        shards = manifest.get("shards", [])
        shard = None
        for s in shards:
            if s.get("worker") == self.worker_id or s.get("id") == int(self.worker_id.replace("worker-", "")):
                shard = s
                break
        if not shard:
            self._write_status("no_shard", {"manifest": str(manifest_path)})
            return False

        files = shard.get("files", [])
        self._write_status("claiming", {"shard_id": shard.get("id"), "num_files": len(files)})

        start = time.time()
        per_file_timeout = max(1.0, float(self.worker_timeout) / max(1, len(files)))

        for f in files:
            lock_id = self._lock_id_for_file(f)
            acquired = self.locker.acquire_lock(lock_id, timeout=per_file_timeout)
            if not acquired:
                # Release already-acquired locks and report according to policy
                self.release_locks()
                self._write_status("lock_failed", {"file": f, "lock_id": lock_id})
                return False
            self.acquired_locks.append(lock_id)
            # Small heartbeat update
            self._write_status("locking", {"acquired": len(self.acquired_locks)})
            # Respect global timeout
            if time.time() - start > self.worker_timeout:
                self._write_status("timeout", {"acquired": len(self.acquired_locks)})
                self.release_locks()
                return False

        # All locks acquired
        self._write_status("locked", {"acquired": len(self.acquired_locks), "shard_id": shard.get("id")})
        return True

    def release_locks(self) -> None:
        """Release any locks this worker holds."""
        for lock_id in list(self.acquired_locks):
            try:
                self.locker.release_lock(lock_id)
            except Exception:  # pragma: no cover - best-effort release
                logger.debug("Failed to release lock %s", lock_id)
            try:
                self.acquired_locks.remove(lock_id)
            except ValueError:
                pass
        self._write_status("released", {"remaining": len(self.acquired_locks)})

    def report_progress(self, message: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """Append a short progress update to the worker status."""
        self._write_status("progress", {"msg": message, "meta": meta or {}})

