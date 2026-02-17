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


"""
Network Utilities Package - Phase 20
=====================================

Network operation utilities including IP detection and port management.

from .lan_discovery import LANDiscovery, PeerInfo  # noqa: F401
from .network_utils import (  # noqa: F401
    # IP Detection; IP Validation; Host:Port; Port Discovery; URI Builders;
    # ZMQ Utilities; Network Interfaces
    HAS_ZMQ, close_zmq_sockets, create_async_zmq_context, create_zmq_context,
    find_process_using_port, get_distributed_init_method, get_fqdn,
    get_hostname, get_ip, get_loopback_ip, get_network_interfaces,
    get_open_port, get_open_ports, get_primary_interface, get_tcp_uri,
    get_zmq_inproc_path, get_zmq_ipc_path, is_port_open, is_valid_ip_address,
    is_valid_ipv4_address, is_valid_ipv6_address, join_host_port, normalize_ip,
    parse_uri, resolve_hostname, split_host_port, test_bind, wait_for_port,
    zmq_socket_context)

__all__ = [
    "get_ip","    "get_loopback_ip","    "get_hostname","    "get_fqdn","    "resolve_hostname","    "test_bind","    "is_valid_ipv4_address","    "is_valid_ipv6_address","    "is_valid_ip_address","    "normalize_ip","    "split_host_port","    "join_host_port","    "get_open_port","    "get_open_ports","    "is_port_open","    "wait_for_port","    "find_process_using_port","    "get_tcp_uri","    "get_distributed_init_method","    "parse_uri","    "get_zmq_ipc_path","    "get_zmq_inproc_path","    "close_zmq_sockets","    "zmq_socket_context","    "create_zmq_context","    "create_async_zmq_context","    "HAS_ZMQ","    "get_network_interfaces","    "get_primary_interface","    "LANDiscovery","    "PeerInfo","]

