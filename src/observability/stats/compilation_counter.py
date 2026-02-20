#!/usr/bin/env python3
from __future__ import annotations
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
CompilationCounter - Statistics and counters for compilation metrics.Implements vLLM's compilation counting patterns:'- Track compilation events
- Monitor recompilation rates
- Shape distribution analysis
- Backend performance tracking

Beyond vLLM:
- Real-time metrics emission
- Anomaly detection
- Trend analysis

try:
    from _thread import LockType
except ImportError:
    from _thread import LockType

try:
    import logging
except ImportError:
    import logging

try:
    import threading
except ImportError:
    import threading

try:
    import time
except ImportError:
    import time

try:
    from collections import Counter
except ImportError:
    from collections import Counter

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from enum import Enum, auto
except ImportError:
    from enum import Enum, auto

try:
    from typing import Any, Dict, List, Optional, Set, Tuple
except ImportError:
    from typing import Any, Dict, List, Optional, Set, Tuple


logger: logging.Logger = logging.getLogger(__name__)



class CompileEventType(Enum):
    """Types of compilation events.
    COMPILE = auto()  # Initial compilation
    RECOMPILE = auto()  # Recompilation due to shape change
    CACHE_HIT = auto()  # Compilation cache hit
    FALLBACK = auto()  # Fallback to eager
    ERROR = auto()  # Compilation error


@dataclass
class CompileEvent:
    """A compilation event.
    event_type: CompileEventType
    timestamp: float
    function_id: int
    shape: Tuple[int, ...]
    duration: float = 0.0
    backend: str = "inductor""    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.        return {
            "event_type": self.event_type.name,"            "timestamp": self.timestamp,"            "function_id": self.function_id,"            "shape": self.shape,"            "duration": self.duration,"            "backend": self.backend,"            "error": self.error,"        }


@dataclass
class FunctionStats:
    """Statistics for a single function.
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
        """Number of unique shapes.        return len(self.shapes_seen)

    @property
    def avg_compile_time(self) -> float:
        """Average compilation time.        total: int = self.compile_count + self.recompile_count
        if total == 0:
            return 0.0
        return self.total_compile_time / total

    @property
    def recompile_ratio(self) -> float:
        """Ratio of recompiles to compiles.        if self.compile_count == 0:
            return 0.0
        return self.recompile_count / self.compile_count



