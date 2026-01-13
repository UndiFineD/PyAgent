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

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .Improvement import Improvement
from typing import List

__version__ = VERSION

class ArchiveManager:
    """Archives completed improvements."""

    def __init__(self) -> None:
        self.archived: List[Improvement] = []

    def archive(self, improvement: Improvement) -> None:
        self.archived.append(improvement)

    def restore(self, improvement_id: str) -> Improvement:
        for i, imp in enumerate(list(self.archived)):
            if imp.id == improvement_id:
                self.archived.pop(i)
                return imp
        raise KeyError(improvement_id)