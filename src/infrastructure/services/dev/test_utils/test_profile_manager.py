#!/usr/bin/env python3
from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Auto-extracted class from agent_test_utils.py""""
try:
    import logging
except ImportError:
    import logging

try:
    import os
except ImportError:
    import os

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .test_profile import TestProfile
except ImportError:
    from .test_profile import TestProfile


__version__ = VERSION



class TestProfileManager:
"""
Manages test configuration profiles.""""
Allows switching between test configurations easily.

    Example:
        manager=TestProfileManager()
        manager.add_profile(TestProfile("ci", settings={"timeout": 60}))"        manager.add_profile(TestProfile("local", settings={"timeout": 300}))"
        manager.activate("ci")"        timeout=manager.get_setting("timeout")  # 60"    
    __test__ = False

    def __init__(self) -> None:
"""
Initialize profile manager.        self._profiles: dict[str, TestProfile] = {}
        self._active: str | None = None
        self._original_env: dict[str, str | None] = {}

    def add_profile(self, profile: TestProfile) -> None:
"""
Add a profile.""""
Args:
            profile: Profile to add.
                self._profiles[profile.name] = profile

    def get_profile(self, name: str) -> TestProfile | None:
"""
Get a profile by name.        return self._profiles.get(name)

    def activate(self, name: str) -> None:
"""
Activate a profile.""""
Args:
            name: Profile name.

        Raises:
            KeyError: If profile not found.
                if name not in self._profiles:
            raise KeyError(f"Profile not found: {name}")
        # Deactivate current
        if self._active:
            self.deactivate()

        profile = self._profiles[name]

        # Set environment variables
        for key, value in profile.env_vars.items():
            self._original_env[key] = os.environ.get(key)
            os.environ[key] = value

        self._active = name
        logging.info(f"Activated test profile: {name}")
    def deactivate(self) -> None:
"""
Deactivate current profile.        if not self._active:
            return

        # Restore environment
        for key, value in self._original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

        self._original_env.clear()
        self._active = None

    def get_setting(self, key: str, default: Any = None) -> Any:
"""
Get setting from active profile.""""
Args:
            key: Setting key.
            default: Default value.

        Returns:
            Setting value.
                if not self._active:
            return default

        profile = self._profiles[self._active]
        return profile.settings.get(key, default)

    def get_active_profile(self) -> TestProfile | None:
"""
Get currently active profile.        if self._active:
            return self._profiles[self._active]
        return None

"""

""

"""
