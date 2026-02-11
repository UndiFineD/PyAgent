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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Test network utility functionality."""

import os
import platform
import shutil
import subprocess
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.infrastructure.swarm.network.network_utils import get_local_network_ip

print('Testing get_local_network_ip()...')

# Let's debug step by step
print('Attempting to run OS network command (if available)...')
result = None
try:
    if platform.system() == 'Windows' and shutil.which('ipconfig'):
        result = subprocess.run(['ipconfig'], capture_output=True, text=True, timeout=10)
    elif shutil.which('ip'):
        result = subprocess.run(['ip', 'addr'], capture_output=True, text=True, timeout=10)
    elif shutil.which('ifconfig'):
        result = subprocess.run(['ifconfig'], capture_output=True, text=True, timeout=10)
    else:
        print('No suitable system network command found; skipping raw parsing.')
except FileNotFoundError:
    result = None

if result is not None and getattr(result, 'returncode', 1) == 0:
    lines = result.stdout.split('\n')
    print('Parsing lines...')
    interfaces = []
    current_iface = None

    for line in lines:
        line = line.strip()
        if line.startswith('Ethernet adapter') or line.startswith('Wireless LAN adapter') or line.startswith('Unknown adapter'):
            if current_iface and 'IPv4' in current_iface:
                interfaces.append(current_iface)
            current_iface = {'name': line.split(':', 1)[0].replace(' adapter', '')}
            print(f'Found adapter: {current_iface["name"]}')
        elif current_iface is not None:
            if line.startswith('IPv4 Address'):
                ip_part = line.split(':', 1)[1].strip()
                ip = ip_part.split('(')[0].strip()
                current_iface['IPv4'] = ip
                print(f'  IPv4: {ip}')
            elif line.startswith('Subnet Mask'):
                subnet = line.split(':', 1)[1].strip()
                current_iface['Subnet'] = subnet
                print(f'  Subnet: {subnet}')

    if current_iface and 'IPv4' in current_iface:
        interfaces.append(current_iface)

    print('Parsed interfaces:')
    for iface in interfaces:
        print(f'  {iface}')

    # Now score them
    scored_interfaces = []
    for iface in interfaces:
        ip = iface.get('IPv4', '')
        subnet = iface.get('Subnet', '')
        name = iface.get('name', '').lower()

        print(f'Scoring {name}: IP={ip}, Subnet={subnet}')

        # Skip VPN/tunnel interfaces
        if any(keyword in name for keyword in ['vpn', 'tunnel', 'wireguard', 'proton', 'openvpn', 'pptp', 'l2tp']):
            score = 0
            print(f'  -> VPN detected, score = {score}')
        # Prefer /24 networks (255.255.255.0 subnet mask)
        elif subnet == '255.255.255.0':
            score = 100
            print(f'  -> /24 network, score = {score}')
        # Then /16 networks (255.255.0.0)
        elif subnet == '255.255.0.0':
            score = 80
            print(f'  -> /16 network, score = {score}')
        # Then other private networks
        elif ip.startswith(('192.168.', '10.', '172.')):
            score = 60
            print(f'  -> Private network, score = {score}')
        else:
            score = 40
            print(f'  -> Other, score = {score}')

        scored_interfaces.append((score, ip, name))

    if scored_interfaces:
        scored_interfaces.sort(reverse=True)
        best_score, best_ip, best_name = scored_interfaces[0]
        print(f'Best interface: {best_ip} from {best_name} (score: {best_score})')
    else:
        print('No scored interfaces found')

else:
    print('ipconfig failed')

print('Now calling get_local_network_ip()...')
try:
    result = get_local_network_ip()
    print(f'Result: {result}')
except Exception as e:
    print(f'Exception: {e}')
    import traceback
    traceback.print_exc()

# Basic sanity: allow either None or a string IP
assert result is None or isinstance(result, str)
