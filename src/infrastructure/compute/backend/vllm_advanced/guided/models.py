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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Models for guided decoding.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional


class GuidedMode(Enum):
    """Mode of guided decoding."""

    NONE = auto()
    JSON = auto()
    JSON_OBJECT = auto()
    REGEX = auto()
    CHOICE = auto()
    GRAMMAR = auto()


@dataclass
class GuidedConfig:
    """Configuration for guided decoding."""

    mode: GuidedMode = GuidedMode.NONE

    # JSON mode
    json_schema: Optional[Dict[str, Any]] = None
    json_object: bool = False  # Simple JSON object mode

    # Regex mode
    regex_pattern: Optional[str] = None

    # Choice mode
    choices: Optional[List[str]] = None

    # Grammar mode (EBNF/CFG)
    grammar: Optional[str] = None

    # Advanced options
    whitespace_pattern: Optional[str] = None
    strict: bool = True  # Fail on constraint violations

    def _add_json_kwargs(self, kwargs: Dict[str, Any]) -> None:
        """Add JSON-related kwargs."""
        if self.mode == GuidedMode.JSON and self.json_schema:
            kwargs["guided_json"] = self.json_schema
        elif self.mode == GuidedMode.JSON_OBJECT:
            kwargs["guided_json"] = {}  # Empty schema = any valid JSON object

    def _add_regex_kwargs(self, kwargs: Dict[str, Any]) -> None:
        """Add regex-related kwargs."""
        if self.mode == GuidedMode.REGEX and self.regex_pattern:
            kwargs["guided_regex"] = self.regex_pattern

    def _add_choice_kwargs(self, kwargs: Dict[str, Any]) -> None:
        """Add choice-related kwargs."""
        if self.mode == GuidedMode.CHOICE and self.choices:
            kwargs["guided_choice"] = self.choices

    def _add_grammar_kwargs(self, kwargs: Dict[str, Any]) -> None:
        """Add grammar-related kwargs."""
        if self.mode == GuidedMode.GRAMMAR and self.grammar:
            kwargs["guided_grammar"] = self.grammar

    def _add_whitespace_kwargs(self, kwargs: Dict[str, Any]) -> None:
        """Add whitespace pattern kwargs."""
        if self.whitespace_pattern:
            kwargs["guided_whitespace_pattern"] = self.whitespace_pattern

    def to_sampling_params_kwargs(self) -> Dict[str, Any]:
        """Convert to kwargs for SamplingParams."""
        kwargs = {}

        self._add_json_kwargs(kwargs)
        self._add_regex_kwargs(kwargs)
        self._add_choice_kwargs(kwargs)
        self._add_grammar_kwargs(kwargs)
        self._add_whitespace_kwargs(kwargs)

        return kwargs


@dataclass
class RegexPattern:
    """
    Regex pattern builder for guided decoding.
    """

    pattern: str
    name: Optional[str] = None
    description: Optional[str] = None

    # Common patterns
    EMAIL = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    PHONE_US = r"\d{3}-\d{3}-\d{4}"
    URL = r"https?://[^\s]+"
    IPV4 = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    DATE_ISO = r"\d{4}-\d{2}-\d{2}"
    TIME_24H = r"[0-2][0-9]:[0-5][0-9]"
    HEX_COLOR = r"#[0-9A-Fa-f]{6}"
    UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

    # Programming patterns
    IDENTIFIER = r"[a-zA-Z_][a-zA-Z0-9_]*"
    PYTHON_VARIABLE = r"[a-z_][a-z0-9_]*"
    CLASS_NAME = r"[A-Z][a-zA-Z0-9]*"

    def __post_init__(self) -> None:
        # Validate regex
        try:
            re.compile(self.pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}") from e

    def to_guided_config(self) -> GuidedConfig:
        """Convert to GuidedConfig for use with decoder."""
        return GuidedConfig(
            mode=GuidedMode.REGEX,
            regex_pattern=self.pattern,
        )

    @classmethod
    def email(cls) -> "RegexPattern":
        """Pattern for common email addresses."""
        return cls(pattern=cls.EMAIL, name="email")

    @classmethod
    def phone_us(cls) -> "RegexPattern":
        """Pattern for US phone numbers."""
        return cls(pattern=cls.PHONE_US, name="phone_us")

    @classmethod
    def url(cls) -> "RegexPattern":
        """Pattern for absolute URLs."""
        return cls(pattern=cls.URL, name="url")

    @classmethod
    def date_iso(cls) -> "RegexPattern":
        """Pattern for ISO 8601 dates."""
        return cls(pattern=cls.DATE_ISO, name="date_iso")

    @classmethod
    def one_of(cls, *patterns: str) -> "RegexPattern":
        """Pattern matching any of the provided sub-patterns."""
        combined = "|".join(f"({p})" for p in patterns)
        return cls(pattern=combined, name="one_of")

    @classmethod
    def sequence(cls, *patterns: str, separator: str = "") -> "RegexPattern":
        """Pattern matching a sequence of sub-patterns with a separator."""
        combined = separator.join(patterns)
        return cls(pattern=combined, name="sequence")


@dataclass
class ChoiceConstraint:
    """
    Choice constraint for limiting output to specific options.
    """

    choices: List[str]
    case_sensitive: bool = True

    def __post_init__(self) -> None:
        if not self.choices:
            raise ValueError("At least one choice is required")

    def to_guided_config(self) -> GuidedConfig:
        """Convert to GuidedConfig for use with decoder."""
        return GuidedConfig(
            mode=GuidedMode.CHOICE,
            choices=self.choices,
        )

    @classmethod
    def yes_no(cls) -> "ChoiceConstraint":
        """Constraint for binary 'yes' or 'no' responses."""
        return cls(["yes", "no"])

    @classmethod
    def true_false(cls) -> "ChoiceConstraint":
        """Constraint for boolean 'true' or 'false' responses."""
        return cls(["true", "false"])

    @classmethod
    def sentiment(cls) -> "ChoiceConstraint":
        """Constraint for common sentiment categories."""
        return cls(["positive", "negative", "neutral"])

    @classmethod
    def rating(cls, min_val: int = 1, max_val: int = 5) -> "ChoiceConstraint":
        """Constraint for integer ratings in the specified range."""
        return cls([str(i) for i in range(min_val, max_val + 1)])
