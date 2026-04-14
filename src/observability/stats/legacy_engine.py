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

"""Legacy synchronous engine used for demonstration of migration."""

from __future__ import annotations

from runtime_py import sleep, spawn

counter: int = 0


def start_loop() -> None:
    """Schedule the asynchronous ticking loop on the global runtime.

    Previous versions blocked the caller with a ``while True``; the new
    implementation spawns an async task so that other work can continue.
    """

    async def _tick() -> None:
        global counter
        while True:  # this loop is asynchronous so it's allowed
            counter += 1
            await sleep(1)  # pause a second between increments

    spawn(_tick())


def get_count() -> int:
    """Return the current value of the counter."""
    return counter
