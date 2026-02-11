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

import json
from src.core.agents.foreach_distributed import Worker
from src.core.base.common.utils.file_lock_manager import FileLockManager


def test_worker_claim_and_release(tmp_path):
    # Create a simple manifest with one shard assigned to worker-1
    manifest = {
        "shards": [
            {"id": 1, "worker": "worker-1", "files": ["a.py", "b.py"]}
        ]
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))

    scratch = tmp_path / "scratch"
    w = Worker("worker-1", scratch_dir=scratch, file_lock_manager=FileLockManager(), worker_timeout=5)

    assert w.claim_shard(manifest_path) is True

    # Check status file exists and shows locked
    status = json.loads((scratch / "worker-1.status.json").read_text())
    assert status["status"] == "locked"
    assert status["detail"]["acquired"] == 2

    # Release locks
    w.release_locks()
    status2 = json.loads((scratch / "worker-1.status.json").read_text())
    assert status2["status"] == "released"


def test_worker_claim_conflict(tmp_path):
    manifest = {
        "shards": [
            {"id": 1, "worker": "worker-1", "files": ["x.py"]}
        ]
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))

    scratch = tmp_path / "scratch"
    locker = FileLockManager()

    # Pre-acquire the lock to simulate conflict
    lock_id = "foreach:x.py"
    proxy = locker.acquire_lock(lock_id)
    assert proxy is not None

    w = Worker("worker-1", scratch_dir=scratch, file_lock_manager=locker, worker_timeout=1)
    ok = w.claim_shard(manifest_path)
    assert ok is False

    status = json.loads((scratch / "worker-1.status.json").read_text())
    assert status["status"] in ("lock_failed", "timeout")

    # Release the pre-acquired lock
    locker.release_lock(lock_id)
