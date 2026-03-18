#!/usr/bin/env python3
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
        for tool in list_tools():
            print(f"  {tool.name:20}  {tool.description}")
        return 0

    try:
        return run_tool(parsed.tool, parsed.args)
    except KeyError as e:
        print(e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
