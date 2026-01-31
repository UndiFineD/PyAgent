#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0

import logging
from src.core.base.common.registry_core import RegistryCore


def test_hook_failure_logged(caplog):
    r = RegistryCore("test")

    def bad_hook(key, item):
        raise ValueError("bad")

    r.add_hook("on_register", bad_hook)
    with caplog.at_level(logging.ERROR):
        r.register("k", "v")
        assert "Registry hook 'on_register' failed" in caplog.text


def test_rust_detect_cycles_fallback(monkeypatch):
    import src.core.base.common.registry_core as mod

    class BadRC:
        def detect_cycles_rust(self, *args, **kwargs):
            raise RuntimeError("boom")

    orig = getattr(mod, "rc", None)
    mod.rc = BadRC()

    r = RegistryCore()
    # Should not raise and return None so Python fallback kicks in
    assert r._try_rust_detect_cycles([], []) is None

    mod.rc = orig
