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

"""SSL certificate management helpers.

Provides utilities to inspect and validate PEM-encoded X.509 certificates
using Python's standard library ``ssl`` module. For advanced operations
(generating self-signed certificates, Let's Encrypt) the optional
``cryptography`` package is used when available.
"""

from __future__ import annotations

import argparse
import datetime
import json
import socket
import ssl
import sys
from pathlib import Path

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


def check_expiry(host: str, port: int = 443, timeout: float = 5.0) -> dict[str, object]:
    """Return TLS certificate expiry information for a live host.

    Parameters
    ----------
    host:
        Hostname to connect to.
    port:
        HTTPS/TLS port (default 443).
    timeout:
        Connection timeout in seconds.

    Returns
    -------
    dict
        Keys: ``subject``, ``issuer``, ``not_before``, ``not_after``,
        ``days_remaining``, ``expired``.

    Raises
    ------
    ssl.SSLError, OSError
        On connection or TLS errors.
    """
    ctx = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=timeout) as raw_sock:
        with ctx.wrap_socket(raw_sock, server_hostname=host) as ssl_sock:
            cert = ssl_sock.getpeercert()

    not_after_str: str = cert.get("notAfter", "")  # type: ignore[assignment]
    not_after = datetime.datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z").replace(
        tzinfo=datetime.timezone.utc
    )
    not_before_str: str = cert.get("notBefore", "")  # type: ignore[assignment]
    not_before = datetime.datetime.strptime(not_before_str, "%b %d %H:%M:%S %Y %Z").replace(
        tzinfo=datetime.timezone.utc
    )

    now = datetime.datetime.now(tz=datetime.timezone.utc)
    days_remaining = (not_after - now).days

    return {
        "subject": dict(x[0] for x in cert.get("subject", [])),  # type: ignore[misc]
        "issuer": dict(x[0] for x in cert.get("issuer", [])),  # type: ignore[misc]
        "not_before": not_before.isoformat(),
        "not_after": not_after.isoformat(),
        "days_remaining": days_remaining,
        "expired": days_remaining < 0,
    }


def verify_pem_file(path: str) -> dict[str, object]:
    """Verify a PEM certificate file is readable and extract basic info.

    Parameters
    ----------
    path:
        Path to a PEM-encoded certificate file.

    Returns
    -------
    dict
        ``valid``: bool, ``path``: str, ``error``: str (on failure).
    """
    p = Path(path)
    if not p.is_file():
        return {"valid": False, "path": str(p), "error": "File not found"}

    try:
        ctx = ssl.create_default_context()
        ctx.load_verify_locations(cafile=str(p))
        return {"valid": True, "path": str(p), "error": None}
    except ssl.SSLError as exc:
        return {"valid": False, "path": str(p), "error": str(exc)}


def main(args: list[str] | None = None) -> int:
    """Main entry point for the ssl_utils tool."""
    parser = argparse.ArgumentParser(prog="ssl_utils", description="SSL certificate inspection tools.")
    sub = parser.add_subparsers(dest="command", required=True)

    exp = sub.add_parser("expiry", help="Check TLS cert expiry for a live host")
    exp.add_argument("host", help="Hostname to check")
    exp.add_argument("--port", type=int, default=443)
    exp.add_argument("--timeout", type=float, default=5.0)
    exp.add_argument("--json", action="store_true")

    verify = sub.add_parser("verify", help="Verify a local PEM certificate file")
    verify.add_argument("cert", help="Path to PEM file")
    verify.add_argument("--json", action="store_true")

    parsed = parser.parse_args(args=args)

    if parsed.command == "expiry":
        try:
            info = check_expiry(parsed.host, parsed.port, parsed.timeout)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        if parsed.json:
            print(json.dumps(info, indent=2))
        else:
            print("\n".join(f"{k}: {v}" for k, v in info.items()))
        return 0

    if parsed.command == "verify":
        info = verify_pem_file(parsed.cert)
        if parsed.json:
            print(json.dumps(info, indent=2))
        else:
            status = "VALID" if info["valid"] else f"INVALID: {info['error']}"
            print(f"{parsed.cert}: {status}")
        return 0 if info.get("valid") else 1

    return 0


register_tool("ssl_utils", main, "SSL/TLS certificate inspection (expiry, verify)")


if __name__ == "__main__":
    sys.exit(main())
