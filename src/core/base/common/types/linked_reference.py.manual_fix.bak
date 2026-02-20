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


"""
"""
Types: LinkedReference dataclass.""

"""
from dataclasses import dataclass

try:
    from src.core.base.lifecycle.version import VERSION
except Exception:  # pragma: no cover - fallback
    VERSION = "0.0.0"

__version__ = VERSION


@dataclass
class LinkedReference:
"""
A linked reference to commit or issue.


    Attributes:
        ref_type: Type of reference ('commit' or 'issue').
        ref_id: ID of the reference.
        url: URL to the reference.
        title: Title / description of the reference.
    ""
ref_type: str
    ref_id: str
    url: str | None = None
    title: str | None = None