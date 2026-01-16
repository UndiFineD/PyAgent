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
SelfImprovementCore: Pure logic for fleet self-improvement analysis.
Extracted from SelfImprovementOrchestrator for Rust-readiness.
"""

from __future__ import annotations
import re
import ast
from typing import Dict, List, Any, Optional

try:
    import rust_core as rc
    _RUST_ACCEL = True
except ImportError:
    rc = None  # type: ignore[assignment]
    _RUST_ACCEL = False


class SelfImprovementCore:
    """
    Pure logic core for identifying tech debt, security risks, and quality issues.
    This class contains no I/O and is suitable for Rust oxidation.
    """

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = workspace_root
        # Security patterns (Phase 84 / 104)
        self.dangerous_patterns = [
            (r"\beval\s*\(", "Use of eval() is highly insecure."),  # nosec
            (
                r"subprocess\.run\(.*shell=True",
                "shell=True in subprocess can lead to command injection.",
            ),  # nosec
            (r"os\.system\(", "os.system() is deprecated and insecure."),  # nosec
            (r"yaml\.load\(", "Unsafe YAML loading detected. Use yaml.safe_load()."),  # nosec
            (
                r"pickle\.load\(",
                "Pickle can execute arbitrary code. Use JSON if possible.",
            ),  # nosec
            (r"requests\.get\(.*verify=False", "SSL verification is disabled."),  # nosec
        ]

        # IO patterns for intelligence gap detection
        self.io_pattern = r"(requests\.(get|post|put|delete|patch|head)\(|self\.ai|subprocess\.(run|call|Popen|check_call|check_output)\(|adb shell)"

    def analyze_content(self, content: str, file_path_rel: str) -> List[Dict[str, Any]]:
        """
        Performs multi-dimensional analysis on file content.
        Returns a list of findings.
        """
        # Fast path: Use Rust for comprehensive analysis
        if _RUST_ACCEL and rc is not None:
            try:
                rust_findings = rc.analyze_code_quality_rust(
                    content, file_path_rel, self.dangerous_patterns
                )
                findings = []
                for issue_type, message, line_num in rust_findings:
                    finding = {
                        "type": issue_type,
                        "message": message,
                        "file": file_path_rel,
                    }
                    if line_num > 0:
                        finding["line"] = line_num
                    findings.append(finding)
                return findings
            except Exception:
                pass  # Fall through to Python path

        # Python fallback
        findings = []
        lines = content.split("\n")

        # 1. Security Analysis - use Rust if available
        if _RUST_ACCEL and rc is not None:
            try:
                rust_findings = rc.analyze_security_patterns_rust(
                    content, self.dangerous_patterns
                )
                for line_num, pattern, msg in rust_findings:
                    # Skip scanner's own rules
                    if "SelfImprovementCore" in content and pattern in str(
                        self.dangerous_patterns
                    ):
                        continue
                    findings.append(
                        {
                            "type": "Security Risk",
                            "message": f"{msg} (Pattern: {pattern})",
                            "file": file_path_rel,
                            "line": line_num,
                        }
                    )
            except Exception:
                pass  # Fall through to Python
        else:
            for pattern, msg in self.dangerous_patterns:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line):
                        if "# nosec" in line:
                            continue
                        # Avoid flagging the scanner rules themselves
                        if "SelfImprovementCore" in content and pattern in str(
                            self.dangerous_patterns
                        ):
                            continue

                        findings.append(
                            {
                                "type": "Security Risk",
                                "message": f"{msg} (Pattern: {pattern})",
                                "file": file_path_rel,
                                "line": i,
                            }
                        )

        # 2. Complexity Analysis (Phase 150 Enhancement)
        if _RUST_ACCEL and rc is not None:
            try:
                complexity = rc.calculate_cyclomatic_complexity(content)
                if complexity > 25:
                    findings.append(
                        {
                            "type": "Complexity Issue",
                            "message": f"Cyclomatic complexity is high ({complexity}). Consider breaking down functions.",
                            "file": file_path_rel,
                        }
                    )
            except Exception:
                pass

        # 3. Documentation Analysis
        if not re.search(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', content[:1000]):
            findings.append(
                {
                    "type": "Missing Docstring",
                    "message": "Module-level docstring is missing. Documentation is required for Phase 315 parity.",
                    "file": file_path_rel,
                }
            )

        # 4. Typing Analysis (Improved)
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
                        "message": f"Found {len(untyped_nodes)} functions without complete type hints (args or return). Strong typing required for Rust port.",
                        "file": file_path_rel,
                        "details": [n.name for n in untyped_nodes],
                    }
                )
        except Exception:
            # Fallback
            untyped_defs = [
                line
                for line in lines
                if (line.strip().startswith("def ") or "(self," in line or "(self)" in line)
                and (":" in line and "->" not in line)
                and not line.strip().startswith("#")
            ]
            if untyped_defs:
                findings.append(
                    {
                        "type": "Rust Readiness Task",
                        "message": f"Found {len(untyped_defs)} functions without complete type hints. Strong typing required for Rust port.",
                        "file": file_path_rel,
                    }
                )

        # 4. Robustness: Exception Handling
        if re.search(r"^\s*except:\s*(#.*)?$", content, re.MULTILINE):
            findings.append(
                {
                    "type": "Robustness Issue",
                    "message": "Bare 'except:' caught. Use 'except Exception:' or specific errors.",
                    "file": file_path_rel,
                }
            )

        # 5. Speed: time.sleep detection
        if (
            re.search(r"^[^\#]*time" + r"\.sleep\(", content, re.MULTILINE)
            and "test" not in file_path_rel.lower()
        ):
            if "SelfImprovementCore.py" not in file_path_rel:
                findings.append(
                    {
                        "type": "Performance Warning",
                        "message": "Found active time.sleep() in non-test code. Possible blocking bottleneck.",
                        "file": file_path_rel,
                    }
                )

        # 6. Intelligence Gap
        if re.search(self.io_pattern, content) and not any(
            x in content for x in ["_record", "record_lesson", "record_interaction"]
        ):
            findings.append(
                {
                    "type": "Intelligence Gap",
                    "message": "Component performs AI/IO or Shell operations without recording context to shards.",
                    "file": file_path_rel,
                }
            )

        return findings

    def generate_simple_fix(self, issue_type: str, content: str) -> Optional[str]:
        """
        Applies non-AI assisted simple fixes.
        """
        # Fast path: Use Rust for simple fixes
        if _RUST_ACCEL and rc is not None:
            try:
                result = rc.apply_simple_fixes_rust(content)
                if result:
                    fixed_content, _ = result
                    return fixed_content
                return None
            except Exception:
                pass  # Fall through to Python path

        # Python fallback
        new_content = content

        if issue_type == "Robustness Issue":
            return re.sub(
                r"^(\s*)except:(\s*)(#.*)?$",
                r"\1except Exception:\2\3",
                content,
                flags=re.MULTILINE,
            )

        # Simple fix for unsafe YAML
        unsafe_yaml = "yaml." + "load("  # nosec: pattern definition
        if unsafe_yaml in content and "yaml.safe_load(" not in content:
            if "import yaml" in content:
                return content.replace(unsafe_yaml, "yaml.safe_load(")

        return None
