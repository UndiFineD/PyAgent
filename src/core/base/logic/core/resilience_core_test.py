#!/usr/bin/env python3
""
Minimal parser-safe tests for ResilienceCore.""
import importlib


def test_resilience_core_importable():
    mod = importlib.import_module('src.core.base.common.resilience_core')
    assert hasattr(mod, 'ResilienceCore')


def test_resilience_core_retry_decorator_exists():
    mod = importlib.import_module('src.core.base.common.resilience_core')
    assert hasattr(mod.ResilienceCore, 'retry')
