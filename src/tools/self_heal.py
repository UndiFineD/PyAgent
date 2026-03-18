#!/usr/bin/env python3
"""Self‑healing helper utilities."""
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

import argparse
import ast
import os
import sys

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


def _check_py_syntax(root: str) -> dict[str, str]:
    issues: dict[str, str] = {}
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(".py"):
                path = os.path.join(dirpath, fn)
                try:
                    with open(path, encoding="utf-8") as f:
                        ast.parse(f.read(), filename=path)
                except Exception as e:
                    issues[path] = str(e)
    return issues


def detect_misconfig(root: str = ".") -> dict[str, str]:
    """Detect common misconfigurations in the project."""
    return _check_py_syntax(root)


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="self_heal")
    parser.add_argument(
        "--root", default=".", help="Root directory to scan for issues (defaults to current directory)"
    )

    parsed = parser.parse_args(args=args)

    issues = _check_py_syntax(parsed.root)
    if not issues:
        print("No syntax issues detected.")
        return 0

    print("Syntax issues detected:")
    for path, err in issues.items():
        print(f" - {path}: {err}")
    return 1


register_tool("self_heal", main, "Basic self-healing checks (syntax scan)")


if __name__ == "__main__":
    sys.exit(main())
