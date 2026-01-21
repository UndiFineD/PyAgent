"""
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
"""

from __future__ import annotations

import contextlib
import ipaddress
import logging
import os
import socket
import sys
import warnings
from collections.abc import Iterator, Sequence
from typing import Any, Literal
from urllib.parse import urlparse
from uuid import uuid4

logger = logging.getLogger(__name__)

# Optional ZMQ import
try:
    import zmq
    import zmq.asyncio
    HAS_ZMQ = True
except ImportError:
    HAS_ZMQ = False
    zmq = None  # type: ignore

# Optional psutil import
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    psutil = None  # type: ignore


# ============================================================================
# IP Address Detection
# ============================================================================


def get_ip(
    prefer_ipv4: bool = True,
    host_env_var: str | None = None
) -> str:
    """
    Get the machine's IP address.
    
    Args:
        prefer_ipv4: If True, prefer IPv4 over IPv6.
        host_env_var: Optional environment variable to check first.
    
    Returns:
        The detected IP address, or "0.0.0.0" if detection fails.
    """
    # Check environment variable first
    if host_env_var:
        env_ip = os.environ.get(host_env_var)
        if env_ip:
            return env_ip
    
    # Try IPv4 first if preferred
    if prefer_ipv4:
        with contextlib.suppress(Exception):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                # Doesn't need to be reachable
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
    
    # Try IPv6
    with contextlib.suppress(Exception):
        with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
            s.connect(("2001:4860:4860::8888", 80))
            return s.getsockname()[0]
    
    # Try IPv4 if we didn't try it first
    if not prefer_ipv4:
        with contextlib.suppress(Exception):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
    
    warnings.warn(
        "Failed to detect IP address, using 0.0.0.0",
        RuntimeWarning,
        stacklevel=2,
    )
    return "0.0.0.0"


def get_loopback_ip(loopback_env_var: str | None = None) -> str:
    """
    Get the loopback IP address (localhost).
    
    Automatically detects whether to use IPv4 (127.0.0.1) or IPv6 (::1).
    
    Args:
        loopback_env_var: Optional environment variable to check first.
    
    Returns:
        The loopback IP address.
        
    Raises:
        RuntimeError: If no loopback interface is available.
    """
    if loopback_env_var:
        env_ip = os.environ.get(loopback_env_var)
        if env_ip:
            return env_ip
    
    # Test IPv4 loopback
    if test_bind("127.0.0.1", socket.AF_INET):
        return "127.0.0.1"
    
    # Test IPv6 loopback
    if test_bind("::1", socket.AF_INET6):
        return "::1"
    
    raise RuntimeError(
        "Neither 127.0.0.1 nor ::1 are bound to a local interface."
    )


def test_bind(address: str, family: int) -> bool:
    """Test if an address can be bound to."""
    try:
        with socket.socket(family, socket.SOCK_DGRAM) as s:
            s.bind((address, 0))  # Port 0 = auto assign
        return True
    except OSError:
        return False


def get_hostname() -> str:
    """Get the local hostname."""
    return socket.gethostname()


def get_fqdn() -> str:
    """Get the fully qualified domain name."""
    return socket.getfqdn()


def resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to its IP addresses.
    
    Returns:
        List of IP addresses.
    """
    try:
        results = socket.getaddrinfo(hostname, None)
        return list(set(r[4][0] for r in results))
    except socket.gaierror:
        return []


# ============================================================================
# IPv6 Utilities
# ============================================================================


def is_valid_ipv6_address(address: str) -> bool:
    """Check if a string is a valid IPv6 address."""
    try:
        ipaddress.IPv6Address(address)
        return True
    except ValueError:
        return False


def is_valid_ipv4_address(address: str) -> bool:
    """Check if a string is a valid IPv4 address."""
    try:
        ipaddress.IPv4Address(address)
        return True
    except ValueError:
        return False


def is_valid_ip_address(address: str) -> bool:
    """Check if a string is a valid IP address (v4 or v6)."""
    return is_valid_ipv4_address(address) or is_valid_ipv6_address(address)


def normalize_ip(address: str) -> str:
    """Normalize an IP address to standard form."""
    if is_valid_ipv4_address(address):
        return str(ipaddress.IPv4Address(address))
    elif is_valid_ipv6_address(address):
        return str(ipaddress.IPv6Address(address))
    return address


# ============================================================================
# Host:Port Parsing
# ============================================================================


def split_host_port(host_port: str) -> tuple[str, int]:
    """
    Parse a host:port string into components.
    
    Handles IPv6 addresses with brackets: [::1]:8080
    
    Args:
        host_port: String in format "host:port" or "[ipv6]:port"
    
    Returns:
        Tuple of (host, port)
    
    Raises:
        ValueError: If the format is invalid.
    """
    # IPv6 with brackets
    if host_port.startswith("["):
        try:
            host, rest = host_port.rsplit("]", 1)
            host = host[1:]  # Remove leading [
            port = int(rest.split(":")[1])
            return host, port
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid host:port format: {host_port}") from e
    else:
        # IPv4 or hostname
        try:
            host, port_str = host_port.rsplit(":", 1)
            return host, int(port_str)
        except ValueError as e:
            raise ValueError(f"Invalid host:port format: {host_port}") from e


def join_host_port(host: str, port: int) -> str:
    """
    Join a host and port into a string.
    
    Handles IPv6 addresses by adding brackets.
    
    Args:
        host: Hostname or IP address.
        port: Port number.
    
    Returns:
        Formatted string "host:port" or "[ipv6]:port"
    """
    if is_valid_ipv6_address(host):
        return f"[{host}]:{port}"
    return f"{host}:{port}"


# ============================================================================
# Port Discovery
# ============================================================================


def get_open_port(
    start_port: int | None = None,
    max_attempts: int = 100,
    prefer_ipv4: bool = True
) -> int:
    """
    Find an available port.
    
    Args:
        start_port: Optional starting port to try.
        max_attempts: Maximum ports to try if start_port is specified.
        prefer_ipv4: If True, prefer IPv4 sockets.
    
    Returns:
        An available port number.
        
    Raises:
        RuntimeError: If no port is available.
    """
    if start_port is not None:
        # Try specific port range
        for port in range(start_port, start_port + max_attempts):
            try:
                family = socket.AF_INET if prefer_ipv4 else socket.AF_INET6
                with socket.socket(family, socket.SOCK_STREAM) as s:
                    s.bind(("", port))
                    return port
            except OSError:
                continue
        raise RuntimeError(f"No available port in range {start_port}-{start_port + max_attempts}")
    
    # Let OS assign a port
    try:
        family = socket.AF_INET if prefer_ipv4 else socket.AF_INET6
        with socket.socket(family, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            return s.getsockname()[1]
    except OSError:
        # Try the other family
        family = socket.AF_INET6 if prefer_ipv4 else socket.AF_INET
        with socket.socket(family, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            return s.getsockname()[1]


def get_open_ports(count: int = 5, **kwargs: Any) -> list[int]:
    """
    Get multiple available ports.
    
    Args:
        count: Number of ports to find.
        **kwargs: Additional arguments for get_open_port.
    
    Returns:
        List of available port numbers.
    """
    ports: set[int] = set()
    while len(ports) < count:
        ports.add(get_open_port(**kwargs))
    return list(ports)


def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """
    Check if a port is open (accepting connections).
    
    Args:
        host: Host to check.
        port: Port to check.
        timeout: Connection timeout in seconds.
    
    Returns:
        True if the port is accepting connections.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, socket.error):
        return False


def wait_for_port(
    host: str,
    port: int,
    timeout: float = 30.0,
    poll_interval: float = 0.5
) -> bool:
    """
    Wait for a port to become available.
    
    Args:
        host: Host to check.
        port: Port to check.
        timeout: Total timeout in seconds.
        poll_interval: Interval between checks.
    
    Returns:
        True if port became available, False if timeout.
    """
    import time
    deadline = time.monotonic() + timeout
    
    while time.monotonic() < deadline:
        if is_port_open(host, port, timeout=min(poll_interval, 0.5)):
            return True
        time.sleep(poll_interval)
    
    return False


