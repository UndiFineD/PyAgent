#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0

import time
from src.core.base.common.resilience_core import ResilienceCore


def test_retry_uses_injected_sleep(monkeypatch):
    calls = []

    def fake_sleep(secs):
        calls.append(secs)

    @ResilienceCore.retry(retries=2, delay=0.01, backoff=1, exceptions=(RuntimeError,), sleep_fn=fake_sleep)
    def flaky():
        if calls:
            return "ok"
        raise RuntimeError("fail")

    assert flaky() == "ok"
    assert any(c > 0 for c in calls)


def test_retry_fallback_wait(monkeypatch):
    # Ensure that providing None sleep_fn falls back to an Event.wait-based sleep
    counts = {"attempts": 0}

    @ResilienceCore.retry(retries=1, delay=0.01, backoff=1, exceptions=(RuntimeError,), sleep_fn=None)
    def flaky2():
        counts["attempts"] += 1
        if counts["attempts"] > 1:
            return "ok"
        raise RuntimeError("fail")

    assert flaky2() == "ok"
