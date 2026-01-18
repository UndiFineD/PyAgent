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


"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from .ChangelogEntry import ChangelogEntry
from dataclasses import dataclass, field

__version__ = VERSION


@dataclass
class MonorepoEntry:
    """Changelog entry for monorepo aggregation.

    Attributes:
        package_name: Name of the package.
        version: Package version.
        entries: List of changelog entries for this package.
        path: Path to the package in the repo.
    """

    package_name: str
    version: str
    entries: list[ChangelogEntry] = field(default_factory=lambda: [])
    path: str = ""
