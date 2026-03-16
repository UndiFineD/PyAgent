#!/usr/bin/env python3
"""Test that the vision package's template function works as expected."""

from pathlib import Path

from roadmap import vision


def test_vision_template_exists(tmp_path: Path) -> None:
    """The vision package should have a get_template function that returns a string."""
    # template function should return a non-empty string
    text = vision.get_template()
    assert isinstance(text, str) and "Vision" in text
