#!/usr/bin/env python3
# Refactored by copilot-placeholder
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

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

from .import_source import ImportSource

__version__ = VERSION


@dataclass
class ImportedEntry:
    """An entry imported from external source.

    Attributes:
        source: Where the entry was imported from.
        external_id: ID in the external system.
        title: Entry title.
        description: Entry description.
        author: Author of the entry.
        created_at: When the entry was created.
        labels: Labels / tags from the source.
    """

    source: ImportSource
    external_id: str
    title: str
    description: str
    author: str = ""
    created_at: str = ""
    labels: list[str] = field(default_factory=lambda: [])
