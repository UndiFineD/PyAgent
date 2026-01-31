#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0

import threading
import time
from typing import Any

from src.infrastructure.swarm.fleet.mixins.fleet_update_mixin import FleetUpdateMixin


class DummyFleet(FleetUpdateMixin):
    def __init__(self):
        self.calls = 0
        self.kill_switch = False

    def _run_git_pull(self) -> None:
        self.calls += 1


def test_fleet_update_service_runs_and_is_interruptible():
    d = DummyFleet()

    calls = {"sleep": 0}

    def sleep_fn(secs: float) -> None:
        # Small artificial delay; flip kill switch after a couple sleeps
        calls["sleep"] += 1
        threading.Event().wait(0.01)
        if calls["sleep"] >= 2:
            d.kill_switch = True

    d.init_update_service(interval_seconds=1, sleep_fn=sleep_fn)

    # Wait for the background thread to run a couple iterations
    timeout = time.time() + 2.0
    while time.time() < timeout and d.calls < 1:
        threading.Event().wait(0.01)

    # Stop service if still running
    d.stop_update_service()

    assert d.calls >= 1
    assert calls["sleep"] >= 1
