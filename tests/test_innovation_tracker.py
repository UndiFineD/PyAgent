#!/usr/bin/env python
"""Test the innovation tracker module."""

from pathlib import Path

from src.roadmap import innovation


def test_record_experiment(tmp_path: Path) -> None:
    """Test that record_experiment creates a file with the experiment name."""
    db = tmp_path / "experiments.json"
    path = innovation.record_experiment("test-exp", db_path=str(db))
    # result is typed Path
    assert path.exists()
    data = path.read_text()
    assert "test-exp" in data
