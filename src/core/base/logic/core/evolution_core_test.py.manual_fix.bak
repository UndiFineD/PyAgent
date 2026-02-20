#!/usr/bin/env python3
"""Smoke test for EvolutionCore importability."""
try:
    from src.core.base.logic.core.evolution_core import EvolutionCore  # type: ignore
except Exception:  # pragma: no cover - test shim
    EvolutionCore = None  # type: ignore


def test_evolution_core_importable() -> None:
    if EvolutionCore is None:
        raise ImportError("EvolutionCore not importable")
    core = EvolutionCore()
    assert core is not None
