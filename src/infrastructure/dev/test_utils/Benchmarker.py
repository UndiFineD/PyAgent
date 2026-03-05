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

"""Minimal Benchmarker shim used during test collection.

Provides a tiny placeholder class so imports succeed during iterative fixes.
"""


class Benchmarker:
    def __init__(self, *_, **__):
        self.results = []

    def start(self, name=None):
        return None

    def stop(self, token=None):
        return None

    def record(self, name, value):
        self.results.append((name, value))


__all__ = ["Benchmarker"]
