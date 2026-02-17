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


Enums for structured output engine.

from enum import Enum, auto


class GrammarType(Enum):
    """Types of grammar specifications.
    JSON_SCHEMA = auto()
    JSON_OBJECT = auto()
    REGEX = auto()
    EBNF = auto()
    LARK = auto()
    STRUCTURAL_TAG = auto()
    CUSTOM = auto()


class VocabType(Enum):
    """Vocabulary encoding types.
    RAW = auto()
    BYTE_FALLBACK = auto()
    BYTE_LEVEL = auto()
