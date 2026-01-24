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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Core logic for execution profiles and configuration management.
"""

from __future__ import annotations

from typing import Dict, Optional

from .base_core import BaseCore
from .models import ExecutionProfile


class ProfileCore(BaseCore):
    """
    Authoritative engine for managing execution settings and profiles.
    """

    def __init__(self) -> None:
        super().__init__()
        self._profiles: Dict[str, ExecutionProfile] = {}
        self._active: Optional[str] = None
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Registers default execution profiles."""
        self._profiles["default"] = ExecutionProfile(name="default", timeout=120)
        self._profiles["fast"] = ExecutionProfile(name="fast", timeout=60, parallel=True, workers=4)

    def activate(self, name: str) -> None:
        """
        Sets the specified profile as active.
        """
        if name in self._profiles:
            self._active = name

    def get_active(self) -> Optional[ExecutionProfile]:
        """
        Retrieves the currently active execution profile.
        """
        if self._active:
            return self._profiles.get(self._active)
        return self._profiles.get("default")
