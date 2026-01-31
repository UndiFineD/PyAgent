#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import threading
import pytest

from src.core.base.common.resilience_core import ResilienceCore


def test_retry_uses_threading_event_wait(monkeypatch):
    called = {"wait": False}

    def fake_wait(self, timeout):
        called["wait"] = True

    # Patch Event.wait so the default _wait uses our fake
    monkeypatch.setattr(threading.Event, "wait", fake_wait, raising=False)

    @ResilienceCore.retry(retries=1, delay=0.001, backoff=2.0)
    def flaky():
        raise ValueError("fail")

    with pytest.raises(ValueError):
        flaky()

    assert called["wait"] is True
