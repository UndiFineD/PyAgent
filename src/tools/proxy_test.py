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

"""Proxy configuration validation utilities."""

from __future__ import annotations

import argparse
import sys
import urllib.request

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


def main(args: list[str] | None = None) -> int:
    """Main entry point for the proxy_test tool."""
    parser = argparse.ArgumentParser(prog="proxy_test")
    parser.add_argument("--url", default="http://example.com", help="URL to fetch for proxy test")
    parser.add_argument("--proxy", help="Proxy URL (e.g. http://127.0.0.1:3128)")

    parsed = parser.parse_args(args=args)

    opener = urllib.request.build_opener()
    if parsed.proxy:
        opener.add_handler(urllib.request.ProxyHandler({"http": parsed.proxy, "https": parsed.proxy}))

    try:
        with opener.open(parsed.url, timeout=5) as resp:
            print(f"{resp.status} {resp.reason}")
            return 0
    except Exception as e:
        print(f"Proxy test failed: {e}", file=sys.stderr)
        return 1


register_tool("proxy_test", main, "Test HTTP proxy connectivity")


if __name__ == "__main__":
    sys.exit(main())
