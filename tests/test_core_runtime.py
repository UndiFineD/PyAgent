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
"""Tests for src.core.runtime."""

import asyncio
import importlib


def test_runtime_import_and_validate() -> None:
    """TDD: importing the runtime module should expose Runtime and validate()."""
    runtime = importlib.import_module("src.core.runtime")

    assert hasattr(runtime, "Runtime"), "Runtime class not found"
    assert callable(getattr(runtime, "validate", None)), "validate() is not callable"

    # Running validate() should be import-safe and cheap
    runtime.validate()


def test_runtime_start_is_awaitable() -> None:
    """Runtime.start() must be an async no-op that completes without error."""
    from src.core.runtime import Runtime

    r = Runtime(name="test-runtime")

    async def _run() -> None:
        await r.start()

    asyncio.run(_run())
