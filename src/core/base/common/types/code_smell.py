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

"""Types: CodeSmell dataclass used by analysis tools and tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class CodeSmell:
    """Simple, parser-safe representation of a code smell."""

    name: str
    description: str
    severity: str
    line_number: Optional[int] = None
    suggestion: Optional[str] = None
    category: str = "general"


__all__ = ["CodeSmell"]