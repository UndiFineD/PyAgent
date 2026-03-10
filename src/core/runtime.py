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
"""Minimal Runtime core scaffold for PyAgent.

This module provides a tiny, import-safe Runtime class and a validate()
hook used by meta-tests and CI to ensure core module health.
"""

from __future__ import annotations
import asyncio
from dataclasses import dataclass


@dataclass
class Runtime:
    """Minimal runtime that manages task lifecycle (synchronous-safe)."""
    name: str = "runtime"

    async def start(self) -> None:
        """Start the runtime — minimal no-op async function."""
        # non-blocking no-op to satisfy async contract
        await asyncio.sleep(0)


def validate() -> None:
    """Lightweight import-safe validation hook."""
    r = Runtime()
    # ensure start is present and awaitable when called
    assert callable(getattr(r, "start", None))
