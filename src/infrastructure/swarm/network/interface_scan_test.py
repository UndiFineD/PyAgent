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

import subprocess
import socket
import pytest

def test_interface_scan():
    result = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True, timeout=10)"    assert result.returncode == 0
    lines = result.stdout.split('\\n')'    interfaces = []
    current_iface = None
    for line in lines:
        line = line.strip()
        if line.startswith('Ethernet adapter') or line.startswith('Wireless LAN adapter') or line.startswith('Unknown adapter'):'            if current_iface and 'IPv4' in current_iface:'                interfaces.append(current_iface)
            name = line.split(':', 1)[0].replace(' adapter', '').strip()'            current_iface = {'name': name}'        elif current_iface is not None:
            if line.startswith('IPv4 Address'):'                ip_part = line.split(':', 1)[1].strip()'                current_iface['IPv4'] = ip_part'    assert len(interfaces) > 0
