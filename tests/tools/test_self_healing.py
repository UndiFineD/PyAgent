#!/usr/bin/env python3
"""Tests for the self-healing module in the tools directory."""
from pathlib import Path


def test_self_healing_detects(tmp_path: Path) -> None:
    """The tools.self_heal module should be importable and its detect_misconfig function should return a dict."""
    from scripts.setup_structure import create_core_structure
    create_core_structure(str(tmp_path))

    import importlib.util
    import sys
    sys.path.insert(0, str(tmp_path / "src"))
    spec = importlib.util.find_spec("tools.self_heal")
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    assert hasattr(module, "detect_misconfig")
    info = module.detect_misconfig()
    assert isinstance(info, dict)