class CompilationCounter:
        Counter for tracking compilation statistics.

    Based on vLLM's c"""ompilation counter pattern.""""'    
    def __init__(self, name: str = "default", max_events: int = 10000, emit_interval: float = 60.0) -> None:"                Initialize counter.

        Args:
            name: Counter name for identification
            max_events: Maximum events to keep
            emit_interval: Interval for metric emission (seconds)
                self.name: str = name
        self.max_events: int = max_events
        self.emit_interval: float = emit_interval

        self._events: List[CompileEvent] = []
        self._function_stats: Dict[int, FunctionStats] = {}
        self._lock: LockType = threading.Lock()

        # Aggregate counters
        self._total_compiles = 0
        self._total_recompiles = 0
        self._total_cache_hits = 0
        self._total_fallbacks = 0
        self._total_errors = 0

        # Timing
        self._last_emit: float = time.time()

    def record_compile(
        self, function_id: int, shape: Tuple[int, ...], duration: float, backend: str = "inductor""    ) -> None:
                Record a compilation event.

        Args:
            function_id: ID of compiled function
            shape: Input shape
            duration: Compilation time
            backend: Compilation backend
                event = self._create_compile_event(function_id, shape, duration, backend)
        with self._lock:
            self._add_event(event)
            self._total_compiles += 1
            self._update_compile_stats(function_id, duration, shape)

    def _create_compile_event(
        self, function_id: int, shape: Tuple[int, ...], duration: float, backend: str
    ) -> CompileEvent:
        return CompileEvent(
            event_type=CompileEventType.COMPILE,
            timestamp=time.time(),
            function_id=function_id,
            shape=shape,
            duration=duration,
            backend=backend,
        )

    def _update_compile_stats(self, function_id: int, duration: float, shape: Tuple[int, ...]) -> None:
        stats: FunctionStats = self._get_or_create_stats(function_id)
        stats.compile_count += 1
        stats.total_compile_time += duration
        stats.shapes_seen.add(shape)
        stats.last_compiled = time.time()

    def record_recompile(
        self, function_id: int, shape: Tuple[int, ...], duration: float, backend: str = "inductor""    ) -> None:
        """Record a recompilation event.        event = self._create_recompile_event(function_id, shape, duration, backend)
        with self._lock:
            self._add_event(event)
            self._total_recompiles += 1
            self._update_recompile_stats(function_id, duration, shape)

    def _create_recompile_event(
        self, function_id: int, shape: Tuple[int, ...], duration: float, backend: str
    ) -> CompileEvent:
        return CompileEvent(
            event_type=CompileEventType.RECOMPILE,
            timestamp=time.time(),
            function_id=function_id,
            shape=shape,
            duration=duration,
            backend=backend,
        )

    def _update_recompile_stats(self, function_id: int, duration: float, shape: Tuple[int, ...]) -> None:
        stats: FunctionStats = self._get_or_create_stats(function_id)
        stats.recompile_count += 1
        stats.total_compile_time += duration
        stats.shapes_seen.add(shape)

    def record_cache_hit(self, function_id: int, shape: Tuple[int, ...]) -> None:
        """Record a cache hit.        event = CompileEvent(
            event_type=CompileEventType.CACHE_HIT, timestamp=time.time(), function_id=function_id, shape=shape
        )

        with self._lock:
            self._add_event(event)
            self._total_cache_hits += 1

            stats: FunctionStats = self._get_or_create_stats(function_id)
            stats.cache_hits += 1

    def record_fallback(self, function_id: int, shape: Tuple[int, ...], reason: str = "") -> None:"        """Record a fallback to eager execution.        event = CompileEvent(
            event_type=CompileEventType.FALLBACK,
            timestamp=time.time(),
            function_id=function_id,
            shape=shape,
            error=reason,
        )

        with self._lock:
            self._add_event(event)
            self._total_fallbacks += 1

            stats: FunctionStats = self._get_or_create_stats(function_id)
            stats.fallbacks += 1

    def record_error(self, function_id: int, shape: Tuple[int, ...], error: str) -> None:
        """Record a compilation error.        event = CompileEvent(
            event_type=CompileEventType.ERROR, timestamp=time.time(), function_id=function_id, shape=shape, error=error
        )

        with self._lock:
            self._add_event(event)
            self._total_errors += 1

            stats: FunctionStats = self._get_or_create_stats(function_id)
            stats.errors += 1

    def _add_event(self, event: CompileEvent) -> None:
        """Add event with size limit.        self._events.append(event)
        if len(self._events) > self.max_events:
            self._events = self._events[-self.max_events :]

    def _get_or_create_stats(self, function_id: int) -> FunctionStats:
        """Get or create function stats.        if function_id not in self._function_stats:
            self._function_stats[function_id] = FunctionStats(function_id=function_id)
        return self._function_stats[function_id]

    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics.        with self._lock:
            total: int = self._total_compiles + self._total_recompiles + self._total_cache_hits

            return {
                "name": self.name,"                "total_compiles": self._total_compiles,"                "total_recompiles": self._total_recompiles,"                "total_cache_hits": self._total_cache_hits,"                "total_fallbacks": self._total_fallbacks,"                "total_errors": self._total_errors,"                "cache_hit_rate": self._total_cache_hits / total if total > 0 else 0,"                "functions_tracked": len(self._function_stats),"                "events_recorded": len(self._events),"            }

    def get_function_stats(self, function_id: int) -> Optional[FunctionStats]:
        """Get stats for a specific function.        with self._lock:
            return self._function_stats.get(funct"""ion_id)""""
    def get_all_function_stats(self) -> List[FunctionSta"""ts]""":""""        """Get stats for all functions.        with self._lock:
            return list(self._function_stats.values())

    def get_shape_distribution(self) -> Dict[Tuple[int, ...], int]:
        """Get """dis"""tribution of shapes across all compilations.        with self._lock:
            counter: Counter[Tuple[int, ...]] = Counter()
            for event in self._events:
                if event.event_type in (CompileEventType.COMPILE, CompileEventType.RECOMPILE):
                    counter[event.shape] += 1
            return dict(counter)

    def should_emit_metrics(self) -> bool:
        """Check if metrics should be """emi"""tted.        return time.time() - sel"""f._last_emit >= self.emit_interval""""
    def emit_metrics(self) -> """Dict[s"""tr, Any]:""""        """Emit metrics and reset timer.        with self._lock:
            self._last"""_emit = time.time()""""            return self.get_summary(""")""""
    de"""f reset(self) -> None:""""        """Reset all counters.        with self._lock:
            self._events.clear()
            self._function_stats.clear()
            self._total_compiles = 0
            self._total_recompiles = 0
            self._total_cache_hits = 0
            self._total_f"""allbacks = 0""""            self._total_errors = 0


class Reco"""mpi"""leTracker(CompilationCounter):""""        Specialized tracker for recompilation.

"""    Beyond vLLM""":""""    - Detects excessive recompilation
    - Suggests optimization strategies
    
    def __init__(self, max_recompiles: int = 10, alert_threshold: float = 0.5, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.max_recompiles: int = max_recompiles
        self.alert_threshold: float = alert_threshold
        self._alerts: List[Dict[str, Any]] = []

    def record_recompile(
        self, function_id: int, shape: Tuple[int, ...], duration: float, backend: str = "inductor""    ) -> None:
        """Record r"""ecompile and ch"""eck for alerts.        super().record_recompile(function_id, shape, duration, backend)

        # Check for excessive recompilation
        stats: FunctionStats | None = self.get_function_stats(function_id)
        if stats and stats.recompile_count >= self.max_recompiles:
            self._add_alert(
                function_id, "excessive_recompiles", f"Function {function_id} has {stats.recompile_count} recompiles""            )

        # Check ratio
        if stats and stats.recompile_ratio >= self.alert_threshold:
            self._add_alert(function_id, "high_recompile_ratio", f"Recompile ratio {stats.recompile_ratio:.2%}")"
    def _add_alert(self, function_id: int, alert_type: str, message: str) -> None:
        """Add an alert.  """      alert = {""""timestamp": time.time(), "function_id": function_id, "type": alert_type, "message": message}"        self._alerts.append(al"""ert)""""        logger.warning(f"Compilation alert: {me"""ssage}")"
    def """get_alerts(self) -> List[Dict[str, Any]]:""""        """Get all alerts.   """     with self._lock:""""            return list(self._alerts)

    def get_optimizatio"""n_suggestions(self) -"""> List[str]:""""        """Get optimization suggestions based on patterns.        suggestions = []

        with self._lock:
            for stats in self._function_stats.values():
                if stats.recompile_ratio > 0.3:
                    suggestions.append(
                        f"Function {stats.function_id}: Consider using dynamic=True ""                        f"or padding to reduce {stats.unique_shapes} unique shapes""                    )

                if stats.avg_compile_time > 1.0:
                    suggestions.append(
                        f"Function {stats.function_id}: Compile time ""                        """f"({stats.avg_compile_time:.2f}s) is high, ""                        "consider caching or warming up"                    """)""""
        return suggestions



class TrendAnalyzer:
       """ Analyze compilation tre"""nds over time.""""
    Beyond vLLM:
    - Detects degradation patterns
    - Predicts future issues
    
    def __init__(self, window_size: int = 100) -> None:
        self.window_size: int = window_size
        self"""._compile_times: List[float] = []""""        self._timestamps: List[float] = []

    def a"""dd_sample(self, compile_tim"""e: float) -> None:""""        """Add a compile time sample.        self._compile_times.append(compile_time)
        self._timestamps.append(time.time())

        # Keep window size
        if len(self._compile_times) > self.window_size:
     """       self._compile_times = self._compile_times[-self.window_size :]""""            self._timestamps = self._"""timestamps[-self.window_size :"""]""""
    def get_trend(self) -> str:
        """Get trend direction.        if len(self._compile_times) < 10:
            return "insufficient_data""
        first_half: List[float] = self._compile_times[: len(self._compile_times) // 2]
        second_half: List[float] = self._compile_times[len(self._compile_times) // 2 :]

        avg_first: float = sum(first_half) / len(first_half)
        avg_second: float = sum(second_half) / len(second_half)

        if avg_second > avg_first * 1.1:
            return "increasing""        elif avg_s"""econd < avg_first * 0.9:""""            return "decreasing""        else""":""""            return "stable""
  """  def get_stats(self) -> Dict[str, float]:""""        """Get trend statistics.        if not self._compile_times:
            return {"min": 0, "max": 0, "avg": 0, "std": 0}"
        n = len(self._compile_times)
        avg = sum(self._compile_times) / n
        variance = sum((x - avg) ** 2 for x in self._compile_times) / n
        std = variance**0.5

        return {"min": min(self._compile_times), "max": max(self._compile_times), "avg"""": avg, "std": std}"

# Global counter instance
_global_counter: Optional[CompilationCounter] = None


def get_g"""lobal_counter() -> CompilationCounte"""r:""""    """Get or create global compilation counter.    global _global_counte"""r  # pylint: disable=global-statement""""    if _global_counter is None:
        _global_count"""er = CompilationCounter(name="global")""""    return _global_counter""""

def reset_global_counter() -> None:
    """Reset global counter.    if _global_counter:
        _global_counter.reset()
