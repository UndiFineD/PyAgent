# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-NachoVPN\src\nachovpn\core\utils.py
import logging
import os

from scapy.all import (
    ARP,
    IP,
    TCP,
    UDP,
    Ether,
    IPv6,
    conf,
    get_if_addr,
    get_if_hwaddr,
    getmacbyip,
    rdpcap,
    sendp,
    sniff,
    srp,
    wrpcap,
)


class PacketHandler:
    """
    TODO: Implement a NAT-based packet handler where the plugin provides a callback function
    that is called when a packet is received back from its destination and written to the client tunnel.
    """

    def __init__(self, write_pcap=False, pcap_filename=None, logger_name="PacketHandler"):
        self.write_pcap = write_pcap
        self.pcap_filename = pcap_filename
        self.logger = logging.getLogger(logger_name)
        if self.write_pcap and pcap_filename is not None:
            os.makedirs(os.path.dirname(pcap_filename), exist_ok=True)

    def get_free_nat_port(self):
        return 0

    def forward_tcp_packet(self, packet_data):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        sport = packet[TCP].sport
        dport = packet[TCP].dport
        self.logger.debug(f"Processing TCP packet: {src_ip}:{sport} -> {dst_ip}:{dport}")

        # Get a unique NAT port for this connection
        nat_port = self.get_free_nat_port()

        # Modify packet for NAT
        packet[IP].src = get_if_addr(conf.iface)  # Replace source IP with our IP
        packet[TCP].sport = nat_port  # Replace source port with NAT port

        self.logger.debug(f"New connection: {src_ip}:{sport} -> {dst_ip}:{dport} (NAT port: {nat_port})")

        # Modify packet for NAT
        packet[IP].src = get_if_addr(conf.iface)  # Replace source IP with our IP
        packet[TCP].sport = nat_port  # Replace source port with NAT port

        # Recalculate checksums
        del packet[IP].chksum
        del packet[TCP].chksum

        # Send the packet out
        sendp(packet, verbose=False, iface=conf.iface)

    def packet_sniffer(self):
        def packet_callback(packet):
            try:
                if IP not in packet:
                    return

                # TODO: restore original IP and TCP ports
                if self.receive_callback:
                    self.receive_callback(packet)
            except Exception as e:
                self.logger.error(f"Error processing packet: {e}")

        self.logger.info("Starting packet sniffer")
        sniff(iface=conf.iface, prn=packet_callback, store=False)

    def handle_client_packet(self, packet_data):
        packet = IP(packet_data)
        self.logger.info(f"Received packet: {packet}")
        self.append_to_pcap(packet)

    def append_to_pcap(self, packet):
        try:
            if self.write_pcap and self.pcap_filename is not None:
                # Add fake layer 2 data to the packet, if missing
                if not packet.haslayer(Ether):
                    src_mac = get_if_hwaddr(conf.iface)
                    fake_ether = Ether(src=src_mac, dst=None)
                    packet = fake_ether / packet
                wrpcap(self.pcap_filename, packet, append=True)
        except Exception as e:
            logging.error(f"Error appending to PCAP: {e}")
