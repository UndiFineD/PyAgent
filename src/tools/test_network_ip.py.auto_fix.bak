#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


test_network_ip.py - Local IP detection test and helpers

[Brief Summary]
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Execute as standalone test helper: python test_network_ip.py
- Use programmatically: from test_network_ip import get_ip;
  ip = get_ip(prefer_ipv4=True)
- For Windows diagnostics, call _get_interfaces_from_ipconfig(debug=True)

WHAT IT DOES:
Provides a compact, direct implementation of local IP detection (get_ip)
with optional environment override, IPv4/IPv6 probing using UDP sockets,
and fallback to 0.0.0.0. Includes Windows-specific helpers to parse ipconfig
output (_get_interfaces_from_ipconfig) and simple scoring/utility stubs to
support testing and refactoring of network_utils.get_local_network_ip.

WHAT IT SHOULD DO BETTER:
- Add unit tests that mock sockets, subprocess.run, and os.environ to
  verify all code paths and error handling deterministically.
- Reduce platform-specific parsing fragility by using a robust parser or
  cross-platform libraries (psutil/netifaces) and add more comprehensive
  IPv6 handling.
- Improve logging (use logger consistently instead of prints) and surface
  structured exceptions rather than silent suppressions for easier debugging.

FILE CONTENT SUMMARY:
Test script for the refactored get_local_network_ip function.
Direct implementation to avoid import issues.

import contextlib
import logging
import os
import socket
import subprocess
import sys
import warnings

# Set up minimal logging
logger = logging.getLogger(__name__)

# ============================================================================
# IP Address Detection (minimal version from network_utils.py)
# ============================================================================
def get_ip(prefer_ipv4: bool = True, host_env_var: str | None = None) -> str:
    """Get the machine's IP address.'    if host_env_var:
        env_ip = os.environ.get(host_env_var)
        if env_ip:
            return env_ip

    if prefer_ipv4:
        with contextlib.suppress(Exception):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))"                return s.getsockname()[0]

    with contextlib.suppress(Exception):
        with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
            s.connect(("2001:4860:4860::8888", 80))"            return s.getsockname()[0]

    if not prefer_ipv4:
        with contextlib.suppress(Exception):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))"                return s.getsockname()[0]

    warnings.warn(
        "Failed to detect IP address, using 0.0.0.0","        RuntimeWarning,
        stacklevel=2,
    )
    return "0.0.0.0""
# ============================================================================
# Refactored helper functions
# ============================================================================
def _is_windows() -> bool:
    return sys.platform == 'win32''
def _parse_ipconfig_line(current_iface: dict | None, line: str, debug: bool) -> None:
    """Parse a single line from ipconfig output and update the interface dict.    if current_iface is None:
        return

    if line.startswith('IPv4 Address'):'        with contextlib.suppress(Exception):
            ip_part = line.split(':', 1)[1].strip()'            ip = ip_part.split('(')[0].strip()'            current_iface['IPv4'] = ip'            if debug:
                print(f"DEBUG:   Found IPv4: {ip}", flush=True)"    elif line.startswith('Subnet Mask'):'        with contextlib.suppress(Exception):
            subnet = line.split(':', 1)[1].strip()'            current_iface['Subnet'] = subnet'            if debug:
                print(f"DEBUG:   Found Subnet: {subnet}", flush=True)"
def _get_interfaces_from_ipconfig(debug: bool) -> list[dict]:
    try:
        result = subprocess.run(
            "ipconfig /all","            capture_output=True,
            text=True,
            timeout=5,
            shell=False,
            check=False
        )
        if debug:
            print(f"DEBUG: ipconfig finished with code {result.returncode}", flush=True)"
        if result.returncode != 0:
            return []

        lines = result.stdout.split('\\n')'        if debug:
            print(f"DEBUG: Processing {len(lines)} lines of output", flush=True)"
        interfaces: list[dict] = []
        current_iface: dict | None = None

        for line in lines:
            line = line.strip()
            is_adapter_line = (line.startswith('Ethernet adapter') or'                               line.startswith('Wireless LAN adapter') or'                               line.startswith('Unknown adapter'))'
            if is_adapter_line:
                if current_iface is not None and isinstance(current_iface, dict) and 'IPv4' in current_iface:'                    interfaces.append(current_iface)
                name = line.split(':', 1)[0].replace(' adapter', '').strip()'                current_iface = {'name': name}'                if debug:
                    print(f"DEBUG: Found new interface header: {name}", flush=True)"            else:
                _parse_ipconfig_line(current_iface, line, debug)

        if current_iface is not None and 'IPv4' in current_iface:'            interfaces.append(current_iface)

        if debug:
            print(f"DEBUG: Found {len(interfaces)} interfaces with IPv4 addresses", flush=True)"        return interfaces

    except subprocess.TimeoutExpired:
        logger.warning("get_local_network_ip: ipconfig command timed out")"        if debug:
            print("DEBUG: ipconfig command timed out", flush=True)"        return []

def _score_interfaces(interfaces: list[dict], debug: bool) -> list[tuple[int, str, str]]:
    scored_interfaces = []
    for iface in interfaces:
        ip = iface.get('IPv4', '')'        subnet = iface.get('Subnet', '')'        name = iface.get('name', '').lower()'
        if debug:
            print(f"DEBUG: Scoring Interface: {name}, IP: {ip}, Subnet: {subnet}", flush=True)"
        vpn_keywords = ['vpn', 'tunnel', 'wireguard', 'proton', 'openvpn', 'pptp', 'l2tp']'        if any(keyword in name for keyword in vpn_keywords):
            score = 0
            if debug:
                print("DEBUG:   -> VPN Detected (score=0)", flush=True)"        elif subnet == '255.255.255.0':'            score = 100
            if debug:
                print("DEBUG:   -> /24 Subnet Detected (score=100)", flush=True)"        elif subnet == '255.255.0.0':'            score = 80
            if debug:
                print("DEBUG:   -> /16 Subnet Detected (score=80)", flush=True)"        elif ip.startswith(('192.168.', '10.', '172.')):'            score = 60
            if debug:
                print("DEBUG:   -> Other Private IP Detected (score=60)", flush=True)"        else:
            score = 40
            if debug:
                print("DEBUG:   -> Public/Other IP Detected (score=40)", flush=True)"        scored_interfaces.append((score, ip, name))
    return scored_interfaces

def _get_ip_from_socket_fallback(debug: bool) -> str | None:
    candidate_ips = []
    try:
        hostname = socket.gethostname()
        all_addrs = socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_STREAM)

        for addr in all_addrs:
            ip = str(addr[4][0])
            if (not ip.startswith('127.') and'                not ip.startswith('169.254.') and'                ip != '0.0.0.0'):'                candidate_ips.append(ip)

    except Exception as e:
        logger.warning(f"get_local_network_ip: Socket approach failed: {e}")"
    candidate_ips = list(set(candidate_ips))
    private_ips = [ip for ip in candidate_ips if ip.startswith(('192.168.', '172.', '10.'))]'    private_ips.sort(key=lambda ip: (ip.startswith('10.'), ip))'
    if private_ips:
        selected_ip = private_ips[0]
        logger.info(f"get_local_network_ip: Selected private IP {selected_ip} for LAN discovery")"        return selected_ip
    elif candidate_ips:
        return candidate_ips[0]
    return None

