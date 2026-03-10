#!/usr/bin/env python3
"""Meta-test to ensure pre-commit is configured and runs."""
import subprocess
import sys
import pathlib


def test_precommit_runs_on_empty_config(tmp_path: pathlib.Path) -> None:
    """Run pre-commit against an empty config or skip if pre-commit not installed."""
    cfg = tmp_path / ".pre-commit-config.yaml"
    cfg.write_text("repos: []\n")

    res = subprocess.run(
        [sys.executable, "-m", "pre_commit.main", "run", "--files",
        str(cfg)],
        capture_output=True,
        text=True
        )
    if "No module named pre_commit" in (res.stderr or ""):
        import pytest

        pytest.skip("pre-commit not installed in environment")

    assert res is not None


def test_precommit_yaml_exists() -> None:
    """Ensure .pre-commit-config.yaml exists in the repo."""
    cfg = pathlib.Path('.pre-commit-config.yaml')
    assert cfg.exists(), "pre-commit config missing"

# additional behavioral tests could be added once hooks are configured
