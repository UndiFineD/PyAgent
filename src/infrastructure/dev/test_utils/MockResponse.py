#!/usr/bin/env python3
"""Minimal MockResponse shim."""


class MockResponse:
    def __init__(self, content="", status=200):
        self.content = content
        self.status = status


__all__ = ["MockResponse"]
