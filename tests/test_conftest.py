#!/usr/bin/env python3
# pyright: reportPrivateUsage=false
"""Combined tests for the pytest shim in `conftest.py`.

This file merges the old `test_conftest_typing_contract.py` and
`test_conftest_import_fixer_resolution.py` tests.  The original typing
contract tests locked the behaviour while we added type annotations; the
import‑fixer tests verify that the path‑resolution logic still prefers
`scripts/` over `scripts-old/` and falls back correctly.

When we began this work there were 22 static analysis errors in
`conftest.py` (unused ignores, broad excepts, protected member access,
`importlib.util` attribute complaints, etc.).  The goal was to fix them
all without changing runtime behaviour, and the current version is clean
– `get_errors` reports **no errors**.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock, patch

import pytest


def _load_repo_root_conftest() -> ModuleType:
    """Load the repository-root conftest module by file path.

    Returns:
        Loaded module object for the repository root conftest.

    Raises:
        RuntimeError: If the module spec cannot be created or loaded.

    """
    root_conftest_path = Path(__file__).resolve().parents[1] / "conftest.py"
    spec = importlib.util.spec_from_file_location("repo_root_conftest", root_conftest_path)
    if spec is None or spec.loader is None:
        msg = f"Unable to load repository root conftest from {root_conftest_path}"
        raise RuntimeError(msg)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


repo_conftest = _load_repo_root_conftest()


def test_session_finish_sets_exitstatus_when_git_dirty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify session_finish sets exitstatus=1 when git status shows modifications."""
    _ = tmp_path
    _ = monkeypatch
    # first call (during SessionManager init) returns clean status
    mock_baseline = Mock()
    mock_baseline.stdout = ""
    # second call (during session_finish) shows a modification
    mock_dirty = Mock()
    mock_dirty.stdout = " M conftest.py\n"

    with patch("subprocess.run", side_effect=[mock_baseline, mock_dirty]):
        mgr = repo_conftest.SessionManager(tmp_path)
        # simulate pytest_sessionstart hook to establish baseline
        mgr.session_start(Mock())
        mock_session = Mock()
        mock_session.exitstatus = 0
        mgr.session_finish(mock_session, 0)
        assert mock_session.exitstatus == 1, "exitstatus should be set to 1 when git shows changes"


def test_session_finish_does_not_raise_with_minimal_session() -> None:
    """Verify session_finish works with minimal session object that has exitstatus attribute."""
    mock_session = Mock()
    mock_session.exitstatus = 0

    mock_result = Mock()
    mock_result.stdout = ""

    with patch("subprocess.run", return_value=mock_result):
        try:
            repo_conftest._mgr.session_finish(mock_session, 0)
        except AttributeError as e:
            pytest.fail(f"session_finish raised AttributeError with minimal session: {e}")


def test_resolve_import_fixer_prefers_scripts_then_scripts_old(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify _resolve_import_fixer prefers scripts/ then scripts-old/ directories."""
    # parameters unused below
    _ = tmp_path
    _ = monkeypatch
    scripts_dir = tmp_path / "scripts"
    scripts_old_dir = tmp_path / "scripts-old"
    scripts_dir.mkdir()
    scripts_old_dir.mkdir()

    scripts_fixer = scripts_dir / "fix_leading_imports.py"
    scripts_old_fixer = scripts_old_dir / "fix_leading_imports.py"

    mgr = repo_conftest.SessionManager(tmp_path)
    resolver = mgr._resolve_import_fixer

    scripts_old_fixer.touch()
    result = resolver()
    assert result == scripts_old_fixer, "Should find scripts-old when scripts doesn't exist"
    scripts_old_fixer.unlink()

    scripts_fixer.touch()
    result = resolver()
    assert result == scripts_fixer, "Should find scripts when it exists"

    scripts_old_fixer.touch()
    result = resolver()
    assert result == scripts_fixer, "Should prefer scripts/ over scripts-old/ when both exist"

    scripts_fixer.unlink()
    scripts_old_fixer.unlink()
    result = resolver()
    assert result is None, "Should return None when neither location exists"


def test_resolve_import_fixer_prefers_scripts_dir(tmp_path: Path) -> None:
    """When fixer exists in both places, scripts/ should be preferred."""
    scripts = tmp_path / "scripts"
    scripts_old = tmp_path / "scripts-old"
    scripts.mkdir()
    scripts_old.mkdir()

    expected = scripts / "fix_leading_imports.py"
    expected.write_text("print('new')\n", encoding="utf-8")
    (scripts_old / "fix_leading_imports.py").write_text("print('old')\n", encoding="utf-8")

    manager = repo_conftest.SessionManager(tmp_path)
    resolver = manager._resolve_import_fixer
    resolved = resolver()

    assert resolved == expected


def test_resolve_import_fixer_falls_back_to_scripts_old(tmp_path: Path) -> None:
    """When scripts/ is missing, resolver should use scripts-old/."""
    scripts_old = tmp_path / "scripts-old"
    scripts_old.mkdir()

    expected = scripts_old / "fix_leading_imports.py"
    expected.write_text("print('fallback')\n", encoding="utf-8")

    manager = repo_conftest.SessionManager(tmp_path)
    resolver = manager._resolve_import_fixer
    resolved = resolver()

    assert resolved == expected


def test_resolve_import_fixer_returns_none_when_missing(tmp_path: Path) -> None:
    """Resolver should return None when fixer script is absent in both locations."""
    manager = repo_conftest.SessionManager(tmp_path)
    resolver = manager._resolve_import_fixer

    assert resolver() is None
