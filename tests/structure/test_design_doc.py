#!/usr/bin/env python3
"""Tests for the design document presence."""

import os


def test_design_doc_present() -> None:
    """The design document should be present in the expected location."""
    assert os.path.exists(".github/superpower/brainstorm/2026-03-09-core_project_structure_design.md")
