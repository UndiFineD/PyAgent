#!/usr/bin/env python3
"""Smoke test for GoalSettingCore importability."""
try:
    from src.core.base.logic.core.goal_setting_core import GoalSettingCore  # type: ignore
except Exception:  # pragma: no cover - test shim
    GoalSettingCore = None  # type: ignore


def test_goal_setting_core_importable() -> None:
    if GoalSettingCore is None:
        raise ImportError("GoalSettingCore not importable")
    core = GoalSettingCore()
    assert core is not None
