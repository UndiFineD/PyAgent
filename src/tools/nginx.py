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

"""NGINX configuration helpers."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


def main(args: list[str] | None = None) -> int:
    """Main entry point for the nginx tool."""
    parser = argparse.ArgumentParser(prog="nginx")
    parser.add_argument("--config", help="Path to nginx.conf")
    parser.add_argument("--test", action="store_true", help="Run nginx -t to validate configuration")

    parsed = parser.parse_args(args=args)

    if parsed.test:
        nginx = shutil.which("nginx")
        if not nginx:
            print("nginx binary not found on PATH", file=sys.stderr)
            return 1

        cmd = [nginx, "-t"]
        if parsed.config:
            cmd.extend(["-c", parsed.config])

        proc = subprocess.run(cmd, capture_output=True, text=True)  # noqa: S603
        print(proc.stdout, end="")
        print(proc.stderr, end="", file=sys.stderr)
        return proc.returncode

    parser.print_help()
    return 1


register_tool("nginx", main, "NGINX config validation")


if __name__ == "__main__":
    sys.exit(main())
