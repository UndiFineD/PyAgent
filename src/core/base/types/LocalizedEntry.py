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
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .LocalizationLanguage import LocalizationLanguage
from dataclasses import dataclass, field

__version__ = VERSION







@dataclass
class LocalizedEntry:
    """A changelog entry with localization support.

    Attributes:
        original_text: Original entry text.
        language: Source language of the entry.
        translations: Dictionary of translations by language code.
        auto_translated: Whether translations were auto - generated.
    """
    original_text: str
    language: LocalizationLanguage = LocalizationLanguage.ENGLISH
    translations: dict[str, str] = field(default_factory=lambda: {})
    auto_translated: bool = False
