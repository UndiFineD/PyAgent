#!/usr/bin/env python3
"""Minimal parser-safe tests for pruning core."""

import importlib


def test_pruning_core_importable():
    mod = importlib.import_module('src.core.base.common.pruning_core')
    assert hasattr(mod, 'PruningCore')


def test_pruning_core_basic_instance():
    mod = importlib.import_module('src.core.base.common.pruning_core')
    pc = mod.PruningCore()
    # Basic sanity: methods exist
    assert hasattr(pc, 'calculate_decay')
    assert hasattr(pc, 'update_weight_on_fire')
    assert hasattr(pc, 'is_in_refractory')
