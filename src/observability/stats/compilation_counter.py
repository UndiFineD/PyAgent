"""
CompilationCounter - Statistics and counters for compilation metrics.

Implements vLLM's compilation counting patterns:
- Track compilation events
- Monitor recompilation rates
- Shape distribution analysis
- Backend performance tracking

Beyond vLLM:
- Real-time metrics emission
- Anomaly detection
- Trend analysis
"""

from __future__ import annotations

import logging
import threading
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


class CompileEventType(Enum):
    """Types of compilation events."""
    COMPILE = auto()          # Initial compilation
    RECOMPILE = auto()        # Recompilation due to shape change
    CACHE_HIT = auto()        # Compilation cache hit
    FALLBACK = auto()         # Fallback to eager
    ERROR = auto()            # Compilation error


@dataclass
class CompileEvent:
    """A compilation event."""
    event_type: CompileEventType
    timestamp: float
    function_id: int
    shape: Tuple[int, ...]
    duration: float = 0.0
    backend: str = "inductor"
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "event_type": self.event_type.name,
            "timestamp": self.timestamp,
            "function_id": self.function_id,
            "shape": self.shape,
            "duration": self.duration,
            "backend": self.backend,
            "error": self.error
        }


@dataclass
class FunctionStats:
    """Statistics for a single function."""
    function_id: int
    compile_count: int = 0
    recompile_count: int = 0
    cache_hits: int = 0
    fallbacks: int = 0
    errors: int = 0
    total_compile_time: float = 0.0
    shapes_seen: Set[Tuple[int, ...]] = field(default_factory=set)
    last_compiled: float = 0.0

    @property
    def unique_shapes(self) -> int:
        """Number of unique shapes."""
        return len(self.shapes_seen)

    @property
    def avg_compile_time(self) -> float:
        """Average compilation time."""
        total = self.compile_count + self.recompile_count
        if total == 0:
            return 0.0
        return self.total_compile_time / total

    @property
    def recompile_ratio(self) -> float:
        """Ratio of recompiles to compiles."""
        if self.compile_count == 0:
            return 0.0
        return self.recompile_count / self.compile_count


