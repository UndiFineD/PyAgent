"""
Profiling utilities for PyAgent.
Includes Rust acceleration profiling and performance tracking.
"""

from src.observability.profiling.rust_profiler import (
    RustProfiler,
    RustUsageScanner,
    FunctionStats,
    profile_rust_call,
    create_profiled_rust_core,
)

from src.observability.profiling.profile_decorators import (
    ProfileResult,
    cprofile_context,
    cprofile,
    timer_context,
    timer,
    ProfileAccumulator,
    track,
    get_profile_report,
    reset_profile_data,
)

__all__ = [
    # RustProfiler
    "RustProfiler",
    "RustUsageScanner",
    "FunctionStats",
    "profile_rust_call",
    "create_profiled_rust_core",
    # ProfileDecorators
    "ProfileResult",
    "cprofile_context",
    "cprofile",
    "timer_context",
    "timer",
    "ProfileAccumulator",
    "track",
    "get_profile_report",
    "reset_profile_data",
]
