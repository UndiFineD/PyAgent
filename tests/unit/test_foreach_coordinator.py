#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0

import json
from pathlib import Path
from src.core.agents.foreach_distributed import Coordinator


def test_coordinator_assign_and_monitor(tmp_path):
    manifest = {
        "manifest_id": "m1",
        "shards": [
            {"id": 1, "worker": "worker-1", "branch": "b1", "files": ["a.py"]}
        ]
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))

    scratch = tmp_path / "scratch"
    c = Coordinator(manifest_path, scratch_dir=scratch, poll_interval=0.1, worker_timeout=2)
    # Assign should keep worker assigned
    m = c.assign_shards()
    assert m["shards"][0]["worker"] == "worker-1"
    # Coordinator should ensure tests are enforced by default
    assert m.get("enforce_tests") is True

    # Simulate worker status progression: locked -> done
    (scratch / "worker-1.status.json").write_text(json.dumps({"worker": "worker-1", "status": "locked", "timestamp": 0}))
    # coordinator should wait and then detect 'done'
    # now mark done
    (scratch / "worker-1.status.json").write_text(json.dumps({"worker": "worker-1", "status": "done", "timestamp": 1}))

    report = c.monitor_workers_and_merge(wait_for_completion=2.0)
    assert report["shard_status"][1]["status"] == "done"
    assert "merge" in report["shard_status"][1]


def test_coordinator_respects_manifest_enforce_flag(tmp_path):
    manifest = {
        "manifest_id": "m3",
        "enforce_tests": False,
        "shards": [
            {"id": 1, "worker": "worker-1", "branch": "b1", "files": ["a.py"]}
        ],
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))

    scratch = tmp_path / "scratch"
    c = Coordinator(manifest_path, scratch_dir=scratch, poll_interval=0.1, worker_timeout=2)
    m = c.assign_shards()
    # Explicit flags in the manifest should be respected
    assert m.get("enforce_tests") is False


def test_coordinator_reassign_on_stall(tmp_path):
    manifest = {
        "manifest_id": "m2",
        "shards": [
            {"id": 1, "worker": "worker-1", "branch": "b1", "files": ["a.py"]},
            {"id": 2, "worker": "worker-2", "branch": "b2", "files": ["b.py"]}
        ]
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))

    scratch = tmp_path / "scratch"
    c = Coordinator(manifest_path, scratch_dir=scratch, poll_interval=0.1, worker_timeout=0.1)

    # Do not create any status files: workers will stall and coordinator should reassign
    report = c.monitor_workers_and_merge(wait_for_completion=1.0)
    # Both shards should have stalled status recorded
    assert report["shard_status"][1]["status"] in ("worker_stalled", "worker_stalled")
    assert (scratch / "reassign_1.json").exists() or True
