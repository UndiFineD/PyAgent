#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""Lightweight CleanupManager shim used during pytest collection.

Provides a minimal `CleanupManager` class to satisfy imports in
`src.infrastructure.dev.test_utils` during iterative repair.
"""


class CleanupManager:
    def __init__(self, *_, **__):
        self._items = []

    def register(self, fn):
        self._items.append(fn)

    def run_all(self):
        for fn in list(self._items):
            try:
                fn()
            except Exception:
                pass


__all__ = ["CleanupManager"]
