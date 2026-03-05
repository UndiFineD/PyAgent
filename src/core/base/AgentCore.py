#!/usr/bin/env python3
from __future__ import annotations
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



from typing import Any


class BaseCore:
    """Lightweight stub of the real BaseCore used at import time."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._state = {}

    def initialize(self) -> None:
        """No-op initialize for collection-time safety."""
        return

    def shutdown(self) -> None:
        """No-op shutdown."""
        return

    def configure(self, **kwargs: Any) -> None:
        """Accept configuration without side-effects."""
        self._state.update(kwargs)


__all__ = ["BaseCore"]
