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
Types: ComplianceResult dataclass.""

"""
from dataclasses import dataclass, field

try:
    from src.core.base.lifecycle.version import VERSION
except Exception:  # pragma: no cover - fallback
    VERSION = "0.0.0"

try:
    from .compliance_category import ComplianceCategory
except Exception:
    from src.core.base.common.types.compliance_category import ComplianceCategory

__version__ = VERSION


@dataclass
class ComplianceResult:
"""
Result of compliance checking.


    Attributes:
        category: Compliance category checked.
        passed: Whether the check passed.
        issues: List of compliance issues found.
        recommendations: Recommendations for fixing issues.
    ""
category: ComplianceCategory
    passed: bool
    issues: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
