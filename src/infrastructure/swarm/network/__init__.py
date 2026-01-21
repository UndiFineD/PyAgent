"""
Network Utilities Package - Phase 20
=====================================

Network operation utilities including IP detection and port management.
"""

from .network_utils import (
    # IP Detection
    get_ip,
    get_loopback_ip,
    get_hostname,
    get_fqdn,
    resolve_hostname,
    test_bind,
    # IP Validation
    is_valid_ipv4_address,
    is_valid_ipv6_address,
    is_valid_ip_address,
    normalize_ip,
    # Host:Port
    split_host_port,
    join_host_port,
    # Port Discovery
    get_open_port,
    get_open_ports,
    is_port_open,
    wait_for_port,
    find_process_using_port,
    # URI Builders
    get_tcp_uri,
    get_distributed_init_method,
    parse_uri,
    # ZMQ Utilities
    get_zmq_ipc_path,
    get_zmq_inproc_path,
    close_zmq_sockets,
    zmq_socket_context,
    create_zmq_context,
    create_async_zmq_context,
    HAS_ZMQ,
    # Network Interfaces
    get_network_interfaces,
    get_primary_interface,
)
from .lan_discovery import LANDiscovery, PeerInfo

__all__ = [
    "get_ip",
    "get_loopback_ip",
    "get_hostname",
    "get_fqdn",
    "resolve_hostname",
    "test_bind",
    "is_valid_ipv4_address",
    "is_valid_ipv6_address",
    "is_valid_ip_address",
    "normalize_ip",
    "split_host_port",
    "join_host_port",
    "get_open_port",
    "get_open_ports",
    "is_port_open",
    "wait_for_port",
    "find_process_using_port",
    "get_tcp_uri",
    "get_distributed_init_method",
    "parse_uri",
    "get_zmq_ipc_path",
    "get_zmq_inproc_path",
    "close_zmq_sockets",
    "zmq_socket_context",
    "create_zmq_context",
    "create_async_zmq_context",
    "HAS_ZMQ",
    "get_network_interfaces",
    "get_primary_interface",
]
