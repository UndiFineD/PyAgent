#!/usr/bin/env python3
"""Test the prioritization module."""


def test_score_feature() -> None:
    """Test that the score_feature function can be imported and returns a number."""
    from roadmap import prioritization

    attrs = {"impact": 10, "effort": 2}
    score = prioritization.score_feature(attrs)
    assert isinstance(score, (int, float))
