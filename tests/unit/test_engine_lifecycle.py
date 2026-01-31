#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0

from src.infrastructure.engine.engine_lifecycle import EngineLifecycleManager


def test_sleep_briefly_uses_injected_sleep():
    called = {"t": 0}

    def fake_sleep(t):
        called["t"] += 1

    mgr = EngineLifecycleManager(sleep_fn=fake_sleep)
    mgr._sleep_briefly()
    assert called["t"] == 1
