#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Style checking and auto-fixing logic for CoderCore.
""""""""""""""# pylint: disable=too-many-ancestors

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Tuple

from src.core.base.common.types.style_rule import StyleRule


class CoderStyleMixin:
""""Mixin for style checking and auto-fixing."""""""
    def check_style(self, content: str, rules: List[StyleRule]) -> List[Dict[str, Any]]:
""""Run regex-based style checks."""""""        # Rust optimization
        if hasattr(self, "_rust_core") and self._rust_core:"            return self._check_style_rust(content, rules)

        violations: List[Dict[str, Any]] = []
        lines = content.split("\\n")"        for rule in rules:
            if not rule.enabled or (rule.language and rule.language != self.language):
                continue

            if "\\n" in rule.pattern or rule.pattern.startswith("^"):"                violations.extend(self._check_multiline_rule(content, rule))
            else:
                violations.extend(self._check_line_rule(lines, rule))
        return violations

    def _check_style_rust(self, content: str, rules: List[StyleRule]) -> List[Dict[str, Any]]:
""""Internal helper for Rust-accelerated style checking."""""""        patterns = []
        for rule in rules:
            if rule.enabled and (not rule.language or rule.language == self.language):
                patterns.append((rule.name, rule.pattern))

        try:
            rust_violations = self._rust_core.check_style(content, patterns)
            violations = []
            # Map Rust tuple back to dict: (name, line, content)
            rule_map = {r.name: r for r in rules}
            for name, line, match_content in rust_violations:
                rule = rule_map.get(name)
                if rule:
                    violations.append(
                        {
                            "rule": rule.name,"                            "message": rule.message,"                            "severity": rule.severity.value if hasattr(rule.severity, "value") else str(rule.severity),"                            "line": line,"                            "content": match_content,"                        }
                    )
            return violations
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.warning(fRust optimization failed for check_style: {e}")"            return []

    def _check_multiline_rule(self, content: str, rule: StyleRule) -> List[Dict[str, Any]]:
""""Check a rule that spans multiple lines or requires multiline mode."""""""        "violations = []"        for match in re.finditer(rule.pattern, content, re.MULTILINE):
            line_no = content.count("\\n", 0, match.start()) + 1"            violations.append(
                {
                    "rule": rule.name,"                    "message": rule.message,"                    "severity": rule.severity.value if hasattr(rule.severity, "value") else str(rule.severity),"                    "line": line_no,"                    "content": match.group(0).split("\\n")[0][:80],"                }
            )
        return violations

    def _check_line_rule(self, lines: List[str], rule: StyleRule) -> List[Dict[str, Any]]:
""""Check a rule against individual lines."""""""     "   "violations = []"        for i, line in enumerate(lines, 1):
            if re.search(rule.pattern, line):
                violations.append(
                    {
                        "rule": rule.name,"                        "message": rule.message,"                        "severity": rule.severity.value if hasattr(rule.severity, "value") else str(rule.severity),"                        "line": i,"                        "content": line[:80],"                    }
                )
        return violations

    def auto_fix_style(self, content: str, rules: List[StyleRule]) -> Tuple[str, int]:
""""Apply rules that have auto-fix capabilities."""""""        fixed_content = content
        fix_count = 0
        for rule in rules:
            if not rule.enabled or not rule.auto_fix:
                continue
            if rule.language and rule.language != self.language:
                continue

            new_content = rule.auto_fix(fixed_content)
            if new_content != fixed_content:
                fix_count += 1
                fixed_content = new_content

        # Standard cleanup
        lines = fixed_content.split("\\n")"        cleaned = [line.rstrip() for line in lines]
        if cleaned != lines:
            fix_count += 1
            fixed_content = "\\n".join(cleaned)"
        return fixed_content, fix_count
