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
Validator for report data integrity.
(Facade for src.core.base.common.validation_core)
"""

from src.core.base.common.validation_core import ValidationCore


class ReportValidator(ValidationCore):
    """Facade for ValidationCore specialized for reports."""

    def validate(self, content: str) -> dict:
        errors = self.validate_report({"summary": content, "agent_name": "unknown", "timestamp": 0})
        return {"valid": not errors, "errors": errors}

    def verify_hash(self, content: str, expected: str) -> bool:
        import hashlib

        actual = hashlib.sha256(content.encode()).hexdigest()[:16]
        return actual == expected
