#!/usr/bin/env python3
"""Tests for the dependency audit tool."""
from pathlib import Path


def test_dependency_audit_returns_list(tmp_path: Path) -> None:
    """`check_dependencies` should exist and return a list (empty or not)."""
    # ensure layout
    from scripts.setup_structure import create_core_structure
    create_core_structure(str(tmp_path))

    import importlib.util, sys
    sys.path.insert(0, str(tmp_path / "src"))
    spec = importlib.util.find_spec("tools.dependency_audit")
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    assert hasattr(module, "check_dependencies")
    result = module.check_dependencies()
    assert isinstance(result, list)
