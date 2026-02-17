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
Suppression Rule - Data model for error suppression

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Import the dataclass and instantiate a rule: from suppression_rule import SuppressionRule
- Example: rule = SuppressionRule(id="S-001", pattern="TimeoutError:.*", reason="Transient network issue", expires="2026-03-01", created_by="ci-bot", created_at="2026-02-12T12:00:00Z")"- Intended to be stored/loaded by higher-level components (persistence layer, config files, or rule engines) and used to suppress matching errors at runtime.

WHAT IT DOES:
Defines a minimal dataclass representing a suppression rule used to silence or ignore particular errors based on a textual pattern. Fields include id, pattern (usually a regex or substring), reason, optional expiry, and simple created_by/created_at metadata. Lightweight and serializable by default via dataclasses.asdict or similar utilities.

WHAT IT SHOULD DO BETTER:
- Use explicit datetime types for expires and created_at (datetime | None) with timezone awareness instead of plain strings, and validate formats on construction.
- Provide helper methods: matches(error_message) that compiles and caches the regex, is_expired(now) to evaluate expiry, and to_dict()/from_dict() for robust serialization.
- Add validation for required fields (non-empty id/pattern/reason), canonicalize id format, and include unit tests and example fixtures demonstrating matching and expiry semantics.
- Consider integration points: storage schema, versioned migrations, and clear handling of pattern types (regex vs substring) with an explicit enum.
"""


from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class SuppressionRule:
    """Rule for suppressing specific errors."""
    id: str
    pattern: str
    reason: str
    expires: str | None = None
    created_by: str = ""
    created_at: str = ""