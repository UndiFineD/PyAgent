"""
Generic Connection Pool for database and HTTP connections.

Phase 19: Beyond vLLM - Performance Patterns
Connection pooling to reduce connection overhead.
"""
from __future__ import annotations

import threading
import time
import weakref
import contextlib
from abc import ABC, abstractmethod
from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Protocol,
    Set,
    TypeVar,
    runtime_checkable,
)

T = TypeVar('T')


class ConnectionState(Enum):
    """State of a pooled connection."""
    IDLE = auto()
    IN_USE = auto()
    STALE = auto()
    CLOSED = auto()


@runtime_checkable
class Closeable(Protocol):
    """Protocol for closeable resources."""

    def close(self) -> None:
        """Close the resource."""
        ...


@runtime_checkable
class Pingable(Protocol):
    """Protocol for resources that can be health-checked."""

    def ping(self) -> bool:
        """Check if resource is healthy."""
        ...


@dataclass
class PoolStats:
    """Statistics for connection pool."""
    created: int = 0
    reused: int = 0
    closed: int = 0
    failed_creates: int = 0
    failed_health_checks: int = 0
    timeouts: int = 0
    current_idle: int = 0
    current_in_use: int = 0
    peak_in_use: int = 0
    total_wait_time_ms: float = 0.0
    total_use_time_ms: float = 0.0

    @property
    def total_connections(self) -> int:
        """Total connections (idle + in use)."""
        return self.current_idle + self.current_in_use

    @property
    def reuse_ratio(self) -> float:
        """Ratio of reused vs created."""
        total = self.created + self.reused
        return self.reused / total if total > 0 else 0.0

    @property
    def avg_wait_time_ms(self) -> float:
        """Average wait time for connection."""
        total = self.created + self.reused
        return self.total_wait_time_ms / total if total > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'created': self.created,
            'reused': self.reused,
            'closed': self.closed,
            'failed_creates': self.failed_creates,
            'failed_health_checks': self.failed_health_checks,
            'timeouts': self.timeouts,
            'current_idle': self.current_idle,
            'current_in_use': self.current_in_use,
            'peak_in_use': self.peak_in_use,
            'total_connections': self.total_connections,
            'reuse_ratio': self.reuse_ratio,
            'avg_wait_time_ms': self.avg_wait_time_ms,
        }


@dataclass(eq=False)
class PooledConnection(Generic[T]):
    """Wrapper for a pooled connection."""
    connection: T
    created_at: float
    last_used_at: float
    use_count: int = 0
    state: ConnectionState = ConnectionState.IDLE

    @property
    def age_seconds(self) -> float:
        """Age of connection in seconds."""
        return time.monotonic() - self.created_at

    @property
    def idle_seconds(self) -> float:
        """Time since last use in seconds."""
        return time.monotonic() - self.last_used_at


