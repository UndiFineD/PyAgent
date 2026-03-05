#!/usr/bin/env python3
"""Minimal FixtureGenerator shim."""


class FixtureGenerator:
    def generate(self, *_, **__):
        return []


__all__ = ["FixtureGenerator"]
