#!/usr/bin/env python3
"""Minimal PerformanceMetric shim."""


class PerformanceMetric:
    def __init__(self, name, value=0):
        self.name = name
        self.value = value


__all__ = ["PerformanceMetric"]
