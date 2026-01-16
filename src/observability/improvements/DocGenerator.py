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
from src.core.base.Version import VERSION
from .Improvement import Improvement
from typing import Any, cast

__version__ = VERSION


class DocGenerator:
    """Generates simple documentation text for improvements."""

    def __init__(self) -> None:
        self.templates: dict[str, str] = {
            "default": "## {title}\n\n{description}\n",
        }

    def generate(self, improvement: Improvement, include_metadata: bool = False) -> str:
        base = self.templates["default"].format(
            title=improvement.title, description=improvement.description
        )
        if include_metadata:
            meta = getattr(improvement, "metadata", None)
            if isinstance(meta, dict) and meta:
                base += "\n## Metadata\n"
                meta_dict = cast(dict[str, Any], meta)
                for k, v in meta_dict.items():
                    base += f"- {k}: {v}\n"
        return base
