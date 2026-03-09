#!/usr/bin/env python3
"""Tests for KPI computation functions in the tools directory."""
from tools.pm import kpi


def test_compute_throughput_function():
    """Test that the compute_throughput function exists and returns an integer."""
    assert hasattr(kpi, "compute_throughput")
    assert isinstance(kpi.compute_throughput([], []), int)
