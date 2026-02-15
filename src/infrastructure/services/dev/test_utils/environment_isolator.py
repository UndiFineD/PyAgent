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


"""Auto-extracted class from agent_test_utils.py
"""

from __future__ import annotations

import os
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class EnvironmentIsolator:
    """Context manager that restores environment variables on exit."""

    def __init__(self) -> None:
        self._original: dict[str, str] = {}

    def __enter__(self) -> EnvironmentIsolator:
        self._original = dict(os.environ)
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        os.environ.clear()
        os.environ.update(self._original)

    def set_env(self, key: str, value: str) -> None:
        os.environ[str(key)] = str(value)
