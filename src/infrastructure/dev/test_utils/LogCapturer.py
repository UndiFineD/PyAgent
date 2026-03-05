#!/usr/bin/env python3
"""Minimal LogCapturer shim."""


class LogCapturer:
    def __init__(self, *_, **__):
        pass

    def start(self):
        return None

    def stop(self):
        return None


__all__ = ["LogCapturer"]
