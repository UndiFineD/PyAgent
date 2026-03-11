#!/usr/bin/env python3
"""Tests for the data generation script."""
from pathlib import Path

from scripts.generate_test_data import generate_sample_fixture


def test_data_script(tmp_path: Path) -> None:
    """The data generation script should create a fixture file
    with expected content.
    """
    file = tmp_path / "fixture.json"
    generate_sample_fixture(str(file))
    assert file.read_text() == "{}"
