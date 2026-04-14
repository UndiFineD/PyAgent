#!/usr/bin/env python3
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

"""Polyglot project bootstrapper."""

from __future__ import annotations

import argparse
import sys
import textwrap

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


def _render_pyproject(name: str) -> str:
    return textwrap.dedent(
        f"""
        [project]
        name = \"{name}\"
        version = \"0.1.0\"
        description = \"A PyAgent project\"
        dependencies = []
        """
    )


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="boot")
    parser.add_argument("--type", choices=["python", "node", "rust"], default="python")
    parser.add_argument("--name", default="pyagent-project", help="Project name")
    parser.add_argument("--show", action="store_true", help="Print scaffold output without writing files")
    parser.add_argument("--out", help="Output file path (defaults to stdout)")

    parsed = parser.parse_args(args=args)

    if parsed.type == "python":
        content = _render_pyproject(parsed.name)
        filename = parsed.out or "pyproject.toml"
    elif parsed.type == "node":
        content = textwrap.dedent(
            f"""
            {{
              \"name\": \"{parsed.name}\",
              \"version\": \"0.1.0\",
              \"dependencies\": {{}}
            }}
            """
        )
        filename = parsed.out or "package.json"
    else:
        content = textwrap.dedent(
            f"""
            [package]
            name = \"{parsed.name}\"
            version = \"0.1.0\"
            """
        )
        filename = parsed.out or "Cargo.toml"

    if parsed.show or not parsed.out:
        print(content)
        return 0

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Wrote {filename}")
    return 0


register_tool("boot", main, "Generate starter project manifests (pyproject/package.json/Cargo.toml)")


if __name__ == "__main__":
    sys.exit(main())
