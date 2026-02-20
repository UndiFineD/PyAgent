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


"""Types: ReleaseNote dataclass."""

from dataclasses import dataclass, field

try:
    from src.core.base.lifecycle.version import VERSION
except Exception:  # pragma: no cover - fallback
    VERSION = "0.0.0"

__version__ = VERSION


@dataclass
class ReleaseNote:
    """Generated release notes.

    Attributes:
        version: Release version.
        title: Release title.
        summary: Brief summary.
        highlights: Key highlights.
        breaking_changes: List of breaking changes.
        full_changelog: Complete changelog text.
    """
    version: str
    title: str
    summary: str
    highlights: list[str] = field(default_factory=list)
    breaking_changes: list[str] = field(default_factory=list)
    full_changelog: str | None = None