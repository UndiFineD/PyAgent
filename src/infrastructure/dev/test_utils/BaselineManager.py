#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Minimal shim for BaselineManager used by tests during collection.

This file provides a tiny placeholder to satisfy import-time references
while the test-shim repair loop proceeds.
"""


class BaselineManager:
    """Lightweight placeholder BaselineManager.

    Implement only what's necessary for import-time resolution.
    Tests that need real behavior should use the real implementation.
    """

    def __init__(self, *_, **__):
        self._baselines = {}

    def register(self, name, value):
        self._baselines[name] = value

    def get(self, name, default=None):
        return self._baselines.get(name, default)


__all__ = ["BaselineManager"]
