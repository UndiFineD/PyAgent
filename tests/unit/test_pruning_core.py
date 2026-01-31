#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0

from src.core.base.common.pruning_core import PruningCore


def test_calculate_decay_python_fallback(monkeypatch):
    # Simulate rc being present but failing
    import src.core.base.common.pruning_core as mod

    class BadRC:
        def calculate_decay_rust(self, *args, **kwargs):
            raise RuntimeError("boom")

    orig = getattr(mod, "rc", None)
    mod.rc = BadRC()

    pc = PruningCore()
    # Should not raise and should return a float fallback
    val = pc.calculate_decay(1.0, half_life=3600.0, current_weight=1.0)
    assert isinstance(val, float)

    mod.rc = orig


def test_update_weight_on_fire_python_fallback(monkeypatch):
    import src.core.base.common.pruning_core as mod

    class BadRC:
        def update_weight_on_fire_rust(self, *args, **kwargs):
            raise RuntimeError("boom")

    orig = getattr(mod, "rc", None)
    mod.rc = BadRC()

    pc = PruningCore()
    w = pc.update_weight_on_fire("agent-x", True)
    assert isinstance(w, float)

    mod.rc = orig


def test_is_in_refractory_python_fallback(monkeypatch):
    import src.core.base.common.pruning_core as mod

    class BadRC:
        def is_in_refractory_rust(self, *args, **kwargs):
            raise RuntimeError("boom")

    orig = getattr(mod, "rc", None)
    mod.rc = BadRC()

    pc = PruningCore()
    # Ensure not in refractory for new agent
    assert pc.is_in_refractory("unknown") is False

    mod.rc = orig
