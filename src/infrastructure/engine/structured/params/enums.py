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

"""
Enums.py module.
"""

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
from enum import Enum, auto


class StructuredOutputType(Enum):
    """Type of structured output constraint."""

    JSON_SCHEMA = auto()  # JSON Schema constraint
    REGEX = auto()  # Regex pattern
    CHOICE = auto()  # Fixed choices
    GRAMMAR = auto()  # EBNF/Lark grammar
    TYPE = auto()  # Type annotation
    COMPOSITE = auto()  # Combined constraints


class ConstraintType(Enum):
    """Internal constraint type."""

    INCLUDE = auto()  # Must match
    EXCLUDE = auto()  # Must not match
    PREFIX = auto()  # Prefix constraint
    SUFFIX = auto()  # Suffix constraint


class SchemaFormat(Enum):
    """JSON Schema format."""

    DRAFT_07 = "draft-07"
    DRAFT_2020_12 = "draft-2020-12"
    OPENAPI_3_0 = "openapi-3.0"
    OPENAPI_3_1 = "openapi-3.1"


class GuidedDecodingBackend(Enum):
    """Guided decoding backend."""

    AUTO = auto()  # Auto-select best backend
    OUTLINES = auto()  # Outlines library
    LMFE = auto()  # lm-format-enforcer
    XGRAMMAR = auto()  # xgrammar
    PYAGENT = auto()  # Native PyAgent engine


class WhitespacePattern(Enum):
    """Whitespace handling in structured output."""

    PRESERVE = auto()  # Preserve as-is
    MINIMAL = auto()  # Minimal whitespace
    COMPACT = auto()  # No whitespace
    PRETTY = auto()  # Pretty-printed (2-space indent)
    CUSTOM = auto()  # Custom pattern
