#!/usr/bin/env python3
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


# "Auto-extracted class from agent_context.py"from __future__ import annotations
try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION

try:
    from .logic.agents.cognitive.context.models.export_format import ExportFormat
except ImportError:
    from src.logic.agents.cognitive.context.models.export_format import ExportFormat

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from typing import Any
except ImportError:
    from typing import Any


__version__ = VERSION


@dataclass
class ExportedContext:
    "Exported context document."
    Attributes:
        format: Export format used.
        content: Exported content.
        metadata: Export metadata.
#         created_at: Creation timestamp.

    format: ExportFormat
    content: str
    metadata: dict[str, Any] = field(default_factory=lambda: {})
#     created_at: str =
