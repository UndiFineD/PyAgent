# NetworkUtils

**File**: `src\infrastructure\network\NetworkUtils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 28 functions, 20 imports  
**Lines**: 663  
**Complexity**: 28 (complex)

## Overview

Network Utilities Module - Phase 20: Production Infrastructure
===============================================================

Helper functions for network operations, IP detection, and port management.
Inspired by vLLM's network_utils.py pattern.

Features:
- get_ip: Detect the machine's IP address
- get_loopback_ip: Get localhost IP (IPv4/IPv6 aware)
- get_open_port: Find an available port
- split_host_port: Parse host:port strings
- join_host_port: Format host:port strings
- is_valid_ipv6: Validate IPv6 addresses
- get_tcp_uri: Generate TCP URIs
- ZMQ utilities: Socket helpers for ZeroMQ
- Port scanning and discovery

Author: PyAgent Phase 20

## Functions (28)

### `get_ip(prefer_ipv4, host_env_var)`

Get the machine's IP address.

Args:
    prefer_ipv4: If True, prefer IPv4 over IPv6.
    host_env_var: Optional environment variable to check first.

Returns:
    The detected IP address, or "0.0.0.0" if detection fails.

### `get_loopback_ip(loopback_env_var)`

Get the loopback IP address (localhost).

Automatically detects whether to use IPv4 (127.0.0.1) or IPv6 (::1).

Args:
    loopback_env_var: Optional environment variable to check first.

Returns:
    The loopback IP address.
    
Raises:
    RuntimeError: If no loopback interface is available.

### `test_bind(address, family)`

Test if an address can be bound to.

### `get_hostname()`

Get the local hostname.

### `get_fqdn()`

Get the fully qualified domain name.

### `resolve_hostname(hostname)`

Resolve a hostname to its IP addresses.

Returns:
    List of IP addresses.

### `is_valid_ipv6_address(address)`

Check if a string is a valid IPv6 address.

### `is_valid_ipv4_address(address)`

Check if a string is a valid IPv4 address.

### `is_valid_ip_address(address)`

Check if a string is a valid IP address (v4 or v6).

### `normalize_ip(address)`

Normalize an IP address to standard form.

## Dependencies

**Imports** (20):
- `__future__.annotations`
- `collections.abc.Iterator`
- `collections.abc.Sequence`
- `contextlib`
- `ipaddress`
- `logging`
- `os`
- `psutil`
- `socket`
- `subprocess`
- `sys`
- `tempfile`
- `time`
- `typing.Any`
- `typing.Literal`
- ... and 5 more

---
*Auto-generated documentation*
