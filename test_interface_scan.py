#!/usr/bin/env python3
import subprocess
import socket

# Test interface scanning using the same approach as network_utils.py
print("Testing interface scanning with ipconfig...")

try:
    # Use ipconfig /all to get interface details
    result = subprocess.run(
        ["ipconfig", "/all"],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode == 0:
        lines = result.stdout.split('\n')
        print(f"DEBUG: Processing {len(lines)} lines of output")
        interfaces = []
        current_iface = None

        for line in lines:
            line = line.strip()
            # print(f"DEBUG: Line: {line}")  # Very verbose

            if line.startswith('Ethernet adapter') or line.startswith('Wireless LAN adapter') or line.startswith('Unknown adapter'):
                # Save previous interface if it had an IP
                if current_iface:
                    if 'IPv4' in current_iface:
                        print(f"DEBUG: Completed interface: {current_iface['name']} with IP {current_iface.get('IPv4')}")
                        interfaces.append(current_iface)
                    else:
                        print(f"DEBUG: Discarding interface {current_iface['name']} (No IPv4)")
                
                # Start new interface
                name = line.split(':', 1)[0].replace(' adapter', '').strip()
                current_iface = {'name': name}
                print(f"DEBUG: Found new interface header: {name}")
                
            elif current_iface is not None:
                if line.startswith('IPv4 Address'):
                    # Extract IP address - handle the dotted format
                    ip_part = line.split(':', 1)[1].strip()
                    ip = ip_part.split('(')[0].strip()
                    current_iface['IPv4'] = ip
                    print(f"DEBUG:   Found IPv4: {ip}")
                elif line.startswith('Subnet Mask'):
                    subnet = line.split(':', 1)[1].strip()
                    current_iface['Subnet'] = subnet
                    print(f"DEBUG:   Found Subnet: {subnet}")

        # Add the last interface
        if current_iface:
            if 'IPv4' in current_iface:
                print(f"DEBUG: Completed last interface: {current_iface['name']} with IP {current_iface.get('IPv4')}")
                interfaces.append(current_iface)
            else:
                print(f"DEBUG: Discarding last interface {current_iface['name']} (No IPv4)")

        print(f"\nFound {len(interfaces)} interfaces with IPv4 addresses:")

        # Filter and score interfaces
        scored_interfaces = []
        for iface in interfaces:
            ip = iface.get('IPv4', '')
            subnet = iface.get('Subnet', '')
            name = iface.get('name', '').lower()

            print(f"Interface: {iface['name']}")
            print(f"  IP: {ip}") 
            print(f"  Subnet: {subnet}")

            # Skip VPN/tunnel interfaces
            is_vpn = any(keyword in name for keyword in ['vpn', 'tunnel', 'wireguard', 'proton', 'openvpn', 'pptp', 'l2tp'])
            if is_vpn:
                score = 0
                print(f"  -> VPN Detected (score=0)")
            else:
                # Prefer /24 networks (255.255.255.0 subnet mask)
                if subnet == '255.255.255.0':
                    score = 100
                    print(f"  -> /24 Subnet Detected (score=100)")
                # Then /16 networks (255.255.0.0)
                elif subnet == '255.255.0.0':
                    score = 80
                    print(f"  -> /16 Subnet Detected (score=80)")
                # Then other private networks
                elif ip.startswith(('192.168.', '10.', '172.')):
                    score = 60
                    print(f"  -> Other Private IP Detected (score=60)")
                else:
                    score = 40
                    print(f"  -> Public/Other IP Detected (score=40)")

            scored_interfaces.append((score, ip, iface['name']))

        # Sort by score and show results
        scored_interfaces.sort(reverse=True)
        print(f"\nScored interfaces (highest first):")
        for score, ip, name in scored_interfaces:
            status = "SELECTED" if score > 0 else "SKIPPED"
            print(f"  {status}: {name} - {ip} (score: {score})")

        # Return the highest scoring interface
        if scored_interfaces and scored_interfaces[0][0] > 0:
            best_score, best_ip, best_name = scored_interfaces[0]
            print(f"\nSelected interface: {best_name} with IP {best_ip}")
        else:
            print("\nNo suitable non-VPN interface found")

    else:
        print(f"ipconfig failed with return code {result.returncode}")
        print(f"Error: {result.stderr}")

except subprocess.TimeoutExpired:
    print("ipconfig command timed out")
except Exception as e:
    print(f"Exception: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)
print("Testing socket approach...")

try:
    hostname = socket.gethostname()
    all_addrs = socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_STREAM)

    local_ips = []
    for addr in all_addrs:
        ip = addr[4][0]
        print(f'Found IP: {ip}')
        if (not ip.startswith('127.') and
            not ip.startswith('169.254.') and
            ip != '0.0.0.0'):
            local_ips.append(ip)
            print(f'  -> Valid IP: {ip}')

    if local_ips:
        print(f'All valid IPs: {local_ips}')
        # Prefer private networks, with 192.168.x.x preferred over 10.x.x.x
        private_ips = [ip for ip in local_ips if ip.startswith(('192.168.', '172.', '10.'))]
        private_ips.sort(key=lambda ip: (ip.startswith('10.'), ip))
        if private_ips:
            print(f'Selected private IP: {private_ips[0]}')
        else:
            print(f'Selected IP: {local_ips[0]}')
    else:
        print('No valid local IPs found')

except Exception as e:
    print(f'Socket exception: {e}')
    import traceback
    traceback.print_exc()