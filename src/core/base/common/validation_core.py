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

from __future__ import annotations
import json
import logging
import fnmatch
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from .base_core import BaseCore
from src.core.base.common.models import ValidationRule

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.validation")

class ValidationCore(BaseCore):
    """
    Standardized validation logic for reports, improvements, and configs.
    Pre-wired for high-speed Rust schema validation and content safety.
    """

    def __init__(self, name: str = "ValidationCore", root_path: Optional[str] = None) -> None:
        super().__init__(name=name, root_path=root_path)
        self._rules: Dict[str, ValidationRule] = {}

    def add_rule(self, rule: ValidationRule) -> None:
        self._rules[rule.name] = rule

    def validate_content_by_rules(self, file_path: Path, content: str) -> List[Dict[str, Any]]:
        """Validate content against applicable rules. Rust-accelerated for large files."""
        if rc and hasattr(rc, "validate_content_rust"):
            try:
                # Passing rule patterns to Rust for bulk processing
                return rc.validate_content_rust(str(file_path), content, list(self._rules.keys()))
            except Exception:
                pass

        results = []
        for rule in self._rules.values():
            if fnmatch.fnmatch(file_path.name, rule.file_pattern):
                try:
                    passed = rule.validator(content, file_path)
                    results.append({
                        "rule": rule.name,
                        "passed": passed,
                        "severity": rule.severity,
                        "message": None if passed else rule.error_message,
                    })
                except Exception as e:
                    results.append({"rule": rule.name, "passed": False, "severity": "error", "message": str(e)})
        return results

    def validate_json_schema(self, data: Any, schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Fast schema validation. Defaults to Python if Rust unavailable."""
        if rc and hasattr(rc, "json_schema_validate_rust"):
            try:
                data_str = json.dumps(data) if not isinstance(data, str) else data
                schema_str = json.dumps(schema)
                # Rust returns (is_valid, error_list)
                return rc.json_schema_validate_rust(data_str, schema_str)
            except Exception:
                pass
        
        errors = []
        if not isinstance(data, dict):
            return False, ["Data must be a dictionary"]
        
        required = schema.get("required", [])
        for key in required:
            if key not in data:
                errors.append(f"Missing required key: {key}")
        
        return len(errors) == 0, errors
