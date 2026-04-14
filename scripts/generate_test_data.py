#!/usr/bin/env python3
"""Script to generate test data fixtures."""


def generate_sample_fixture(path: str) -> None:
    """Generate a sample fixture file with empty JSON content."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("{}")
