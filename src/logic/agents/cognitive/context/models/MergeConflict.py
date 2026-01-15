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

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from src.logic.agents.cognitive.context.utils.ConflictResolution import ConflictResolution
from dataclasses import dataclass

__version__ = VERSION




@dataclass
class MergeConflict:
    """Merge conflict information.

    Attributes:
        section: Section with conflict.
        ours: Our version of content.
        theirs: Their version of content.
        resolution: Applied resolution.
    """
    section: str
    ours: str
    theirs: str
    resolution: ConflictResolution | None = None