class CompilationCounter:
    """
    Counter for tracking compilation statistics.

    Based on vLLM's compilation counter pattern.
    """

    def __init__(
        self,
        name: str = "default",
        max_events: int = 10000,
        emit_interval: float = 60.0
    ):
        """
        Initialize counter.

        Args:
            name: Counter name for identification
            max_events: Maximum events to keep
            emit_interval: Interval for metric emission (seconds)
        """
        self.name = name
        self.max_events = max_events
        self.emit_interval = emit_interval

        self._events: List[CompileEvent] = []
        self._function_stats: Dict[int, FunctionStats] = {}
        self._lock = threading.Lock()

        # Aggregate counters
        self._total_compiles = 0
        self._total_recompiles = 0
        self._total_cache_hits = 0
        self._total_fallbacks = 0
        self._total_errors = 0

        # Timing
        self._last_emit = time.time()

    def record_compile(
        self,
        function_id: int,
        shape: Tuple[int, ...],
        duration: float,
        backend: str = "inductor"
    ) -> None:
        """
        Record a compilation event.

        Args:
            function_id: ID of compiled function
            shape: Input shape
            duration: Compilation time
            backend: Compilation backend
        """
        event = CompileEvent(
            event_type=CompileEventType.COMPILE,
            timestamp=time.time(),
            function_id=function_id,
            shape=shape,
            duration=duration,
            backend=backend
        )

        with self._lock:
            self._add_event(event)
            self._total_compiles += 1

            stats = self._get_or_create_stats(function_id)
            stats.compile_count += 1
            stats.total_compile_time += duration
            stats.shapes_seen.add(shape)
            stats.last_compiled = time.time()

    def record_recompile(
        self,
        function_id: int,
        shape: Tuple[int, ...],
        duration: float,
        backend: str = "inductor"
    ) -> None:
        """Record a recompilation event."""
        event = CompileEvent(
            event_type=CompileEventType.RECOMPILE,
            timestamp=time.time(),
            function_id=function_id,
            shape=shape,
            duration=duration,
            backend=backend
        )

        with self._lock:
            self._add_event(event)
            self._total_recompiles += 1

            stats = self._get_or_create_stats(function_id)
            stats.recompile_count += 1
            stats.total_compile_time += duration
            stats.shapes_seen.add(shape)

    def record_cache_hit(self, function_id: int, shape: Tuple[int, ...]) -> None:
        """Record a cache hit."""
        event = CompileEvent(
            event_type=CompileEventType.CACHE_HIT,
            timestamp=time.time(),
            function_id=function_id,
            shape=shape
        )

        with self._lock:
            self._add_event(event)
            self._total_cache_hits += 1

            stats = self._get_or_create_stats(function_id)
            stats.cache_hits += 1

    def record_fallback(
        self,
        function_id: int,
        shape: Tuple[int, ...],
        reason: str = ""
    ) -> None:
        """Record a fallback to eager execution."""
        event = CompileEvent(
            event_type=CompileEventType.FALLBACK,
            timestamp=time.time(),
            function_id=function_id,
            shape=shape,
            error=reason
        )

        with self._lock:
            self._add_event(event)
            self._total_fallbacks += 1

            stats = self._get_or_create_stats(function_id)
            stats.fallbacks += 1

    def record_error(
        self,
        function_id: int,
        shape: Tuple[int, ...],
        error: str
    ) -> None:
        """Record a compilation error."""
        event = CompileEvent(
            event_type=CompileEventType.ERROR,
            timestamp=time.time(),
            function_id=function_id,
            shape=shape,
            error=error
        )

        with self._lock:
            self._add_event(event)
            self._total_errors += 1

            stats = self._get_or_create_stats(function_id)
            stats.errors += 1

    def _add_event(self, event: CompileEvent) -> None:
        """Add event with size limit."""
        self._events.append(event)
        if len(self._events) > self.max_events:
            self._events = self._events[-self.max_events:]

    def _get_or_create_stats(self, function_id: int) -> FunctionStats:
        """Get or create function stats."""
        if function_id not in self._function_stats:
            self._function_stats[function_id] = FunctionStats(function_id=function_id)
        return self._function_stats[function_id]

    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        with self._lock:
            total = (
                self._total_compiles +
                self._total_recompiles +
                self._total_cache_hits
            )

            return {
                "name": self.name,
                "total_compiles": self._total_compiles,
                "total_recompiles": self._total_recompiles,
                "total_cache_hits": self._total_cache_hits,
                "total_fallbacks": self._total_fallbacks,
                "total_errors": self._total_errors,
                "cache_hit_rate": self._total_cache_hits / total if total > 0 else 0,
                "functions_tracked": len(self._function_stats),
                "events_recorded": len(self._events)
            }

    def get_function_stats(self, function_id: int) -> Optional[FunctionStats]:
        """Get stats for a specific function."""
        with self._lock:
            return self._function_stats.get(function_id)

    def get_all_function_stats(self) -> List[FunctionStats]:
        """Get stats for all functions."""
        with self._lock:
            return list(self._function_stats.values())

    def get_shape_distribution(self) -> Dict[Tuple[int, ...], int]:
        """Get distribution of shapes across all compilations."""
        with self._lock:
            counter: Counter[Tuple[int, ...]] = Counter()
            for event in self._events:
                if event.event_type in (
                    CompileEventType.COMPILE,
                    CompileEventType.RECOMPILE
                ):
                    counter[event.shape] += 1
            return dict(counter)

    def should_emit_metrics(self) -> bool:
        """Check if metrics should be emitted."""
        return time.time() - self._last_emit >= self.emit_interval

    def emit_metrics(self) -> Dict[str, Any]:
        """Emit metrics and reset timer."""
        with self._lock:
            self._last_emit = time.time()
            return self.get_summary()

    def reset(self) -> None:
        """Reset all counters."""
        with self._lock:
            self._events.clear()
            self._function_stats.clear()
            self._total_compiles = 0
            self._total_recompiles = 0
            self._total_cache_hits = 0
            self._total_fallbacks = 0
            self._total_errors = 0


