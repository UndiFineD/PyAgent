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


"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from dataclasses import dataclass
from typing import Optional

__version__ = VERSION

@dataclass
class ModernizationSuggestion:
    """Suggestion to modernize deprecated API usage.

    Attributes:
        old_api: The deprecated API being used.
        new_api: The modern replacement API.
        deprecation_version: Version where the old API was deprecated.
        removal_version: Version where it will be removed.
        migration_guide: URL or text explaining migration.
    """
    old_api: str
    new_api: str
    deprecation_version: str
    removal_version: str | None = None
    migration_guide: str = ""