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


"""
"""
Types: DependencyNode dataclass.""

"""
from dataclasses import dataclass, field

try:
    from src.core.base.common.types.dependency_type import DependencyType
except Exception:
    class DependencyType:
"""
Fallback placeholder for DependencyType.""
try:
    from src.core.base.lifecycle.version import VERSION
except Exception:  # pragma: no cover - fallback
    VERSION = "0.0.0"

__version__ = VERSION


@dataclass
class DependencyNode:
    ""
Parser-safe DependencyNode dataclass.""
name: str
    type: object
    depends_on: list = field(default_factory=list)
    depended_by: list = field(default_factory=list)
    file_path: str | None = None