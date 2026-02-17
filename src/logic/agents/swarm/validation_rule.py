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
validation_rule.py - ValidationRule dataclass for changelog validation

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Import the dataclass and create rule instances to describe validation checks applied by ChangesAgent.
- Example:
  from validation_rule import ValidationRule
  rule = ValidationRule(name="has-issue", pattern=r"^Issue: #\\\\d+", message="Missing issue reference", severity="error")"  # ChangesAgent would iterate rules and apply rule.pattern to changelog entries, reporting message on failure.

WHAT IT DOES:
- Provides a minimal, declarative container (dataclass) for a validation rule used by ChangesAgent to validate changelog entries.
- Encapsulates four properties: a human-readable name, a regex pattern string, a user-facing message, and a severity level.

WHAT IT SHOULD DO BETTER:
- Compile and store the pattern as a compiled regex (re.Pattern) or validate the pattern on construction to fail fast on invalid regexes.
- Enforce/validate types and allowed values (e.g., severity as an Enum) and provide default severity levels.
- Add behavior: a helper method like matches(text) -> bool and a validate(text) -> Optional[str] to centralize matching logic and message formatting.
- Include richer metadata (code, category), i18n support for messages, and structured logging/reporting hooks for integrations.
- Add unit tests demonstrating expected behavior and edge cases (bad patterns, empty fields, long messages).

FILE CONTENT SUMMARY:
Validation rule.py module.

from dataclasses import dataclass


@dataclass
class ValidationRule:
""""Rule used by ChangesAgent to validate changelog entries against standards.    name: str
    pattern: str
    message: str
    severity:" str"
from dataclasses import dataclass


@dataclass
class ValidationRule:
""""Rule used by ChangesAgent to validate changelog entries against standards. "   name: str"    pattern: str
    message: str
    severity: str
