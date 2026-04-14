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

"""Port knocking client utility."""

from __future__ import annotations

import argparse
import socket
import sys

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


def main(args: list[str] | None = None) -> int:
    """Main entry point for the knock tool."""
    parser = argparse.ArgumentParser(prog="knock")
    parser.add_argument("host", help="Host to knock")
    parser.add_argument("ports", nargs="+", type=int, help="Ports to knock in sequence")
    parser.add_argument("--timeout", type=float, default=0.5, help="Connection timeout per port")

    parsed = parser.parse_args(args=args)

    def _check_port(port: int) -> str:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(parsed.timeout)
        try:
            sock.connect((parsed.host, port))
            return f"{parsed.host}:{port} -> OPEN"
        except Exception:
            return f"{parsed.host}:{port} -> CLOSED"
        finally:
            sock.close()

    print("\n".join(map(_check_port, parsed.ports)))
    return 0


register_tool("knock", main, "Port knocking client")


if __name__ == "__main__":
    sys.exit(main())
