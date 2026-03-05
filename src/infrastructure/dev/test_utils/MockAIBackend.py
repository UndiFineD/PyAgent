#!/usr/bin/env python3
"""Minimal MockAIBackend shim."""


class MockAIBackend:
    def __init__(self, *_, **__):
        pass

    def respond(self, *_, **__):
        return ""


__all__ = ["MockAIBackend"]
