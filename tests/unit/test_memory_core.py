#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0

from src.core.base.common.memory_core import MemoryCore


def test_store_knowledge_success(monkeypatch, tmp_path):
    m = MemoryCore()

    def fake_save_json(self, path, content):
        # Ensure it's called with a Path-like and content
        assert path is not None
        return True

    monkeypatch.setattr(m, "_storage", type("S", (), {"save_json": fake_save_json})())
    ok = m.store_knowledge("agent1", "key1", {"a": 1}, mode="structured")
    assert ok is True


def test_store_knowledge_failure(monkeypatch):
    m = MemoryCore()

    def bad_save_json(path, content):
        raise OSError("disk full")

    monkeypatch.setattr(m, "_storage", type("S", (), {"save_json": bad_save_json})())
    ok = m.store_knowledge("agent1", "key1", {"a": 1}, mode="structured")
    assert ok is False