class RecompileTracker(CompilationCounter):
    """
    Specialized tracker for recompilation.

    Beyond vLLM:
    - Detects excessive recompilation
    - Suggests optimization strategies
    """

    def __init__(
        self,
        max_recompiles: int = 10,
        alert_threshold: float = 0.5,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.max_recompiles = max_recompiles
        self.alert_threshold = alert_threshold
        self._alerts: List[Dict[str, Any]] = []

    def record_recompile(
        self,
        function_id: int,
        shape: Tuple[int, ...],
        duration: float,
        backend: str = "inductor"
    ) -> None:
        """Record recompile and check for alerts."""
        super().record_recompile(function_id, shape, duration, backend)

        # Check for excessive recompilation
        stats = self.get_function_stats(function_id)
        if stats and stats.recompile_count >= self.max_recompiles:
            self._add_alert(
                function_id,
                "excessive_recompiles",
                f"Function {function_id} has {stats.recompile_count} recompiles"
            )

        # Check ratio
        if stats and stats.recompile_ratio >= self.alert_threshold:
            self._add_alert(
                function_id,
                "high_recompile_ratio",
                f"Recompile ratio {stats.recompile_ratio:.2%}"
            )

    def _add_alert(
        self,
        function_id: int,
        alert_type: str,
        message: str
    ) -> None:
        """Add an alert."""
        alert = {
            "timestamp": time.time(),
            "function_id": function_id,
            "type": alert_type,
            "message": message
        }
        self._alerts.append(alert)
        logger.warning(f"Compilation alert: {message}")

    def get_alerts(self) -> List[Dict[str, Any]]:
        """Get all alerts."""
        with self._lock:
            return list(self._alerts)

    def get_optimization_suggestions(self) -> List[str]:
        """Get optimization suggestions based on patterns."""
        suggestions = []

        with self._lock:
            for stats in self._function_stats.values():
                if stats.recompile_ratio > 0.3:
                    suggestions.append(
                        f"Function {stats.function_id}: Consider using dynamic=True "
                        f"or padding to reduce {stats.unique_shapes} unique shapes"
                    )

                if stats.avg_compile_time > 1.0:
                    suggestions.append(
                        f"Function {stats.function_id}: Compile time "
                        f"({stats.avg_compile_time:.2f}s) is high, "
                        "consider caching or warming up"
                    )

        return suggestions


class TrendAnalyzer:
    """
    Analyze compilation trends over time.

    Beyond vLLM:
    - Detects degradation patterns
    - Predicts future issues
    """

    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self._compile_times: List[float] = []
        self._timestamps: List[float] = []

    def add_sample(self, compile_time: float) -> None:
        """Add a compile time sample."""
        self._compile_times.append(compile_time)
        self._timestamps.append(time.time())

        # Keep window size
        if len(self._compile_times) > self.window_size:
            self._compile_times = self._compile_times[-self.window_size:]
            self._timestamps = self._timestamps[-self.window_size:]

    def get_trend(self) -> str:
        """Get trend direction."""
        if len(self._compile_times) < 10:
            return "insufficient_data"

        first_half = self._compile_times[:len(self._compile_times)//2]
        second_half = self._compile_times[len(self._compile_times)//2:]

        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)

        if avg_second > avg_first * 1.1:
            return "increasing"
        elif avg_second < avg_first * 0.9:
            return "decreasing"
        else:
            return "stable"

    def get_stats(self) -> Dict[str, float]:
        """Get trend statistics."""
        if not self._compile_times:
            return {"min": 0, "max": 0, "avg": 0, "std": 0}

        n = len(self._compile_times)
        avg = sum(self._compile_times) / n
        variance = sum((x - avg) ** 2 for x in self._compile_times) / n
        std = variance ** 0.5

        return {
            "min": min(self._compile_times),
            "max": max(self._compile_times),
            "avg": avg,
            "std": std
        }


# Global counter instance
_global_counter: Optional[CompilationCounter] = None


def get_global_counter() -> CompilationCounter:
    """Get or create global compilation counter."""
    global _global_counter
    if _global_counter is None:
        _global_counter = CompilationCounter(name="global")
    return _global_counter


def reset_global_counter() -> None:
    """Reset global counter."""
    global _global_counter
    if _global_counter:
        _global_counter.reset()
