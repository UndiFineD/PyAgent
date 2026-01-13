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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .ValidationSeverity import ValidationSeverity
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

__version__ = VERSION

@dataclass
class ValidationResult:
    """Result from improvement validation.

    Attributes:
        improvement_id: ID of the validated improvement.
        is_valid: Whether the improvement passed validation.
        issues: List of validation issues.
        test_results: Results from automated tests.
    """
    improvement_id: str
    is_valid: bool = True
    issues: List[Tuple[ValidationSeverity, str]] = field(
        default_factory=lambda: []
    )
    test_results: Dict[str, bool] = field(
        default_factory=lambda: {}  # type: ignore[assignment]
    )

    @property
    def errors(self) -> List[str]:
        """Compatibility accessor used by tests."""
        return [msg for sev, msg in self.issues if sev == ValidationSeverity.ERROR]