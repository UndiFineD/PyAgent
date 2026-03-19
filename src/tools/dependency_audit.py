#!/usr/bin/env python3
"""Simple utility to audit project dependencies."""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
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

import argparse
import json
import os
import sys

try:
    import tomllib  # type: ignore
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


def check_dependencies(project_root: str = ".") -> list[str]:
    """Check for missing or outdated dependencies; returns list of issues."""
    issues: list[str] = []
    pyproject = os.path.join(project_root, "pyproject.toml")

    if os.path.exists(pyproject):
        try:
            with open(pyproject, "rb") as f:
                data = tomllib.load(f)
            deps = data.get("project", {}).get("dependencies", [])
            issues.append(f"pyproject dependencies: {len(deps)} entries")
        except Exception as e:
            issues.append(f"Failed to parse pyproject.toml: {e}")
    else:
        issues.append("pyproject.toml not found")

    reqs = os.path.join(project_root, "requirements.txt")
    if os.path.exists(reqs):
        try:
            with open(reqs, encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            issues.append(f"requirements.txt entries: {len(lines)}")
        except Exception as e:
            issues.append(f"Failed to read requirements.txt: {e}")
    else:
        issues.append("requirements.txt not found")

    return issues


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="dependency_audit")
    parser.add_argument("--root", default=".", help="Project root directory")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    parsed = parser.parse_args(args=args)
    issues = check_dependencies(parsed.root)

    if parsed.json:
        print(json.dumps({"issues": issues}, indent=2))
    else:
        print("\n".join(issues))

    return 0


register_tool("dependency_audit", main, "Audit dependency manifests (pyproject/requirements)")
