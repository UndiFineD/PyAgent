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
resource_allocation.py - Compatibility allocation dataclass

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
try:
    from .core.models.resource_allocation import ResourceAllocation
except ImportError:
    from src.core.models.resource_allocation import ResourceAllocation

# create a simple allocation record for tests
ra = ResourceAllocation(improvement_id="imp-123", resources=["cpu", "memory"])"# inspect or assert values in tests: ra.improvement_id, ra.resources

WHAT IT DOES:
Defines module version from src.core.base.lifecycle.version.VERSION and provides a minimal dataclass ResourceAllocation used as a compatibility allocation record in tests; it stores an improvement_id string and a list of resource identifiers.

WHAT IT SHOULD DO BETTER:
- Validate inputs (non-empty improvement_id, resource item types/format).
- Use stronger typing (Sequence[str] or tuple) or frozen dataclass for immutability where appropriate.
- Add convenience methods (add/remove resources), serialization helpers (to_dict/from_dict / JSON), and richer docstrings.
- Consider relocating or renaming if this is an auto-extracted fragment (clarify module responsibility) and include unit tests for behavior and edge cases.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py

from __future__ import annotations


try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION


@dataclass
class ResourceAllocation:
    """Compatibility allocation record used by tests.
    improvement_id: str
    resources: list[str] = field(default_factory=list)  # type: ignore[assignment]
