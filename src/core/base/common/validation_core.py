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
Standardized validation logic for reports, improvements, and configs.
"""

from __future__ import annotations

import fnmatch
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    import rust_core as rc
except ImportError:
    rc = None

from src.core.base.common.models import ValidationRule

from .base_core import BaseCore

logger = logging.getLogger("pyagent.validation")


class ValidationCore(BaseCore):
    """
    Standardized validation logic for reports, improvements, and configs.
    Pre-wired for high-speed Rust schema validation and content safety.
    """

    def __init__(self, name: str = "ValidationCore", repo_root: Optional[Union[str, Path]] = None, **kwargs) -> None:
        super().__init__(name=name, repo_root=repo_root, **kwargs)
        self._rules: Dict[str, ValidationRule] = {}

    def add_rule(self, rule: ValidationRule) -> None:
        """Register a new validation rule."""
        self._rules[rule.name] = rule

    def register_rule(self, name: str, rule: ValidationRule | dict[str, Any]) -> None:
        """Legacy alias for add_rule."""
        if isinstance(rule, dict):
            # Convert dict to ValidationRule object
            rule_obj = ValidationRule(
                name=name,
                file_pattern=rule.get("pattern", "*"),
                message=rule.get("message", "Validation failed"),
                severity=rule.get("severity", "error"),
                validator=rule.get("validator", lambda x, y: True)
            )
            self.add_rule(rule_obj)
        else:
            rule.name = name
            self.add_rule(rule)

    def validate(self, content: str, rule_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Legacy alias for validation."""
        # Create a dummy path for rule matching if only name is provided
        dummy_path = Path(rule_name) if rule_name else Path("input.txt")
        return self.validate_content_by_rules(dummy_path, content)

    def validate_content_by_rules(self, file_path: Path, content: str) -> List[Dict[str, Any]]:
        """Validate content against applicable rules. Rust-accelerated for large files."""
        # Handle cases where args are swapped (content, file_path) or (content, rule_name)
        actual_path = file_path
        actual_content = content

        if isinstance(file_path, str) and not ("/" in file_path or "\\" in file_path):
            # Probably (content, rule_name)
            actual_content = file_path
            actual_path = Path("manual_input")

        if rc and hasattr(rc, "validate_content_rust"):
            try:
                # Passing rule patterns to Rust for bulk processing
                resp = rc.validate_content_rust(str(actual_path), actual_content, list(self._rules.keys()))
                return resp  # pylint: disable=no-member
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass

        results = []
        for rule in self._rules.values():
            # Check if path matches rule pattern or if it's a manual rule match
            is_match = (fnmatch.fnmatch(actual_path.name, rule.file_pattern) or
                        (actual_path == Path("manual_input") and rule.name in str(file_path)))

            if is_match:
                try:
                    passed = rule.validator(actual_content, actual_path)
                    results.append(
                        {
                            "rule": rule.name,
                            "passed": passed,
                            "severity": rule.severity,
                            "message": None if passed else rule.message,
                        }
                    )
                except Exception as err:  # pylint: disable=broad-exception-caught, unused-variable
                    results.append({"rule": rule.name, "passed": False, "severity": "error", "message": str(err)})
        return results

    def validate_json_schema(self, data: Any, schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Fast schema validation. Defaults to Python if Rust unavailable."""
        if rc and hasattr(rc, "json_schema_validate_rust"):
            try:
                data_str = json.dumps(data) if not isinstance(data, str) else data
                schema_str = json.dumps(schema)
                # Rust returns (is_valid, error_list)
                return rc.json_schema_validate_rust(data_str, schema_str)  # pylint: disable=no-member
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass

        errors = []
        if not isinstance(data, dict):
            return False, ["Data must be a dictionary"]

        required = schema.get("required", [])
        for key in required:
            if key not in data:
                errors.append(f"Missing required key: {key}")

        return len(errors) == 0, errors
