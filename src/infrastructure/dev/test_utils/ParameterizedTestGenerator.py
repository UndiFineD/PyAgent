#!/usr/bin/env python3
"""Minimal ParameterizedTestGenerator shim."""


class ParameterizedTestGenerator:
    def generate(self, fn, params):
        for p in params:
            fn(*p)


__all__ = ["ParameterizedTestGenerator"]
