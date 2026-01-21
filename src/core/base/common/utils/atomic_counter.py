"""
AtomicCounter - Thread-safe counter with Rust acceleration.

Inspired by vLLM's counter.py patterns for high-frequency atomic operations.

Phase 17: vLLM Pattern Integration
"""
from __future__ import annotations
import threading
from typing import Optional

# Rust acceleration imports
try:
    from rust_core import rust_core as rc
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False


class Counter:
    """
    Simple non-atomic counter for single-threaded use.
    
    Use AtomicCounter for multi-threaded scenarios.
    """
    
    __slots__ = ('_value',)
    
    def __init__(self, start: int = 0) -> None:
        self._value = start
    
    @property
    def value(self) -> int:
        """Current counter value."""
        return self._value
    
    def inc(self, delta: int = 1) -> int:
        """Increment and return the new value."""
        self._value += delta
        return self._value
    
    def dec(self, delta: int = 1) -> int:
        """Decrement and return the new value."""
        self._value -= delta
        return self._value
    
    def reset(self, value: int = 0) -> int:
        """Reset to a value and return the old value."""
        old = self._value
        self._value = value
        return old
    
    def __repr__(self) -> str:
        return f"Counter({self._value})"


class AtomicCounter:
    """
    Thread-safe atomic counter.
    
    Uses a lock internally for thread safety. For extremely high-frequency
    operations, consider using Rust-accelerated atomic operations.
    
    Example:
        >>> counter = AtomicCounter()
        >>> counter.inc()
        1
        >>> counter.inc(5)
        6
        >>> counter.value
        6
    """
    
    __slots__ = ('_value', '_lock', '_use_rust')
    
    def __init__(self, start: int = 0, use_rust: bool = True) -> None:
        """
        Initialize atomic counter.
        
        Args:
            start: Initial value
            use_rust: Whether to use Rust acceleration if available
        """
        self._value = start
        self._lock = threading.Lock()
        self._use_rust = use_rust and RUST_AVAILABLE
    
    @property
    def value(self) -> int:
        """Current counter value (atomic read)."""
        with self._lock:
            return self._value
    
    def inc(self, delta: int = 1) -> int:
        """
        Atomically increment the counter.
        
        Args:
            delta: Amount to increment by
            
        Returns:
            New counter value
        """
        if self._use_rust and hasattr(rc, 'atomic_counter_add_rust'):
            # Rust atomic operation
            with self._lock:
                self._value = rc.atomic_counter_add_rust(self._value, delta)
                return self._value
        
        with self._lock:
            self._value += delta
            return self._value
    
    def dec(self, delta: int = 1) -> int:
        """
        Atomically decrement the counter.
        
        Args:
            delta: Amount to decrement by
            
        Returns:
            New counter value
        """
        return self.inc(-delta)
    
    def add(self, delta: int) -> int:
        """Alias for inc()."""
        return self.inc(delta)
    
    def sub(self, delta: int) -> int:
        """Alias for dec()."""
        return self.dec(delta)
    
    def reset(self, value: int = 0) -> int:
        """
        Atomically reset the counter.
        
        Args:
            value: New value to set
            
        Returns:
            Old counter value
        """
        with self._lock:
            old = self._value
            self._value = value
            return old
    
    def compare_and_swap(self, expected: int, new_value: int) -> bool:
        """
        Atomically compare and swap.
        
        Args:
            expected: Expected current value
            new_value: New value to set if current matches expected
            
        Returns:
            True if swap occurred, False otherwise
        """
        with self._lock:
            if self._value == expected:
                self._value = new_value
                return True
            return False
    
    def get_and_reset(self) -> int:
        """
        Atomically get the current value and reset to 0.
        
        Useful for collecting metrics.
        
        Returns:
            Value before reset
        """
        return self.reset(0)
    
    def __repr__(self) -> str:
        return f"AtomicCounter({self.value})"
    
    def __int__(self) -> int:
        return self.value
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, (int, AtomicCounter, Counter)):
            return self.value == (other.value if hasattr(other, 'value') else other)
        return NotImplemented


class AtomicFlag:
    """
    Thread-safe atomic boolean flag.
    
    Useful for signaling between threads.
    """
    
    __slots__ = ('_flag', '_lock')
    
    def __init__(self, initial: bool = False) -> None:
        self._flag = initial
        self._lock = threading.Lock()
    
    @property
    def value(self) -> bool:
        """Current flag value."""
        with self._lock:
            return self._flag
    
    def set(self) -> bool:
        """Set the flag to True. Returns the old value."""
        with self._lock:
            old = self._flag
            self._flag = True
            return old
    
    def clear(self) -> bool:
        """Set the flag to False. Returns the old value."""
        with self._lock:
            old = self._flag
            self._flag = False
            return old
    
    def toggle(self) -> bool:
        """Toggle the flag. Returns the new value."""
        with self._lock:
            self._flag = not self._flag
            return self._flag
    
    def test_and_set(self) -> bool:
        """Atomically test if flag was False and set it to True."""
        with self._lock:
            if not self._flag:
                self._flag = True
                return True
            return False
    
    def __bool__(self) -> bool:
        return self.value
    
    def __repr__(self) -> str:
        return f"AtomicFlag({self.value})"


class AtomicGauge:
    """
    Thread-safe gauge that tracks min, max, and current value.
    
    Useful for monitoring metrics that can go up and down.
    """
    
    __slots__ = ('_value', '_min', '_max', '_lock')
    
    def __init__(self, initial: float = 0.0) -> None:
        self._value = initial
        self._min = initial
        self._max = initial
        self._lock = threading.Lock()
    
    @property
    def value(self) -> float:
        """Current gauge value."""
        with self._lock:
            return self._value
    
    @property
    def min(self) -> float:
        """Minimum observed value."""
        with self._lock:
            return self._min
    
    @property
    def max(self) -> float:
        """Maximum observed value."""
        with self._lock:
            return self._max
    
    def set(self, value: float) -> None:
        """Set the gauge value and update min/max."""
        with self._lock:
            self._value = value
            if value < self._min:
                self._min = value
            if value > self._max:
                self._max = value
    
    def inc(self, delta: float = 1.0) -> float:
        """Increment and return new value."""
        with self._lock:
            self._value += delta
            if self._value > self._max:
                self._max = self._value
            return self._value
    
    def dec(self, delta: float = 1.0) -> float:
        """Decrement and return new value."""
        with self._lock:
            self._value -= delta
            if self._value < self._min:
                self._min = self._value
            return self._value
    
    def snapshot(self) -> dict:
        """Get a snapshot of current, min, max values."""
        with self._lock:
            return {
                'value': self._value,
                'min': self._min,
                'max': self._max,
            }
    
    def reset(self, value: float = 0.0) -> dict:
        """Reset and return previous snapshot."""
        with self._lock:
            snapshot = {
                'value': self._value,
                'min': self._min,
                'max': self._max,
            }
            self._value = value
            self._min = value
            self._max = value
            return snapshot
    
    def __repr__(self) -> str:
        snap = self.snapshot()
        return f"AtomicGauge(value={snap['value']}, min={snap['min']}, max={snap['max']})"


__all__ = [
    'Counter',
    'AtomicCounter',
    'AtomicFlag',
    'AtomicGauge',
    'RUST_AVAILABLE',
]
