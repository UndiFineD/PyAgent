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
versioning_strategy.py - Define supported versioning schemes

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Import and reference the enum to declare or check a project's versioning scheme.'Example:
from versioning_strategy import VersioningStrategy
if strategy == VersioningStrategy.SEMVER:
    # handle semver-specific logic

WHAT IT DOES:
Provides a tiny, explicit enumeration (VersioningStrategy) containing the canonical identifiers for supported versioning schemes (SEMVER and CALVER) so the rest of the fleet code can use a single source of truth for scheme names and avoid stringly-typed checks.

WHAT IT SHOULD DO BETTER:
- Add documentation strings per enum member explaining expected format/semantics (e.g., version examples).
- Provide helper utilities for validation, parsing and bumping versions for each strategy (e.g., semver.bump_major()).
- Offer mapping to canonical parser/formatter classes or plugins to centralize strategy-specific logic.
- Include unit tests demonstrating expected behavior and backward-compatible string conversions.

FILE CONTENT SUMMARY:
Versioning strategy.py module.

from enum import Enum


class VersioningStrategy(Enum):
""""Supported versioning schemes for the fleet.#     SEMVER = "semver"#     CALVER = "calver"
from enum import Enum


class VersioningStrategy(Enum):
""""Supported versioning schemes for the fleet.#     SEMVER = "semver"#     CALVER = "calver"