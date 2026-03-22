#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for prj0000015: enhanced common.py helpers."""

import json
from pathlib import Path

from src.tools.common import (
    ensure_dir,
    format_table,
    get_logger,
    load_config,
    retry,
)


def test_load_config_json(tmp_path: Path) -> None:
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({"key": "value"}))
    result = load_config(str(cfg))
    assert result == {"key": "value"}


def test_load_config_toml(tmp_path: Path) -> None:
    cfg = tmp_path / "config.toml"
    cfg.write_text('[section]\nname = "pyagent"\n')
    try:
        result = load_config(str(cfg))
        assert result["section"]["name"] == "pyagent"
    except RuntimeError:
        import pytest
        pytest.skip("TOML support unavailable (no tomllib/tomli)")


def test_ensure_dir_creates_nested(tmp_path: Path) -> None:
    target = tmp_path / "a" / "b" / "c"
    result = ensure_dir(target)
    assert result.is_dir()
    assert result == target


def test_ensure_dir_idempotent(tmp_path: Path) -> None:
    ensure_dir(tmp_path)  # already exists — should not raise
    assert tmp_path.is_dir()


def test_retry_succeeds_on_first_attempt() -> None:
    calls = []

    def fn():
        calls.append(1)
        return 42

    result = retry(fn, max_attempts=3)
    assert result == 42
    assert len(calls) == 1


def test_retry_retries_on_failure() -> None:
    calls = []

    def fn():
        calls.append(1)
        if len(calls) < 3:
            raise ValueError("not yet")
        return "done"

    result = retry(fn, max_attempts=5, delay=0.0)
    assert result == "done"
    assert len(calls) == 3


def test_retry_raises_after_max_attempts() -> None:
    import pytest

    def always_fail():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        retry(always_fail, max_attempts=2, delay=0.0)


def test_format_table_basic() -> None:
    output = format_table([["alice", 30], ["bob", 25]], ["Name", "Age"])
    assert "alice" in output
    assert "bob" in output
    assert "Name" in output
    assert "Age" in output


def test_format_table_alignment() -> None:
    output = format_table([["x", "y"]], ["Col1", "Col2"])
    lines = output.splitlines()
    # header, separator, data
    assert len(lines) == 3


def test_get_logger_returns_logger() -> None:
    import logging

    logger = get_logger("test_prj0000015")
    assert isinstance(logger, logging.Logger)
    # calling again should not add duplicate handlers
    logger2 = get_logger("test_prj0000015")
    assert logger is logger2
