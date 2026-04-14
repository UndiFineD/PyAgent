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

"""Network testing utilities (e.g. dual-stack validation)."""

from __future__ import annotations

import argparse
import asyncio
import sys

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


async def _check_host(host: str, port: int, timeout: float) -> bool:
    """Check if we can establish a TCP connection to the specified host and port."""
    try:
        fut = asyncio.open_connection(host, port)
        reader, writer = await asyncio.wait_for(fut, timeout)
        writer.close()
        await writer.wait_closed()
        return True
    except Exception:
        return False


async def main(args: list[str] | None = None) -> int:
    """Main entry point for the nettest tool."""
    parser = argparse.ArgumentParser(prog="nettest")
    parser.add_argument("host", help="Host to test")
    parser.add_argument("port", type=int, help="TCP port to connect to")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout in seconds")

    parsed = parser.parse_args(args=args)

    success = await _check_host(parsed.host, parsed.port, parsed.timeout)
    print("OK" if success else "FAIL")
    return 0 if success else 1


register_tool("nettest", main, "Test TCP connectivity to a host/port")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
