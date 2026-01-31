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


class Coordinator:
    """Simple Coordinator to assign shards, monitor workers, and attempt merges.

    This coordinator uses the manifest stored in `scratch/foreach_shards/` and
    monitors worker status files to drive the distributed flow. It does not
    perform any real git operations — merges are simulated by creating a
    `.merge_result.json` artifact under the scratch directory for review.
    """

    def __init__(
        self,
        manifest_path: str | Path,
        scratch_dir: str | Path = "scratch/foreach_shards",
        poll_interval: float = 0.5,
        worker_timeout: int = 60,
    ) -> None:
        self.manifest_path = Path(manifest_path)
        self.scratch_dir = Path(scratch_dir)
        self._fs = FileSystemCore()
        self._fs.ensure_directory(self.scratch_dir)
        self.poll_interval = poll_interval
        self.worker_timeout = worker_timeout

    def load_manifest(self) -> Dict[str, Any]:
        return json.loads(self.manifest_path.read_text())

    def persist_manifest(self, manifest: Dict[str, Any]) -> None:
        self._fs.atomic_write(self.manifest_path, json.dumps(manifest, indent=2))

    def assign_shards(self) -> Dict[str, Any]:
        """Ensure each shard has a `worker` and `branch` assigned."""
        manifest = self.load_manifest()
        shards = manifest.get("shards", [])
        next_worker = 1
        for s in shards:
            if not s.get("worker"):
                s["worker"] = f"worker-{next_worker}"
                s["branch"] = s.get("branch") or f"foreach/{self.manifest_path.stem}/worker-{next_worker}/batch-1"
                next_worker = (next_worker % max(1, len(shards))) + 1
        manifest["shards"] = shards
        self.persist_manifest(manifest)
        return manifest

    def _worker_status_path(self, worker_id: str) -> Path:
        return self.scratch_dir / f"{worker_id}.status.json"

    def monitor_workers_and_merge(self, wait_for_completion: float = 10.0) -> Dict[str, Any]:
        """Monitor worker statuses until completion or timeout and attempt merges.

        Returns an aggregated report containing per-shard outcomes and merge results.
        """
        manifest = self.load_manifest()
        shards = manifest.get("shards", [])
        deadline = time.time() + wait_for_completion
        shard_status: Dict[int, Dict[str, Any]] = {s.get("id"): {"status": "pending"} for s in shards}

        # Keep track of last update times
        last_updates: Dict[str, float] = {}

        while time.time() < deadline:
            all_done = True
            for s in shards:
                sid = s.get("id")
                worker = s.get("worker")
                status_path = self._worker_status_path(worker)
                if status_path.exists():
                    try:
                        st = json.loads(status_path.read_text())
                        last_updates[worker] = st.get("timestamp", time.time())
                        cur_status = st.get("status")
                        shard_status[sid]["status"] = cur_status
                        shard_status[sid]["detail"] = st.get("detail", {})

                        if cur_status == "locked":
                            # Wait for worker to mark 'done'
                            all_done = False
                        elif cur_status in ("released", "done"):
                            # Attempt a simulated merge for the completed shard
                            merge_res = self._attempt_merge(s)
                            shard_status[sid]["merge"] = merge_res
                        elif cur_status in ("lock_failed", "timeout"):
                            # Reassign according to conflict strategy
                            shard_status[sid]["status"] = cur_status
                            # Try to reassign to a different worker (simple round-robin)
                            self._reassign_shard(manifest, s)
                            shards = manifest.get("shards", [])
                            all_done = False
                        else:
                            all_done = False
                    except Exception:
                        all_done = False
                else:
                    # No status file yet; check worker liveness
                    last = last_updates.get(worker, 0)
                    if time.time() - last > self.worker_timeout:
                        shard_status[sid]["status"] = "worker_stalled"
                        self._reassign_shard(manifest, s)
                        shards = manifest.get("shards", [])
                        all_done = False
                    else:
                        all_done = False

            if all_done:
                break
            time.sleep(self.poll_interval)

        # Finalize and write aggregated report
        report = {
            "manifest": str(self.manifest_path),
            "shard_status": shard_status,
            "finished_at": time.time(),
        }
        rep_path = self.scratch_dir / f"{self.manifest_path.stem}_coordinator_report.json"
        self._fs.atomic_write(rep_path, json.dumps(report, indent=2))
        return report

    def _reassign_shard(self, manifest: Dict[str, Any], shard: Dict[str, Any]) -> None:
        """Reassign a shard to the next available worker id.

        This is a simple round-robin reassignment used in staged runs.
        """
        shards = manifest.get("shards", [])
        worker_ids = [s.get("worker") for s in shards if s.get("worker")]
        if not worker_ids:
            return
        current = shard.get("worker")
        try:
            idx = worker_ids.index(current)
            new_worker = worker_ids[(idx + 1) % len(worker_ids)]
        except ValueError:
            new_worker = worker_ids[0]
        shard["worker"] = new_worker
        # update status to requeued so workers can pick it up
        self._fs.atomic_write(self.manifest_path, json.dumps(manifest, indent=2))
        self._fs.atomic_write(self.scratch_dir / f"reassign_{shard.get('id')}.json", json.dumps({"reassigned_to": new_worker}, indent=2))

    def _attempt_merge(self, shard: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate a merge attempt for the worker branch and write a merge result artifact."""
        branch = shard.get("branch")
        # In a real implementation, we would attempt a `git merge` and run CI; here
        # we simulate success and write an artifact for manual review.
        merge_artifact = {
            "branch": branch,
            "merged": True,
            "notes": "Simulated merge - requires human review before actual merge",
            "timestamp": time.time(),
        }
        out_path = self.scratch_dir / f"merge_result_{branch.replace('/', '_')}.json"
        try:
            self._fs.atomic_write(out_path, json.dumps(merge_artifact, indent=2))
        except Exception as e:  # pragma: no cover - best-effort artifact
            logger.debug("Failed to write merge artifact: %s", e)
        return merge_artifact

