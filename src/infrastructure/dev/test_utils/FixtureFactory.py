#!/usr/bin/env python3
"""Minimal FixtureFactory shim."""


class FixtureFactory:
    def create(self, name, *_, **__):
        return None


__all__ = ["FixtureFactory"]