class ConnectionPool(Generic[T]):
    """
    Generic connection pool with health checking.

    Features:
    - Configurable min/max connections
    - Health checking with ping
    - Connection aging and rotation
    - Wait timeout for busy pool
    - Statistics tracking

    Example:
        pool = ConnectionPool(
            factory=lambda: create_connection(),
            min_size=5,
            max_size=20,
        )

        with pool.acquire() as conn:
            conn.execute("SELECT 1")
    """

    def __init__(
        self,
        factory: Callable[[], T],
        min_size: int = 1,
        max_size: int = 10,
        max_idle_seconds: float = 300.0,
        max_lifetime_seconds: float = 3600.0,
        acquire_timeout_seconds: float = 30.0,
        health_check_interval: float = 30.0,
        validate_on_acquire: bool = True,
    ):
        """
        Initialize connection pool.

        Args:
            factory: Function to create new connections
            min_size: Minimum pool size
            max_size: Maximum pool size
            max_idle_seconds: Close connections idle longer than this
            max_lifetime_seconds: Close connections older than this
            acquire_timeout_seconds: Max time to wait for connection
            health_check_interval: Seconds between health checks
            validate_on_acquire: Validate connection before returning
        """
        self._factory = factory
        self._min_size = min_size
        self._max_size = max_size
        self._max_idle_seconds = max_idle_seconds
        self._max_lifetime_seconds = max_lifetime_seconds
        self._acquire_timeout = acquire_timeout_seconds
        self._health_check_interval = health_check_interval
        self._validate_on_acquire = validate_on_acquire

        self._idle: deque[PooledConnection[T]] = deque()
        self._in_use: Set[PooledConnection[T]] = set()

        self._lock = threading.Lock()
        self._available = threading.Condition(self._lock)

        self._stats = PoolStats()
        self._closed = False

        # Pre-populate pool
        self._warm_pool()

    def _warm_pool(self) -> None:
        """Pre-populate pool to minimum size."""
        for _ in range(self._min_size):
            try:
                conn = self._create_connection()
                if conn:
                    self._idle.append(conn)
                    self._stats.current_idle += 1
            except Exception:
                self._stats.failed_creates += 1

    def _create_connection(self) -> Optional[PooledConnection[T]]:
        """Create a new pooled connection."""
        try:
            now = time.monotonic()
            raw = self._factory()
            self._stats.created += 1

            return PooledConnection(
                connection=raw,
                created_at=now,
                last_used_at=now,
                state=ConnectionState.IDLE,
            )
        except Exception:
            self._stats.failed_creates += 1
            raise

    def _validate_connection(self, pooled: PooledConnection[T]) -> bool:
        """Validate a connection is healthy."""
        # Check age
        if pooled.age_seconds > self._max_lifetime_seconds:
            return False

        # Check idle time
        if pooled.idle_seconds > self._max_idle_seconds:
            return False

        # Ping if supported
        conn = pooled.connection
        if isinstance(conn, Pingable):
            try:
                if not conn.ping():
                    self._stats.failed_health_checks += 1
                    return False
            except Exception:
                self._stats.failed_health_checks += 1
                return False

        return True

    def _close_connection(self, pooled: PooledConnection[T]) -> None:
        """Close a pooled connection."""
        pooled.state = ConnectionState.CLOSED
        conn = pooled.connection

        if isinstance(conn, Closeable):
            try:
                conn.close()
            except Exception:
                pass

        self._stats.closed += 1

    def acquire(self, timeout: Optional[float] = None) -> T:
        """
        Acquire a connection from the pool.

        Args:
            timeout: Max seconds to wait (uses default if None)

        Returns:
            Connection from pool

        Raises:
            TimeoutError: If no connection available within timeout
        """
        if timeout is None:
            timeout = self._acquire_timeout

        start = time.monotonic()
        deadline = start + timeout

        with self._available:
            while True:
                if self._closed:
                    raise RuntimeError("Pool is closed")

                # Try to get from idle pool
                while self._idle:
                    pooled = self._idle.popleft()
                    self._stats.current_idle -= 1

                    # Validate if required
                    if self._validate_on_acquire and not self._validate_connection(pooled):
                        self._close_connection(pooled)
                        continue

                    # Mark as in use
                    pooled.state = ConnectionState.IN_USE
                    pooled.last_used_at = time.monotonic()
                    pooled.use_count += 1

                    self._in_use.add(pooled)
                    self._stats.current_in_use += 1
                    self._stats.reused += 1
                    self._stats.peak_in_use = max(
                        self._stats.peak_in_use,
                        self._stats.current_in_use,
                    )

                    wait_time = (time.monotonic() - start) * 1000
                    self._stats.total_wait_time_ms += wait_time

                    return pooled.connection

                # Try to create new connection if under max
                total = self._stats.current_idle + self._stats.current_in_use
                if total < self._max_size:
                    with contextlib.suppress(Exception):
                        pooled = self._create_connection()
                        if pooled:
                            pooled.state = ConnectionState.IN_USE
                            pooled.use_count = 1

                            self._in_use.add(pooled)
                            self._stats.current_in_use += 1
                            self._stats.peak_in_use = max(
                                self._stats.peak_in_use,
                                self._stats.current_in_use,
                            )

                            wait_time = (time.monotonic() - start) * 1000
                            self._stats.total_wait_time_ms += wait_time

                            return pooled.connection

                # Wait for a connection to be released
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    self._stats.timeouts += 1
                    raise TimeoutError("Timed out waiting for connection")

                self._available.wait(timeout=remaining)

    def release(self, connection: T) -> None:
        """
        Return a connection to the pool.

        Args:
            connection: Connection to return
        """
        with self._available:
            # Find the pooled connection
            pooled = None
            for p in self._in_use:
                if p.connection is connection:
                    pooled = p
                    break

            if pooled is None:
                return  # Unknown connection

            self._in_use.remove(pooled)
            self._stats.current_in_use -= 1

            # Check if still valid
            if self._validate_connection(pooled):
                pooled.state = ConnectionState.IDLE
                pooled.last_used_at = time.monotonic()
                self._idle.append(pooled)
                self._stats.current_idle += 1
            else:
                self._close_connection(pooled)

            self._available.notify()

    @contextmanager
    def connection(self, timeout: Optional[float] = None):
        """
        Context manager for acquiring a connection.

        Yields:
            Connection from pool (automatically returned)
        """
        conn = self.acquire(timeout)
        try:
            yield conn
        finally:
            self.release(conn)

    def close(self) -> None:
        """Close all connections and the pool."""
        with self._available:
            self._closed = True

            # Close idle connections
            while self._idle:
                pooled = self._idle.popleft()
                self._close_connection(pooled)
                self._stats.current_idle -= 1

            # Close in-use connections (if any)
            for pooled in list(self._in_use):
                self._close_connection(pooled)

            self._in_use.clear()
            self._stats.current_in_use = 0

            self._available.notify_all()

    def prune(self) -> int:
        """
        Remove stale connections from the pool.

        Returns:
            Number of connections removed
        """
        removed = 0

        with self._lock:
            new_idle: deque[PooledConnection[T]] = deque()

            while self._idle:
                pooled = self._idle.popleft()

                if self._validate_connection(pooled):
                    new_idle.append(pooled)
                else:
                    self._close_connection(pooled)
                    removed += 1

            self._idle = new_idle
            self._stats.current_idle = len(self._idle)

        return removed

    @property
    def size(self) -> int:
        """Total pool size (idle + in use)."""
        return self._stats.current_idle + self._stats.current_in_use

    @property
    def idle_count(self) -> int:
        """Number of idle connections."""
        return self._stats.current_idle

    @property
    def in_use_count(self) -> int:
        """Number of connections in use."""
        return self._stats.current_in_use

    @property
    def stats(self) -> PoolStats:
        """Pool statistics."""
        return self._stats

    def __enter__(self) -> 'ConnectionPool[T]':
        """Enter context."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context and close pool."""
        self.close()


