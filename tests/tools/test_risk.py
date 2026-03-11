#!/usr/bin/env python3
"""Unit tests for the risk matrix helper in the pm package."""

from tools.pm import risk


def test_risk_matrix_reader_writer(tmp_path) -> None:
    """Test that the risk matrix reader and writer functions work."""
    path = tmp_path / "risk.md"
    sample = "- Risk: test\n  Likelihood: low\n  Impact: low\n"
    path.write_text(sample)
    matrix = risk.read_matrix(str(path))
    assert isinstance(matrix, list)
    assert matrix[0]["Risk"] == "test"
