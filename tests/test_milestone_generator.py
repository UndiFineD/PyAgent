#!/usr/bin/env python3
"""Test the milestone generator."""

import asyncio
from pathlib import Path

from src.roadmap import milestones


def test_generate_milestones(tmp_path: Path) -> None:
    """Test that the milestone generator can create a roadmap file with given milestones."""
    out = tmp_path / "roadmap.md"
    asyncio.run(milestones.create(out, ["Q1: start", "Q2: scale"]))
    text = out.read_text()
    assert "Q1" in text and "Q2" in text
