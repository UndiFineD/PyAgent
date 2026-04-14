#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the minimal runtime scaffold."""

from __future__ import annotations

import asyncio


def test_runtime_validate_and_start() -> None:
    """Runtime.validate should run and start must be awaitable."""
    from src.core import runtime

    # validate should not raise
    runtime.validate()

    # start should be an async coroutine that can be awaited
    r = runtime.Runtime()
    assert callable(getattr(r, "start", None))
    asyncio.run(r.start())
