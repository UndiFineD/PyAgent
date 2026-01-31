#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0

import json
import time
import threading
import asyncio
from pathlib import Path
from src.core.agents.foreach_distributed import Worker, Coordinator
from src.core.base.common.utils.file_lock_manager import FileLockManager


def test_claim_with_retries_waits_for_lock(tmp_path):
    manifest = {"shards": [{"id": 1, "worker": "worker-1", "files": ["x.py"]}]}
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))

    scratch = tmp_path / "scratch"
    locker = FileLockManager()
    # Pre-acquire the lock and release after 0.5s
    lock_id = "foreach:x.py"
    proxy = locker.acquire_lock(lock_id)
    assert proxy is not None

    def release_l():
        time.sleep(0.5)
        locker.release_lock(lock_id)

    threading.Thread(target=release_l, daemon=True).start()

    w = Worker("worker-1", scratch_dir=scratch, file_lock_manager=locker, worker_timeout=5)
    ok = w.claim_shard_with_retries(manifest_path, retries=5, delay=0.1, backoff=1.5)
    assert ok is True
    status = json.loads((scratch / "worker-1.status.json").read_text())
    assert status["status"] == "locked"


def test_leader_election(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps({"shards": []}))
    scratch = tmp_path / "scratch"

    c1 = Coordinator(manifest_path, scratch_dir=scratch, worker_timeout=1)
    c2 = Coordinator(manifest_path, scratch_dir=scratch, worker_timeout=1)

    assert c1.elect_leader("leader1") is True
    assert c2.elect_leader("leader2") is False

    # Wait for TTL expiry then allow takeover
    time.sleep(c1.leader_ttl + 0.1)
    assert c2.elect_leader("leader2") is True


def test_async_claim(monkeypatch, tmp_path):
    manifest = {"shards": [{"id": 1, "worker": "worker-1", "files": ["a.py"]}]}
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))

    scratch = tmp_path / "scratch"
    w = Worker("worker-1", scratch_dir=scratch, file_lock_manager=FileLockManager(), worker_timeout=2)

    async def run():
        ok = await w.claim_shard_async(manifest_path, retries=1, delay=0.1)
        assert ok is True

    asyncio.run(run())
