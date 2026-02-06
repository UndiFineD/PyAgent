#!/usr/bin/env python3
import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.infrastructure.swarm.network.network_utils import get_local_network_ip

print('Testing get_local_network_ip()...')

# Let's debug step by step
import subprocess
print('Running ipconfig...')
result = subprocess.run(['ipconfig'], capture_output=True, text=True, timeout=10)
print('ipconfig return code:', result.returncode)

if result.returncode == 0:
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