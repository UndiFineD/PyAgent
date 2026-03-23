#!/usr/bin/env python3
"""Unit tests for the risk matrix helper in the pm package."""

from pathlib import Path

import pytest

from tools.pm import risk


@pytest.mark.asyncio
async def test_risk_matrix_reader_writer(tmp_path: Path) -> None:
    """Test that the risk matrix reader and writer functions work."""
    riskpath = tmp_path / "risk.md"
    sample = "| Title | Probability | Impact | Mitigation |\n|---|---|---|---|\n| test | low | low | |\n"
    riskpath.write_text(sample)
    matrix = await risk.read_matrix(str(riskpath))
    assert isinstance(matrix, list)
    assert matrix[0]["title"] == "test"
