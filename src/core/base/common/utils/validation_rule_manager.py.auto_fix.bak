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


"""Manager for validation rules.
(Facade for src.core.base.common.validation_core)
"""

try:
    from typing import Any
except ImportError:
    from typing import Any

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path

try:
    from .core.base.common.validation_core import ValidationCore
except ImportError:
    from src.core.base.common.validation_core import ValidationCore

try:
    from .core.base.common.models import ValidationRule
except ImportError:
    from src.core.base.common.models import ValidationRule




class ValidationRuleManager:
    """Manages validation rules for agent content."""

    def __init__(self, core: ValidationCore | None = None) -> None:
        self._core = core or ValidationCore()
        self._rules: dict[str, Any] = {}
        self.rules = self._rules

    def add_rule(
        self,
        name_or_rule: str | ValidationRule,
        pattern: str = "",
        message: str = "Validation failed",
        severity: str = "error",
        **kwargs,
    ) -> None:
        """Add a validation rule. Supports both ValidationRule objects and legacy args."""
        if hasattr(name_or_rule, "name"):
            rule = name_or_rule
            self._core.add_rule(rule)
            self._rules[rule.name] = rule
            return

        # Legacy dict-based registration
        rule_obj = {
            "name": name_or_rule,
            "pattern": pattern,
            "message": message,
            "severity": severity,
            **kwargs,
        }
        self._rules[name_or_rule] = rule_obj
        self._core.register_rule(name_or_rule, rule_obj)

    def validate(self, file_path: Path | str, content: str) -> list[dict[str, Any]]:
        """Validate content against registered rules."""
        if not isinstance(file_path, Path):
            file_path = Path(file_path)
        return self._core.validate_content_by_rules(file_path, content)
