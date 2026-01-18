"""
CircuitBreaker - Resilience pattern for failing gracefully.

Goes beyond vLLM with production-grade circuit breaker implementation
for protecting against cascading failures in distributed systems.

States:
- CLOSED: Normal operation, requests flow through
- OPEN: Failures exceeded threshold, requests rejected immediately
- HALF_OPEN: Testing if service recovered with limited requests

Phase 18: Beyond vLLM - Resilience Patterns
"""
from __future__ import annotations
import asyncio
import functools
import threading
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, TypeVar, ParamSpec, Any, Generic

P = ParamSpec('P')
R = TypeVar('R')
T = TypeVar('T')


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = auto()      # Normal operation
    OPEN = auto()        # Rejecting requests
    HALF_OPEN = auto()   # Testing recovery


@dataclass
class CircuitStats:
    """Statistics for circuit breaker monitoring."""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    rejected_calls: int = 0
    state_changes: int = 0
    last_failure_time: float | None = None
    last_success_time: float | None = None
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    
    @property
    def failure_rate(self) -> float:
        """Calculate failure rate."""
        if self.total_calls == 0:
            return 0.0
        return self.failed_calls / self.total_calls
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_calls == 0:
            return 0.0
        return self.successful_calls / self.total_calls
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'total_calls': self.total_calls,
            'successful_calls': self.successful_calls,
            'failed_calls': self.failed_calls,
            'rejected_calls': self.rejected_calls,
            'failure_rate': round(self.failure_rate, 4),
            'success_rate': round(self.success_rate, 4),
            'consecutive_failures': self.consecutive_failures,
            'consecutive_successes': self.consecutive_successes,
            'state_changes': self.state_changes,
        }


class CircuitBreakerError(Exception):
    """Raised when circuit is open."""
    def __init__(self, message: str, retry_after: float | None = None):
        super().__init__(message)
        self.retry_after = retry_after


