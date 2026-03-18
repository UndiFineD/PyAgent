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

"""IP address and CIDR calculation helpers."""

from __future__ import annotations

import argparse
import ipaddress
import sys

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


def main(args: list[str] | None = None) -> int:
    """Run the netcalc CLI."""
    parser = argparse.ArgumentParser(prog="netcalc")
    sub = parser.add_subparsers(dest="command", required=True)

    cidr = sub.add_parser("cidr", help="Print network details for a CIDR block")
    cidr.add_argument("cidr", help="CIDR notation (e.g. 192.168.0.0/24)")

    parsed = parser.parse_args(args=args)

    if parsed.command == "cidr":
        net = ipaddress.ip_network(parsed.cidr, strict=False)
        print(f"Network: {net.network_address}")
        print(f"Netmask: {net.netmask}")
        print(f"Broadcast: {net.broadcast_address}")
        print(f"Hosts: {net.num_addresses}")
        return 0

    parser.print_help()
    return 1


register_tool("netcalc", main, "IP/CIDR calculation utilities")


if __name__ == "__main__":
    sys.exit(main())
