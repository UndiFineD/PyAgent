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

<<<<<<< HEAD
<<<<<<< HEAD
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""
Core logic for execution profiles and configuration management.
"""

from __future__ import annotations
<<<<<<< HEAD
<<<<<<< HEAD

from typing import Any, Dict, Optional

from .base_core import BaseCore
from .models import ExecutionProfile

=======
from typing import Any, Dict, Optional
from .base_core import BaseCore
from .models import ExecutionProfile, ConfigProfile
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
from typing import Any, Dict, Optional
from .base_core import BaseCore
from .models import ExecutionProfile, ConfigProfile
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

class ProfileCore(BaseCore):
    """
    Authoritative engine for managing execution settings and profiles.
    """

    def __init__(self) -> None:
        super().__init__()
        self._profiles: Dict[str, ExecutionProfile] = {}
        self._active: Optional[str] = None
        self._register_defaults()

<<<<<<< HEAD
<<<<<<< HEAD
    @property
    def profiles(self) -> Dict[str, ExecutionProfile]:
        """Returns the dictionary of registered profiles."""
        return self._profiles

    @property
    def active_profile(self) -> Optional[ExecutionProfile]:
        """Returns the currently active profile."""
        if self._active:
            return self._profiles.get(self._active)
        return None

    def _register_defaults(self) -> None:
        """Registers default execution profiles."""
        self._profiles["default"] = ExecutionProfile(name="default", timeout=120)
        self._profiles["fast"] = ExecutionProfile(name="fast", timeout=60, parallel=True, workers=4)
        self._profiles["ci"] = ExecutionProfile(name="ci", timeout=300, config={"dry_run": True})

    def activate(self, name: str) -> None:
        """
        Sets the specified profile as active.
        """
        if name in self._profiles:
            self._active = name

    def add_profile(self, profile: Any) -> None:
        """
        Registers a new execution profile.
        Supports both ExecutionProfile and ConfigProfile.
        """
        name = getattr(profile, "name", str(profile))
        self._profiles[name] = profile

    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a setting from the active profile, with inheritance support.
        """
        profile = self.get_active_profile()
        if not profile:
            return default

        # Check in current profile
        if hasattr(profile, "settings") and key in profile.settings:
            return profile.settings[key]
        if hasattr(profile, "get"):
            val = profile.get(key)
            if val is not None:
                return val

        # Check in parent if it's a ConfigProfile
        parent_name = getattr(profile, "parent", None)
        if parent_name and parent_name in self._profiles:
            parent = self._profiles[parent_name]
            if hasattr(parent, "settings") and key in parent.settings:
                return parent.settings[key]
            if hasattr(parent, "get"):
                return parent.get(key, default)

        return default

    def get_active_profile(self) -> Any:
        """
        Retrieves the currently active execution profile instance.
        """
        if self._active:
            return self._profiles.get(self._active)
        return self._profiles.get("default")

    def get_active(self) -> Optional[ExecutionProfile]:
        """
        Compatibility method for returning ExecutionProfile.
        """
        profile = self.get_active_profile()
        if isinstance(profile, ExecutionProfile):
            return profile
        return None
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def _register_defaults(self) -> None:
        self._profiles["default"] = ExecutionProfile(name="default", timeout=120)
        self._profiles["fast"] = ExecutionProfile(name="fast", timeout=60, parallel=True, workers=4)

    def activate(self, name: str) -> None:
        if name in self._profiles:
            self._active = name

    def get_active(self) -> Optional[ExecutionProfile]:
        if self._active:
            return self._profiles.get(self._active)
        return self._profiles.get("default")
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
