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

"""SSL certificate management helpers."""

from __future__ import annotations

import argparse
import ssl
import sys
from datetime import datetime

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


def _read_pem_cert(path: str) -> ssl.SSLContext:
    """Load a PEM certificate file as a trust root into an SSL context."""
    ctx = ssl.create_default_context()
    ctx.load_verify_locations(cafile=path)
    return ctx


def main(args: list[str] | None = None) -> int:
    """Main entry point for the ssl_utils tool."""
    parser = argparse.ArgumentParser(prog="ssl_utils")
    parser.add_argument("cert", help="Path to PEM-encoded certificate")
    parsed = parser.parse_args(args=args)

    try:
        ctx = _read_pem_cert(parsed.cert)
        # can't parse expiration easily without cryptography; do basic check
        print(f"Loaded cert: {parsed.cert}")
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


register_tool("ssl_utils", main, "SSL certificate helper (basic)")


if __name__ == "__main__":
    sys.exit(main())
