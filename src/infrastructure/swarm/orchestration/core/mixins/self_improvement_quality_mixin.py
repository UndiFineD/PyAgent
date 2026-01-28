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
Quality and robustness analysis logic for SelfImprovementCore.
"""

from __future__ import annotations

import ast
import re
from typing import Any, Dict, List


class SelfImprovementQualityMixin:
    """Mixin for quality, complexity, and robustness analysis."""

    def _analyze_complexity(self, content: str, file_path_rel: str) -> List[Dict[str, Any]]:
        """Checks for high cyclomatic complexity."""
        _RUST_ACCEL = getattr(self, "_RUST_ACCEL", False)
        rc = getattr(self, "rc", None)

        if _RUST_ACCEL and rc is not None:
            try:
                complexity = rc.calculate_cyclomatic_complexity(content)
                if complexity > 25:
                    return [
                        {
                            "type": "Complexity Issue",
                            "message": (
                                f"Cyclomatic complexity is high ({complexity}). "
                                "Consider breaking down functions."
                            ),
                            "file": file_path_rel,
                        }
                    ]
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                pass
        return []

    def _analyze_documentation(self, content: str, file_path_rel: str) -> List[Dict[str, Any]]:
        """Checks for missing or insufficient docstrings."""
        findings = []
        if not re.search(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', content[:1000]):
            findings.append(
                {
                    "type": "Missing Docstring",
                    "message": "Module-level docstring is missing. Documentation is required for Phase 315 parity.",
                    "file": file_path_rel,
                }
            )
        return findings

    def _analyze_typing(self, content: str, file_path_rel: str) -> List[Dict[str, Any]]:
        """Checks for missing type hints to ensure Rust FFI readiness."""
        findings = []
        try:
            tree = ast.parse(content)
            untyped_nodes = [
                n
                for n in ast.walk(tree)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                and (n.returns is None or any(arg.annotation is None for arg in n.args.args if arg.arg != "self"))
            ]
            if untyped_nodes:
                findings.append(
                    {
                        "type": "Rust Readiness Task",
                        "message": (
                            f"Found {len(untyped_nodes)} functions without complete type hints. "
                            "Strong typing required for Rust port."
                        ),
                        "file": file_path_rel,
                        "details": [n.name for n in untyped_nodes],
                    }
                )
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            # Simple line-based fallback for broken syntax
            untyped_count = content.count("def ") - content.count("->")
            if untyped_count > 0:
                findings.append(
                    {
                        "type": "Rust Readiness Task",
                        "message": f"Heuristically detected {untyped_count} functions missing type hints.",
                        "file": file_path_rel,
                    }
                )
        return findings

    def _analyze_robustness_and_perf(self, content: str, file_path_rel: str, allow_triton_check: bool = True) -> List[Dict[str, Any]]:
        """General quality and performance checks."""
        findings = []
        # Robustness: Bare except
        if re.search(r"^\s*except Exception as e:  # pylint: disable=broad-exception-caught\s*(#.*)?$", content, re.MULTILINE):
            findings.append(
                {
                    "type": "Robustness Issue",
                    "message": "Bare 'except Exception as e:  # pylint: disable=broad-exception-caught' or specific errors.",
                    "file": file_path_rel,
                }
            )

        # Performance: time.sleep in non-test code
        if re.search(r"^[^\#]*time" + r"\.sleep\(", content, re.MULTILINE) and "test" not in file_path_rel.lower():
            if "SelfImprovementCore.py" not in file_path_rel:
                findings.append(
                    {
                        "type": "Performance Warning",
                        "message": "Found active time.sleep() in non-test code. Possible blocking bottleneck.",
                        "file": file_path_rel,
                    }
                )

        # Intelligence Gap
        io_pattern = getattr(self, "io_pattern", "")
        if (
            io_pattern
            and re.search(io_pattern, content)
            and not any(x in content for x in ["_record", "record_lesson", "record_interaction"])
        ):
            findings.append(
                {
                    "type": "Intelligence Gap",
                    "message": "Component performs AI/IO or Shell operations without recording context to shards.",
                    "file": file_path_rel,
                }
            )

        # Triton compatibility warning (placeholder for actual check location)
        if not allow_triton_check:
            # If Triton check is not allowed, skip any Triton-related warnings/checks here
            pass
        return findings
