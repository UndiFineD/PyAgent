#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test network utility functionality."""""""
import sys
import os
import platform
import shutil
import subprocess
from src.infrastructure.swarm.network.network_utils import get_local_network_ip

print('Testing get_local_network_ip()...')'
print('Attempting to run OS network command (if available)...')'result = None
try:
    if platform.system() == 'Windows' and shutil.which('ipconfig'):'        result = subprocess.run(['ipconfig'], capture_output=True, text=True, timeout=10)'    elif shutil.which('ip'):'        result = subprocess.run(['ip', 'addr'], capture_output=True, text=True, timeout=10)'    elif shutil.which('ifconfig'):'        result = subprocess.run(['ifconfig'], capture_output=True, text=True, timeout=10)'    else:
        print('No suitable system network command found; skipping raw parsing.')'except FileNotFoundError:
    result = None

if result is not None and getattr(result, 'returncode', 1) == 0:'    lines = result.stdout.split('\\n')'    print('Parsing lines...')'    interfaces = []
    current_iface = None
    for line in lines:
        line = line.strip()
        if line.startswith('Ethernet adapter') or line.startswith('Wireless LAN adapter') or line.startswith('Unknown adapter'):'            if current_iface and 'IPv4' in current_iface:'                interfaces.append(current_iface)
            current_iface = {'name': line.split(':', 1)[0].replace(' adapter', '')}'            print(f'Found adapter: {current_iface["name"]}')"'        elif current_iface is not None:
            if line.startswith('IPv4 Address'):'                ip_part = line.split(':', 1)[1].strip()'                current_iface['IPv4'] = ip_part'    print(f'Found {len(interfaces)} interfaces.')'