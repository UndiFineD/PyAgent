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
import asyncio
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

    def claim_shard_with_retries(
        self,
        manifest_path: str | Path,
        retries: int = 3,
        delay: float = 0.1,
        backoff: float = 2.0,
        sleep_fn: Optional[callable] = None,
    ) -> bool:
        """Attempt to claim shard with retries and exponential backoff.

        `sleep_fn` may be injected for testability; it should accept seconds to
        sleep. If omitted, falls back to `time.sleep`.
        """
        sleep_fn = sleep_fn or time.sleep
        attempt = 0
        cur_delay = float(delay)
        while attempt < int(retries):
            ok = self.claim_shard(manifest_path)
            if ok:
                return True
            attempt += 1
            sleep_fn(cur_delay)
            cur_delay *= float(backoff)
        return False

    async def claim_shard_async(self, manifest_path: str | Path, retries: int = 3, delay: float = 0.1) -> bool:
        """Async wrapper that runs claim_shard_with_retries in a thread pool."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.claim_shard_with_retries, manifest_path, retries, delay)

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


class Coordinator:
    """A lightweight coordinator for staged Foreach runs.

    The Coordinator reads a manifest describing shards and monitors worker
    status files in a scratch area. It will detect stalled workers and emit
    simple reassign markers, and will detect shard completion (status 'done')
    and include a 'merge' hint in the aggregated report.

    For safety, the Coordinator ensures that the manifest indicates tests
    should be run for staged changes by setting `enforce_tests` to True by
    default. Agents and Workers may consult this flag when choosing whether
    to run focused tests before staging edits.
    """

    def __init__(
        self,
        manifest_path: str | Path,
        scratch_dir: str | Path = "scratch/foreach_shards",
        poll_interval: float = 2.0,
        worker_timeout: float = 600.0,
        leader_ttl: float | None = None,
    ) -> None:
        self.manifest_path = Path(manifest_path)
        self.scratch_dir = Path(scratch_dir)
        self.poll_interval = float(poll_interval)
        self.worker_timeout = float(worker_timeout)
        # leader_ttl defaults to worker_timeout when not supplied so tests may
        # set worker_timeout to control leader leasing.
        self.leader_ttl = float(leader_ttl) if leader_ttl is not None else float(self.worker_timeout)
        self._fs = FileSystemCore()
        self._fs.ensure_directory(self.scratch_dir)
        self._leader_file = self.scratch_dir / "leader.json"

    def assign_shards(self) -> Dict[str, Any]:
        """Read and return the manifest, ensuring `enforce_tests` is set.

        This method is intentionally idempotent and does not modify worker
        assignments unless necessary.
        """
        content = self.manifest_path.read_text()
        manifest = json.loads(content)
        # Ensure enforce_tests flag is present and True by default
        if "enforce_tests" not in manifest:
            manifest["enforce_tests"] = True
        return manifest

    def monitor_workers_and_merge(self, wait_for_completion: float = 30.0) -> Dict[str, Any]:
        """Poll worker status files and return an aggregated report.

        wait_for_completion sets the maximum wall-clock time to wait for all
        shards to reach a terminal state. The report includes a map
        `shard_status` keyed by shard id describing outcomes.
        """
        manifest = self.assign_shards()
        shards = {s.get("id"): s for s in manifest.get("shards", [])}
        shard_status: Dict[int, Dict[str, Any]] = {}

        deadline = time.time() + float(wait_for_completion)
        pending = set(shards.keys())

        while pending and time.time() < deadline:
            for sid in list(pending):
                shard = shards[sid]
                worker = shard.get("worker")
                status_path = self.scratch_dir / f"{worker}.status.json"
                if status_path.exists():
                    try:
                        data = json.loads(status_path.read_text())
                        st = data.get("status")
                        if st == "done":
                            shard_status[sid] = {"status": "done", "merge": {"shard_id": sid}}
                            pending.remove(sid)
                        elif st == "locked":
                            # still working; leave for next poll
                            shard_status.setdefault(sid, {}).update({"status": "locked"})
                        elif st == "lock_failed":
                            shard_status[sid] = {"status": "lock_failed"}
                            pending.remove(sid)
                    except Exception:
                        shard_status[sid] = {"status": "unknown"}
                        pending.remove(sid)
                else:
                    # no status file yet; defer until deadline
                    pass
            if pending and time.time() < deadline:
                time.sleep(self.poll_interval)
        # Any remaining pending shards are considered stalled
        for sid in list(pending):
            shard_status[sid] = {"status": "worker_stalled"}
            # write a reassign marker for operators/telemetry
            try:
                self._fs.atomic_write(self.scratch_dir / f"reassign_{sid}.json", json.dumps({"shard_id": sid}, indent=2))
            except Exception:
                logger.debug("Failed to write reassign marker for shard %s", sid)
        return {"manifest_id": manifest.get("manifest_id"), "shard_status": shard_status}

    def elect_leader(self, leader_name: str) -> bool:
        """Attempt to acquire leadership for the given `leader_name`.

        Returns True if leadership was acquired, False otherwise. Leadership is
        represented by a simple file in the scratch area with an expiry time.
        """
        now = time.time()
        # If leader file exists and not expired, fail
        if self._leader_file.exists():
            try:
                data = json.loads(self._leader_file.read_text())
                expires = float(data.get("expires", 0))
                if expires > now:
                    return False
            except Exception:
                # Corrupt file: allow takeover
                pass
        # Acquire leadership by writing a new leader file
        try:
            payload = {"leader": leader_name, "expires": now + float(self.leader_ttl)}
            self._fs.atomic_write(self._leader_file, json.dumps(payload, indent=2))
            return True
        except Exception:
            return False