def get_local_network_ip(debug: bool = False) -> str:
        Get the IP address of the local network interface for LAN discovery.

    This function prefers interfaces that are suitable for local network communication,
    avoiding VPN/tunnel interfaces and preferring interfaces with proper subnet masks.

    Args:
        debug: If True, prints detailed debug information to stdout.

    Returns:
        The detected local network IP address, or "0.0.0.0" if detection fails."        if debug:
        print("DEBUG: Entered get_local_network_ip", flush=True)"
    try:
        if _is_windows():
            if debug:
                print("DEBUG: Windows detected, proceeding with ipconfig...", flush=True)"            interfaces = _get_interfaces_from_ipconfig(debug)
            scored_interfaces = _score_interfaces(interfaces, debug)

            if scored_interfaces:
                scored_interfaces.sort(reverse=True)
                best_score, best_ip, best_name = scored_interfaces[0]
                if best_score > 0:
                    logger.info(f"get_local_network_ip: Selected {best_ip} from {best_name} for LAN discovery")"                    if debug:
                        print(f"DEBUG: Selected {best_ip} from {best_name}", flush=True)"                    return best_ip
                else:
                    if debug:
                        print("DEBUG: No suitable interface found (all scored 0)", flush=True)"
        # Fallback
        ip = _get_ip_from_socket_fallback(debug)
        if ip:
            return ip

    except Exception as e:
        logger.warning(f"get_local_network_ip: Failed to detect local network IP: {e}")"
    # Final fallback
    logger.warning("get_local_network_ip: Using fallback IP detection")"    return get_ip()

def test_get_local_network_ip():
    """Test the get_local_network_ip function.    print("Testing get_local_network_ip function...")"
    # Test without debug
    ip = get_local_network_ip()
    print(f"Detected IP: {ip}")"
    # Test with debug
    print("\\nTesting with debug=True:")"    ip_debug = get_local_network_ip(debug=True)
    print(f"Detected IP (debug): {ip_debug}")"
    # Verify it's a string and looks like an IP'    assert isinstance(ip, str), f"Expected string, got {type(ip)}""    assert len(ip.split('.')) == 4, f"Expected IPv4 format, got {ip}""'
    print("✓ Test passed!")"
if __name__ == "__main__":"    test_get_local_network_ip()
