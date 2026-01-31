#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import json
import time
import pytest
from pathlib import Path

from src.core.agents.foreach_distributed import Worker


def test_claim_shard_with_injected_sleep(tmp_path, monkeypatch):
    # Prepare a manifest file with a single shard assigned to worker-1
    manifest = {
        "shards": [
            {"id": 1, "worker": "worker-1", "files": ["a.txt", "b.txt"]}
        ]
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))

    calls = []

    def fake_sleep(s):
        calls.append(s)

    # Create a worker with injected fake sleep and a locker that fails first
    w = Worker("worker-1", scratch_dir=tmp_path, sleep_fn=fake_sleep)

    # Monkeypatch claim_shard to simulate two failures then success
    states = [False, False, True]

    def fake_claim(p):
        return states.pop(0)

    monkeypatch.setattr(w, "claim_shard", fake_claim)

    # Should eventually return True and have called fake_sleep twice
    res = w.claim_shard_with_retries(manifest_path, retries=2, delay=0.1, backoff=2.0)
    assert res is True
    assert len(calls) == 2
    assert calls[0] == pytest.approx(0.1, rel=0.01)
    assert calls[1] == pytest.approx(0.2, rel=0.01)
