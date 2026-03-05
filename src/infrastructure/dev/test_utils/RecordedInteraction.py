#!/usr/bin/env python3
"""RecordedInteraction shim for pytest collection."""


class RecordedInteraction:
    def __init__(self, input=None, output=None, meta=None):
        self.input = input
        self.output = output
        self.meta = meta or {}

    def to_dict(self):
        return {"input": self.input, "output": self.output, "meta": self.meta}


__all__ = ["RecordedInteraction"]
