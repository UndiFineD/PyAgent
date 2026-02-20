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
Types.py module.
"""
try:

"""
from typing import TypeAlias, TypeVar, Any
except ImportError:
    from typing import TypeAlias, TypeVar, Any


_T = TypeVar("_T")
_U = TypeVar("_U")

# Type alias for nested JSON structures where leaves can be any type
JSONTree: TypeAlias = dict[str, "JSONTree[_T]"] | list["JSONTree[_T]"] | tuple["JSONTree[_T]", ...] | _T

# Extended type alias for overload compatibility
_JSONTree: TypeAlias = (
    dict[str, "JSONTree[_T]"]
    | list["JSONTree[_T]"]
    | tuple["JSONTree[_T]", ...]
    | dict[str, _T]
    | list[_T]
    | tuple[_T, ...]
    | _T
)
