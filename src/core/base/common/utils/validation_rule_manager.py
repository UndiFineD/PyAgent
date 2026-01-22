<<<<<<< HEAD
<<<<<<< HEAD
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors

"""
Manager for validation rules.
(Facade for src.core.base.common.validation_core)
"""

from __future__ import annotations
from typing import Any
from pathlib import Path
from src.core.base.common.validation_core import ValidationCore
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
        **kwargs
    ) -> None:
        """Add a validation rule. Supports both legacy signature and ValidationRule object."""
        if hasattr(name_or_rule, "name"):
            # It's a ValidationRule object
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
            **kwargs
        }
        self._rules[name_or_rule] = rule_obj
        self._core.register_rule(name_or_rule, rule_obj)

    def validate(self, file_path: Path | str, content: str) -> list[dict[str, Any]]:
        """Validate content against rules. Legacy support."""
        if not isinstance(file_path, Path):
            file_path = Path(file_path)
        return self._core.validate_content_by_rules(file_path, content)
=======
"""
Manager for validation rules.
(Facade for src.core.base.common.validation_core)
"""

from src.core.base.common.validation_core import ValidationCore as ValidationRuleManager
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
"""
Manager for validation rules.
(Facade for src.core.base.common.validation_core)
"""

from src.core.base.common.validation_core import ValidationCore as ValidationRuleManager
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
