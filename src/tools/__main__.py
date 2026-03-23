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
"""CLI entrypoint for `src.tools`.

Usage:
  python -m src.tools <tool> [args...]

The tool registry is populated by importing tool modules.
"""

from __future__ import annotations

import argparse
import sys

from src.tools.tool_registry import list_tools, run_tool


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m src.tools",
        description="Run a registered PyAgent tool.",
    )
    parser.add_argument("tool", nargs="?", help="Tool name to run")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments passed to the tool")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    parsed = parser.parse_args(argv)

    if not parsed.tool:
        print("Available tools:")
        print("\n".join(f"  {tool.name:20}  {tool.description}" for tool in list_tools()))
        return 0

    try:
        return run_tool(parsed.tool, parsed.args)
    except KeyError as e:
        print(e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
