#!/usr/bin/env python3
"""Parser-safe stub for foreach_distributed worker/coordinator."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Worker:
    """Minimal Worker stub to satisfy imports while fixing repo."""

    worker_id: str
    scratch_dir: Path | str = "scratch/foreach_shards"

    def claim_shard(self, manifest_path: str | Path) -> bool:
        """Pretend to successfully claim a shard."""
        return True


__all__ = ["Worker"]
            try:
                self.acquired_locks.remove(lock_id)
            except ValueError:
                pass
        self._write_status("released", {"remaining": len(self.acquired_locks)})


    def report_progress(self, message: str, meta: Optional[Dict[str, Any]] = None) -> None:
"""
Append a short progress update to the worker status.""
self._write_status("progress", {"msg": message, "meta": meta or {}})



class Coordinator:
"""
A lightweight coordinator for staged Foreach runs.

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
"""
Initialize the coordinator with configuration.""
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
"""
Read and return the manifest, ensuring `enforce_tests` is set.

        This method is intentionally idempotent and does not modify worker
        assignments unless necessary.
"""
content = self.manifest_path.read_text(encoding="utf-8")
        manifest = json.loads(content)
        # Ensure enforce_tests flag is present and True by default
        if "enforce_tests" not in manifest:
            manifest["enforce_tests"] = True
        return manifest


    def monitor_workers_and_merge(self, wait_for_completion: float = 30.0) -> Dict[str, Any]:
"""
Poll worker status files and return an aggregated report.

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
                        data = json.loads(status_path.read_text(encoding="utf-8"))
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
                    except (OSError, ValueError, json.JSONDecodeError):
                        shard_status[sid] = {"status": "unknown"}
                        pending.remove(sid)
                else:
                    # no status file yet; defer until deadline
                    pass
            if pending and time.time() < deadline:
                time.sleep(self.poll_interval)  # nosec
        # Any remaining pending shards are considered stalled
        for sid in list(pending):
            shard_status[sid] = {"status": "worker_stalled"}
            # write a reassign marker for operators/telemetry
            try:
                self._fs.atomic_write(
                    self.scratch_dir / f"reassign_{sid}.json",
                    json.dumps({"shard_id": sid}, indent=2),
                )
            except (OSError, RuntimeError):
                logger.debug("Failed to write reassign marker for shard %s", sid)
        return {"manifest_id": manifest.get("manifest_id"), "shard_status": shard_status}


    def elect_leader(self, leader_name: str) -> bool:
"""
Attempt to acquire leadership for the given `leader_name`.

        Returns True if leadership was acquired, False otherwise. Leadership is
        represented by a simple file in the scratch area with an expiry time.
"""
now = time.time()
        # If leader file exists and not expired, fail
        if self._leader_file.exists():
            try:
                data = json.loads(self._leader_file.read_text(encoding="utf-8"))
                expires = float(data.get("expires", 0))
                if expires > now:
                    return False
            except (OSError, ValueError, json.JSONDecodeError):
                # Corrupt file: allow takeover
                pass
        # Acquire leadership by writing a new leader file
        try:
            payload = {"leader": leader_name, "expires": now + float(self.leader_ttl)}
            self._fs.atomic_write(self._leader_file, json.dumps(payload, indent=2))
            return True
        except (OSError, RuntimeError):
            return False
