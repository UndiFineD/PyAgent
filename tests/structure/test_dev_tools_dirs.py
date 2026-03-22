#!/usr/bin/env python3
"""Tests for the development tools directory structure."""

from pathlib import Path


def test_dev_tools_structure(tmp_path: Path) -> None:
    """`src/tools` and `docs/` should be created by the setup helper."""
    from scripts.setup_structure import create_core_structure

    create_core_structure(str(tmp_path))
    # verify development‑tools locations
    assert (tmp_path / "src" / "tools").exists()
    assert (tmp_path / "docs").exists()


def test_required_tool_modules_exist() -> None:
    """Core tool modules must be present on the filesystem."""
    import src.tools  # noqa: F401 — triggers auto-registration

    tool_root = Path("src/tools")
    required = [
        "common.py",
        "git_utils.py",
        "metrics.py",
        "remote.py",
        "ssl_utils.py",
        "tool_registry.py",
        "__init__.py",
        "__main__.py",
    ]
    for module_file in required:
        assert (tool_root / module_file).exists(), f"Missing: {module_file}"


def test_pm_subpackage_exists() -> None:
    """The `pm` subpackage must contain its three helper modules."""
    pm_root = Path("src/tools/pm")
    assert pm_root.is_dir(), "src/tools/pm/ directory missing"
    for name in ("__init__.py", "kpi.py", "email.py", "risk.py"):
        assert (pm_root / name).exists(), f"Missing pm module: {name}"


def test_tools_package_importable() -> None:
    """Importing src.tools should not raise."""
    import importlib

    mod = importlib.import_module("src.tools")
    assert mod is not None