class AsyncConnectionPool(Generic[T]):
    """
    Async connection pool using asyncio.
    """

    def __init__(
        self,
        factory: Callable[[], T],
        min_size: int = 1,
        max_size: int = 10,
        acquire_timeout: float = 30.0,
    ):
        """Initialize async connection pool."""
        import asyncio

        self._factory = factory
        self._min_size = min_size
        self._max_size = max_size
        self._acquire_timeout = acquire_timeout

        self._idle: deque[PooledConnection[T]] = deque()
        self._semaphore = asyncio.Semaphore(max_size)
        self._lock = asyncio.Lock()
        self._stats = PoolStats()

    async def acquire(self) -> T:
        """Acquire connection asynchronously."""
        import asyncio

        await asyncio.wait_for(
            self._semaphore.acquire(),
            timeout=self._acquire_timeout,
        )

        async with self._lock:
            if self._idle:
                pooled = self._idle.popleft()
                pooled.state = ConnectionState.IN_USE
                pooled.use_count += 1
                self._stats.reused += 1
                return pooled.connection

            # Create new
            now = time.monotonic()
            raw = self._factory()
            self._stats.created += 1

            return raw

    async def release(self, connection: T) -> None:
        """Release connection asynchronously."""
        async with self._lock:
            now = time.monotonic()
            pooled = PooledConnection(
                connection=connection,
                created_at=now,
                last_used_at=now,
            )
            self._idle.append(pooled)

        self._semaphore.release()

    @property
    def stats(self) -> PoolStats:
        """Pool statistics."""
        return self._stats


class PooledConnectionManager(Generic[T]):
    """
    Context manager wrapper that auto-releases connection.
    """

    def __init__(self, pool: ConnectionPool[T], connection: T):
        """Initialize with pool and connection."""
        self._pool = pool
        self._connection = connection

    def __enter__(self) -> T:
        """Return the connection."""
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Release connection back to pool."""
        self._pool.release(self._connection)


class MultiHostPool(Generic[T]):
    """
    Connection pool across multiple hosts with load balancing.
    """

    def __init__(
        self,
        hosts: List[str],
        factory: Callable[[str], T],
        connections_per_host: int = 5,
    ):
        """
        Initialize multi-host pool.

        Args:
            hosts: List of host addresses
            factory: Factory that takes host and returns connection
            connections_per_host: Connections per host
        """
        self._hosts = hosts
        self._pools: Dict[str, ConnectionPool[T]] = {}
        self._round_robin_index = 0
        self._lock = threading.Lock()

        for host in hosts:
            self._pools[host] = ConnectionPool(
                factory=lambda h=host: factory(h),
                max_size=connections_per_host,
            )

    def acquire(self, host: Optional[str] = None) -> tuple[str, T]:
        """
        Acquire connection, optionally from specific host.

        Args:
            host: Specific host, or None for round-robin

        Returns:
            Tuple of (host, connection)
        """
        if host is None:
            with self._lock:
                host = self._hosts[self._round_robin_index % len(self._hosts)]
                self._round_robin_index += 1

        conn = self._pools[host].acquire()
        return (host, conn)

    def release(self, host: str, connection: T) -> None:
        """Release connection to specific host pool."""
        self._pools[host].release(connection)

    @contextmanager
    def connection(self, host: Optional[str] = None):
        """Get connection with auto-release."""
        h, conn = self.acquire(host)
        try:
            yield conn
        finally:
            self.release(h, conn)

    def close(self) -> None:
        """Close all pools."""
        for pool in self._pools.values():
            pool.close()

    def get_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get stats for all hosts."""
        return {
            host: pool.stats.to_dict()
            for host, pool in self._pools.items()
        }