def find_process_using_port(port: int) -> Any | None:
    """
    Find the process using a specific port.
    
    Requires psutil.
    
    Returns:
        psutil.Process if found, None otherwise.
    """
    if not HAS_PSUTIL:
        logger.warning("psutil not installed, cannot find process")
        return None
    
    for conn in psutil.net_connections():
        if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
            try:
                return psutil.Process(conn.pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    return None


# ============================================================================
# URI Builders
# ============================================================================


def get_tcp_uri(ip: str, port: int) -> str:
    """
    Build a TCP URI string.
    
    Args:
        ip: IP address.
        port: Port number.
    
    Returns:
        URI in format "tcp://ip:port" or "tcp://[ipv6]:port"
    """
    if is_valid_ipv6_address(ip):
        return f"tcp://[{ip}]:{port}"
    return f"tcp://{ip}:{port}"


def get_distributed_init_method(ip: str, port: int) -> str:
    """
    Get the distributed initialization method string.
    
    Compatible with PyTorch distributed.
    """
    return get_tcp_uri(ip, port)


def parse_uri(uri: str) -> dict[str, Any]:
    """
    Parse a URI into components.
    
    Returns:
        Dictionary with scheme, host, port, path, query, fragment.
    """
    parsed = urlparse(uri)
    return {
        "scheme": parsed.scheme,
        "host": parsed.hostname,
        "port": parsed.port,
        "path": parsed.path,
        "query": parsed.query,
        "fragment": parsed.fragment,
        "netloc": parsed.netloc,
    }


# ============================================================================
# ZeroMQ Utilities
# ============================================================================


def get_zmq_ipc_path(base_path: str | None = None) -> str:
    """
    Generate a unique ZeroMQ IPC path.
    
    Args:
        base_path: Base directory for IPC sockets.
    
    Returns:
        IPC URI string.
    """
    import tempfile
    if base_path is None:
        base_path = tempfile.gettempdir()
    return f"ipc://{base_path}/{uuid4()}"


def get_zmq_inproc_path() -> str:
    """Generate a unique ZeroMQ in-process path."""
    return f"inproc://{uuid4()}"


def close_zmq_sockets(sockets: Sequence[Any]) -> None:
    """
    Close ZeroMQ sockets with linger=0.
    
    Args:
        sockets: Sequence of ZMQ sockets to close.
    """
    if not HAS_ZMQ:
        return
    
    for sock in sockets:
        if sock is not None:
            with contextlib.suppress(Exception):
                sock.close(linger=0)


@contextlib.contextmanager
def zmq_socket_context(
    context: Any,
    socket_type: int,
    *,
    linger: int = 0
) -> Iterator[Any]:
    """
    Context manager for ZMQ sockets with automatic cleanup.
    
    Usage:
        >>> with zmq_socket_context(ctx, zmq.REQ) as sock:
        ...     sock.connect("tcp://localhost:5555")
    """
    if not HAS_ZMQ:
        raise RuntimeError("ZeroMQ is not installed")
    
    sock = context.socket(socket_type)
    try:
        yield sock
    finally:
        sock.close(linger=linger)


def create_zmq_context(io_threads: int = 1) -> Any:
    """
    Create a new ZeroMQ context.
    
    Args:
        io_threads: Number of I/O threads.
    
    Returns:
        zmq.Context instance.
    """
    if not HAS_ZMQ:
        raise RuntimeError("ZeroMQ is not installed")
    return zmq.Context(io_threads)


def create_async_zmq_context(io_threads: int = 1) -> Any:
    """
    Create a new async ZeroMQ context.
    
    Args:
        io_threads: Number of I/O threads.
    
    Returns:
        zmq.asyncio.Context instance.
    """
    if not HAS_ZMQ:
        raise RuntimeError("ZeroMQ is not installed")
    return zmq.asyncio.Context(io_threads)


# ============================================================================
# Network Interface Information
# ============================================================================


def get_network_interfaces() -> dict[str, list[str]]:
    """
    Get all network interfaces and their IP addresses.
    
    Requires psutil.
    
    Returns:
        Dictionary mapping interface names to list of IP addresses.
    """
    if not HAS_PSUTIL:
        logger.warning("psutil not installed, limited interface info")
        return {"default": [get_ip()]}
    
    result: dict[str, list[str]] = {}
    
    for iface, addrs in psutil.net_if_addrs().items():
        ips = []
        for addr in addrs:
            if addr.family in (socket.AF_INET, socket.AF_INET6):
                ips.append(addr.address)
        if ips:
            result[iface] = ips
    
    return result


def get_primary_interface() -> str | None:
    """
    Get the name of the primary network interface.
    
    Returns:
        Interface name or None if not determinable.
    """
    if not HAS_PSUTIL:
        return None
    
    # Get the interface used for default route
    with contextlib.suppress(Exception):
        import subprocess
        if sys.platform != "win32":
            result = subprocess.run(
                ["ip", "route", "get", "8.8.8.8"],
                capture_output=True,
                text=True,
            )
            for part in result.stdout.split():
                if part.startswith("dev"):
                    idx = result.stdout.split().index("dev")
                    return result.stdout.split()[idx + 1]
    
    return None


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # IP Detection
    "get_ip",
    "get_loopback_ip",
    "get_hostname",
    "get_fqdn",
    "resolve_hostname",
    "test_bind",
    # IP Validation
    "is_valid_ipv4_address",
    "is_valid_ipv6_address",
    "is_valid_ip_address",
    "normalize_ip",
    # Host:Port
    "split_host_port",
    "join_host_port",
    # Port Discovery
    "get_open_port",
    "get_open_ports",
    "is_port_open",
    "wait_for_port",
    "find_process_using_port",
    # URI Builders
    "get_tcp_uri",
    "get_distributed_init_method",
    "parse_uri",
    # ZMQ Utilities
    "get_zmq_ipc_path",
    "get_zmq_inproc_path",
    "close_zmq_sockets",
    "zmq_socket_context",
    "create_zmq_context",
    "create_async_zmq_context",
    "HAS_ZMQ",
    # Network Interfaces
    "get_network_interfaces",
    "get_primary_interface",
]
