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

"""SSH/FTP helper utilities."""

from __future__ import annotations

import argparse
import subprocess
import sys

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="remote")
    parser.add_argument("--run", help="Command to run locally (shell)")
    parser.add_argument("--host", help="Remote host (placeholder, no ssh support yet)")

    parsed = parser.parse_args(args=args)

    if parsed.run:
        proc = subprocess.run(parsed.run, shell=True)
        return proc.returncode

    parser.print_help()
    return 1


register_tool("remote", main, "Local command runner (placeholder for SSH/FTP helpers)")


if __name__ == "__main__":
    sys.exit(main())