class CircuitBreaker:
    """
    Thread-safe circuit breaker for protecting against cascading failures.
    
    Example:
        >>> breaker = CircuitBreaker(
        ...     failure_threshold=5,
        ...     recovery_timeout=30.0,
        ...     half_open_max_calls=3,
        ... )
        >>> 
        >>> @breaker
        ... def call_external_service():
        ...     return requests.get("http://api.example.com")
        >>> 
        >>> try:
        ...     result = call_external_service()
        ... except CircuitBreakerError as e:
        ...     print(f"Circuit open, retry after {e.retry_after}s")
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        half_open_max_calls: int = 3,
        failure_rate_threshold: float | None = None,
        success_threshold: int = 2,
        excluded_exceptions: tuple[type[Exception], ...] = (),
        name: str = "default",
    ) -> None:
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Consecutive failures to open circuit
            recovery_timeout: Seconds before attempting recovery
            half_open_max_calls: Max calls allowed in half-open state
            failure_rate_threshold: Optional failure rate threshold (0.0-1.0)
            success_threshold: Successes needed in half-open to close
            excluded_exceptions: Exceptions that don't count as failures
            name: Identifier for this circuit breaker
        """
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._half_open_max_calls = half_open_max_calls
        self._failure_rate_threshold = failure_rate_threshold
        self._success_threshold = success_threshold
        self._excluded_exceptions = excluded_exceptions
        self._name = name
        
        self._state = CircuitState.CLOSED
        self._stats = CircuitStats()
        self._lock = threading.RLock()
        self._opened_at: float | None = None
        self._half_open_calls = 0
        self._half_open_successes = 0
        
        # Callbacks
        self._on_open: list[Callable[[], None]] = []
        self._on_close: list[Callable[[], None]] = []
        self._on_half_open: list[Callable[[], None]] = []
    
    @property
    def state(self) -> CircuitState:
        """Get current state."""
        with self._lock:
            self._check_state_transition()
            return self._state
    
    @property
    def stats(self) -> CircuitStats:
        """Get statistics."""
        return self._stats
    
    @property
    def is_closed(self) -> bool:
        """Check if circuit is closed (normal operation)."""
        return self.state == CircuitState.CLOSED
    
    @property
    def is_open(self) -> bool:
        """Check if circuit is open (rejecting requests)."""
        return self.state == CircuitState.OPEN
    
    def _check_state_transition(self) -> None:
        """Check if state should transition based on timeout."""
        if self._state == CircuitState.OPEN and self._opened_at:
            elapsed = time.monotonic() - self._opened_at
            if elapsed >= self._recovery_timeout:
                self._transition_to(CircuitState.HALF_OPEN)
    
    def _transition_to(self, new_state: CircuitState) -> None:
        """Transition to a new state."""
        if self._state == new_state:
            return
        
        old_state = self._state
        self._state = new_state
        self._stats.state_changes += 1
        
        if new_state == CircuitState.OPEN:
            self._opened_at = time.monotonic()
            for callback in self._on_open:
                try:
                    callback()
                except Exception:
                    pass
        
        elif new_state == CircuitState.HALF_OPEN:
            self._half_open_calls = 0
            self._half_open_successes = 0
            for callback in self._on_half_open:
                try:
                    callback()
                except Exception:
                    pass
        
        elif new_state == CircuitState.CLOSED:
            self._opened_at = None
            self._stats.consecutive_failures = 0
            for callback in self._on_close:
                try:
                    callback()
                except Exception:
                    pass
    
    def _should_allow_request(self) -> bool:
        """Check if request should be allowed."""
        with self._lock:
            self._check_state_transition()
            
            if self._state == CircuitState.CLOSED:
                return True
            
            if self._state == CircuitState.OPEN:
                return False
            
            # HALF_OPEN: Allow limited requests
            if self._half_open_calls < self._half_open_max_calls:
                self._half_open_calls += 1
                return True
            
            return False
    
    def _record_success(self) -> None:
        """Record a successful call."""
        with self._lock:
            self._stats.total_calls += 1
            self._stats.successful_calls += 1
            self._stats.last_success_time = time.monotonic()
            self._stats.consecutive_successes += 1
            self._stats.consecutive_failures = 0
            
            if self._state == CircuitState.HALF_OPEN:
                self._half_open_successes += 1
                if self._half_open_successes >= self._success_threshold:
                    self._transition_to(CircuitState.CLOSED)
    
    def _record_failure(self) -> None:
        """Record a failed call."""
        with self._lock:
            self._stats.total_calls += 1
            self._stats.failed_calls += 1
            self._stats.last_failure_time = time.monotonic()
            self._stats.consecutive_failures += 1
            self._stats.consecutive_successes = 0
            
            if self._state == CircuitState.HALF_OPEN:
                # Any failure in half-open reopens circuit
                self._transition_to(CircuitState.OPEN)
            
            elif self._state == CircuitState.CLOSED:
                # Check if we should open
                should_open = False
                
                if self._stats.consecutive_failures >= self._failure_threshold:
                    should_open = True
                
                if (self._failure_rate_threshold and 
                    self._stats.total_calls >= 10 and
                    self._stats.failure_rate >= self._failure_rate_threshold):
                    should_open = True
                
                if should_open:
                    self._transition_to(CircuitState.OPEN)
    
    def _get_retry_after(self) -> float | None:
        """Get seconds until retry is possible."""
        if self._state != CircuitState.OPEN or not self._opened_at:
            return None
        
        elapsed = time.monotonic() - self._opened_at
        remaining = self._recovery_timeout - elapsed
        return max(0.0, remaining)
    
    def call(self, func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
        """
        Execute a function through the circuit breaker.
        
        Args:
            func: Function to call
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result
            
        Raises:
            CircuitBreakerError: If circuit is open
        """
        if not self._should_allow_request():
            self._stats.rejected_calls += 1
            raise CircuitBreakerError(
                f"Circuit breaker '{self._name}' is OPEN",
                retry_after=self._get_retry_after(),
            )
        
        try:
            result = func(*args, **kwargs)
            self._record_success()
            return result
        except self._excluded_exceptions:
            # Don't count excluded exceptions as failures
            self._record_success()
            raise
        except Exception:
            self._record_failure()
            raise
    
    async def call_async(
        self, 
        func: Callable[P, Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Any:
        """
        Execute an async function through the circuit breaker.
        """
        if not self._should_allow_request():
            self._stats.rejected_calls += 1
            raise CircuitBreakerError(
                f"Circuit breaker '{self._name}' is OPEN",
                retry_after=self._get_retry_after(),
            )
        
        try:
            result = await func(*args, **kwargs)
            self._record_success()
            return result
        except self._excluded_exceptions:
            self._record_success()
            raise
        except Exception:
            self._record_failure()
            raise
    
    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        """Decorator for wrapping functions with circuit breaker."""
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                return await self.call_async(func, *args, **kwargs)
            return async_wrapper  # type: ignore
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                return self.call(func, *args, **kwargs)
            return sync_wrapper
    
    def on_open(self, callback: Callable[[], None]) -> None:
        """Register callback for when circuit opens."""
        self._on_open.append(callback)
    
    def on_close(self, callback: Callable[[], None]) -> None:
        """Register callback for when circuit closes."""
        self._on_close.append(callback)
    
    def on_half_open(self, callback: Callable[[], None]) -> None:
        """Register callback for when circuit enters half-open."""
        self._on_half_open.append(callback)
    
    def reset(self) -> None:
        """Manually reset circuit to closed state."""
        with self._lock:
            self._transition_to(CircuitState.CLOSED)
            self._stats = CircuitStats()


class CircuitBreakerRegistry:
    """
    Registry for managing multiple circuit breakers.
    
    Example:
        >>> registry = CircuitBreakerRegistry()
        >>> 
        >>> @registry.breaker("openai_api")
        ... def call_openai(prompt):
        ...     return openai.chat(prompt)
        >>> 
        >>> print(registry.get_all_stats())
    """
    
    def __init__(self) -> None:
        self._breakers: dict[str, CircuitBreaker] = {}
        self._lock = threading.Lock()
    
    def get_or_create(
        self,
        name: str,
        **kwargs: Any,
    ) -> CircuitBreaker:
        """Get existing or create new circuit breaker."""
        with self._lock:
            if name not in self._breakers:
                self._breakers[name] = CircuitBreaker(name=name, **kwargs)
            return self._breakers[name]
    
    def breaker(
        self,
        name: str,
        **kwargs: Any,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        """Decorator to wrap function with named circuit breaker."""
        cb = self.get_or_create(name, **kwargs)
        return cb
    
    def get_stats(self, name: str) -> dict | None:
        """Get stats for a specific circuit breaker."""
        cb = self._breakers.get(name)
        if cb:
            return cb.stats.to_dict()
        return None
    
    def get_all_stats(self) -> dict[str, dict]:
        """Get stats for all circuit breakers."""
        return {
            name: cb.stats.to_dict()
            for name, cb in self._breakers.items()
        }
    
    def reset_all(self) -> None:
        """Reset all circuit breakers."""
        for cb in self._breakers.values():
            cb.reset()


# Global registry
_global_registry = CircuitBreakerRegistry()


def circuit_breaker(
    name: str = "default",
    **kwargs: Any,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to protect a function with a circuit breaker.
    
    Example:
        >>> @circuit_breaker("external_api", failure_threshold=3)
        ... def call_api():
        ...     return requests.get("http://api.example.com")
    """
    return _global_registry.breaker(name, **kwargs)


def get_circuit_stats(name: str) -> dict | None:
    """Get stats for a circuit breaker."""
    return _global_registry.get_stats(name)


def get_all_circuit_stats() -> dict[str, dict]:
    """Get stats for all circuit breakers."""
    return _global_registry.get_all_stats()


__all__ = [
    'CircuitState',
    'CircuitStats',
    'CircuitBreakerError',
    'CircuitBreaker',
    'CircuitBreakerRegistry',
    'circuit_breaker',
    'get_circuit_stats',
    'get_all_circuit_stats',
]
