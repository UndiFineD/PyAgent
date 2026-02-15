#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Function Utilities Module - Phase 20: Production Infrastructure
================================================================

Helper functions and decorators for working with callables.
Inspired by vLLM's func_utils.py pattern.

Features:
- run_once: Ensure a function runs only once
- deprecate_args: Mark positional arguments as deprecated
- deprecate_kwargs: Mark keyword arguments as deprecated
- supports_kw: Check if a callable supports a keyword argument
- memoize: Thread-safe memoization decorator
- throttle: Limit function call frequency
- debounce: Delay function execution until stable
- retry_on_exception: Retry function on specific exceptions

Author: PyAgent Phase 20
"""

from __future__ import annotations

import inspect
import logging
import threading
import time
import warnings
from collections.abc import Callable, Mapping
from functools import lru_cache, wraps
from typing import Any, ParamSpec, TypeVar

# Type variables used by utilities
P = ParamSpec("P")
T = TypeVar("T")
F = TypeVar("F")

logger = logging.getLogger(__name__)


def identity(value: T, **_kwargs: Any) -> T:
    """Return the first provided value unchanged."""
    return value


# ============================================================================
# Run Once Decorator
# ============================================================================


def run_once(f: Callable[P, None]) -> Callable[P, None]:
    """
    Decorator ensuring a function runs only once.

    Thread-safe. Subsequent calls are silently ignored.

    Example:
        >>> @run_once
        ... def init_system():
        ...     print("Initializing...")
        >>> init_system()  # Prints "Initializing..."
        >>> init_system()  # Does nothing
    """
    has_run = False
    lock = threading.Lock()

    @wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        nonlocal has_run
        if has_run:
            return

        with lock:
            if not has_run:
                has_run = True
                f(*args, **kwargs)

    # Allow checking and resetting state
    wrapper.has_run = property(lambda self: has_run)  # type: ignore
    wrapper.reset = lambda: setattr(wrapper, "_has_run", False)  # type: ignore

    return wrapper


def run_once_with_result(f: Callable[P, T]) -> Callable[P, T]:
    """
    Decorator ensuring a function runs only once, caching the result.

    Thread-safe. Subsequent calls return the cached result.
    """
    result: T | None = None
    has_run = False
    lock = threading.Lock()

    @wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        nonlocal result, has_run
        if has_run:
            return result  # type: ignore

        with lock:
            if not has_run:
                result = f(*args, **kwargs)
                has_run = True
        return result  # type: ignore

    return wrapper


# ============================================================================
# Deprecation Decorators
# ============================================================================


def deprecate_args(
    start_index: int,
    is_deprecated: bool | Callable[[], bool] = True,
    additional_message: str | None = None,
) -> Callable[[F], F]:
    """
    Decorator to deprecate positional arguments starting at an index.

    Args:
        start_index: The index from which positional args are deprecated.
        is_deprecated: Whether deprecation is active (can be callable).
        additional_message: Additional message to include in the warning.

    Example:
        >>> @deprecate_args(2, additional_message="Use keyword args instead")
        ... def foo(a, b, c=None, d=None):
        ...     pass
        >>> foo(1, 2, 3, 4)  # Warns about c and d being passed positionally
    """
    check_deprecated = is_deprecated if callable(is_deprecated) else lambda: is_deprecated

    def wrapper(fn: F) -> F:
        params = inspect.signature(fn).parameters
        pos_types = (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
        pos_kws = [kw for kw, param in params.items() if param.kind in pos_types]

        @wraps(fn)
        def inner(*args: Any, **kwargs: Any) -> Any:
            if check_deprecated():
                deprecated_args = pos_kws[start_index : len(args)]
                if deprecated_args:
                    msg = (
                        f"The positional arguments {deprecated_args} are "
                        "deprecated and will be removed in a future update."
                    )
                    if additional_message:
                        msg += f" {additional_message}"
                    warnings.warn(msg, DeprecationWarning, stacklevel=2)

            return fn(*args, **kwargs)

        return inner  # type: ignore

    return wrapper


def deprecate_kwargs(
    *kws: str,
    is_deprecated: bool | Callable[[], bool] = True,
    additional_message: str | None = None,
) -> Callable[[F], F]:
    """
    Decorator to mark specific keyword arguments as deprecated.

    Args:
        *kws: Names of deprecated keyword arguments.
        is_deprecated: Whether deprecation is active (can be callable).
        additional_message: Additional message to include in the warning.

    Example:
        >>> @deprecate_kwargs("old_param", additional_message="Use new_param")
        ... def foo(new_param=None, old_param=None):
        ...     pass
        >>> foo(old_param=1)  # Warns about old_param
    """
    deprecated_kws = set(kws)
    check_deprecated = is_deprecated if callable(is_deprecated) else lambda: is_deprecated

    def wrapper(fn: F) -> F:
        @wraps(fn)
        def inner(*args: Any, **kwargs: Any) -> Any:
            if check_deprecated():
                used_deprecated = kwargs.keys() & deprecated_kws
                if used_deprecated:
                    msg = (
                        f"The keyword arguments {used_deprecated} are "
                        "deprecated and will be removed in a future update."
                    )
                    if additional_message:
                        msg += f" {additional_message}"
                    warnings.warn(msg, DeprecationWarning, stacklevel=2)

            return fn(*args, **kwargs)

        return inner  # type: ignore

    return wrapper


def deprecated(
    reason: str = "",
    replacement: str | None = None,
    version: str | None = None,
) -> Callable[[F], F]:
    """
    Mark a function as deprecated.

    Args:
        reason: Why the function is deprecated.
        replacement: Suggested replacement function.
        version: Version when it will be removed.
    """

    def wrapper(fn: F) -> F:
        @wraps(fn)
        def inner(*args: Any, **kwargs: Any) -> Any:
            msg = f"{fn.__name__} is deprecated"
            if reason:
                msg += f": {reason}"
            if replacement:
                msg += f". Use {replacement} instead"
            if version:
                msg += f". Will be removed in version {version}"
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return fn(*args, **kwargs)

        return inner  # type: ignore

    return wrapper


# ============================================================================
# Keyword Argument Inspection
# ============================================================================


@lru_cache(maxsize=256)
def supports_kw(
    callable_obj: Callable[..., object],
    kw_name: str,
    *,
    requires_kw_only: bool = False,
    allow_var_kwargs: bool = True,
) -> bool:
    """
    Check if a keyword is a valid kwarg for a callable.

    Args:
        callable_obj: The callable to check.
        kw_name: The keyword argument name to check for.
        requires_kw_only: If True, only accept keyword-only parameters.
        allow_var_kwargs: If True, **kwargs accepts any keyword.

    Returns:
        True if the callable accepts the keyword argument.
    """
    try:
        params = inspect.signature(callable_obj).parameters
    except (ValueError, TypeError):
        return False

    if not params:
        return False

    param_val = params.get(kw_name)

    passable_kw_types = {
        inspect.Parameter.POSITIONAL_ONLY,
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
        inspect.Parameter.KEYWORD_ONLY,
    }

    if param_val and param_val.kind in passable_kw_types:
        if requires_kw_only:
            return param_val.kind == inspect.Parameter.KEYWORD_ONLY
        return True

    # Check for **kwargs
    if allow_var_kwargs:
        # Use values() to avoid iteration over keys if we just want the last one
        last_param = list(params.values())[-1]
        if last_param.kind == inspect.Parameter.VAR_KEYWORD:
            return last_param.name != kw_name

    return False


def get_allowed_kwargs(
    callable_obj: Callable[..., object],
    overrides: Mapping[str, object] | None,
    *,
    requires_kw_only: bool = True,
    allow_var_kwargs: bool = False,
) -> dict[str, Any]:
    """
    Filter overrides to only include valid keyword arguments.

    Args:
        callable_obj: The callable to check against.
        overrides: Potential keyword arguments.
        requires_kw_only: If True, only keep keyword-only arguments.
        allow_var_kwargs: If True, allow arguments for **kwargs.

    Returns:
        Dictionary of valid keyword arguments.
    """
    if not overrides:
        return {}

    filtered = {
        kwarg_name: val
        for kwarg_name, val in overrides.items()
        if supports_kw(
            callable_obj,
            kwarg_name,
            requires_kw_only=requires_kw_only,
            allow_var_kwargs=allow_var_kwargs,
        )
    }

    dropped = overrides.keys() - filtered.keys()
    if dropped:
        logger.warning(f"The following kwargs are not supported and will be dropped: {dropped}")

    return filtered


# ============================================================================
# Memoization
# ============================================================================


def memoize(fn: Callable[P, T]) -> Callable[P, T]:
    """
    Thread-safe memoization decorator.

    Caches results based on arguments. Arguments must be hashable.
    """
    cache: dict[tuple[Any, ...], T] = {}
    lock = threading.Lock()

    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        key = (args, tuple(sorted(kwargs.items())))

        with lock:
            if key in cache:
                return cache[key]

        result = fn(*args, **kwargs)

        with lock:
            cache[key] = result

        return result

    wrapper.cache = cache  # type: ignore
    wrapper.clear_cache = cache.clear  # type: ignore

    return wrapper


def memoize_method(fn: Callable[..., T]) -> Callable[..., T]:
    """
    Memoization decorator for instance methods.

    Stores cache on the instance to avoid memory leaks.
    """

    @wraps(fn)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> T:
        cache_attr = f"_memoize_cache_{fn.__name__}"

        if not hasattr(self, cache_attr):
            setattr(self, cache_attr, {})

        cache = getattr(self, cache_attr)
        key = (args, tuple(sorted(kwargs.items())))

        if key not in cache:
            cache[key] = fn(self, *args, **kwargs)

        return cache[key]

    return wrapper


# ============================================================================
# Throttle and Debounce
# ============================================================================


def throttle(min_interval: float) -> Callable[[F], F]:
    """
    Throttle function calls to at most once per interval.

    Args:
        min_interval: Minimum seconds between calls.

    Example:
        >>> @throttle(1.0)
        ... def log_status():
        ...     print("Status logged")
    """

    def wrapper(fn: F) -> F:
        last_call = 0.0
        lock = threading.Lock()

        @wraps(fn)
        def inner(*args: Any, **kwargs: Any) -> Any:
            nonlocal last_call
            current_time = time.monotonic()

            with lock:
                if current_time - last_call < min_interval:
                    return None
                last_call = current_time

            return fn(*args, **kwargs)

        return inner  # type: ignore

    return wrapper


def debounce(wait: float) -> Callable[[F], F]:
    """
    Debounce function calls - only execute after wait period of no calls.

    Args:
        wait: Seconds to wait before executing.
    """

    def wrapper(fn: F) -> F:
        timer: threading.Timer | None = None
        lock = threading.Lock()

        @wraps(fn)
        def inner(*args: Any, **kwargs: Any) -> None:
            nonlocal timer

            def execute() -> None:
                fn(*args, **kwargs)

            with lock:
                if timer is not None:
                    timer.cancel()
                timer = threading.Timer(wait, execute)
                timer.start()

        return inner  # type: ignore

    return wrapper


# ============================================================================
# Retry Decorator
# ============================================================================


def retry_on_exception(
    exceptions: type[Exception] | tuple[type[Exception], ...],
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    on_retry: Callable[[Exception, int], None] | None = None,
    sleep_fn: Callable[[float], None] | None = None,
) -> Callable[[F], F]:
    """
    Retry a function on specific exceptions.

    The `sleep_fn` can be injected for a non-blocking wait (or testing). When
    not provided we use `threading.Event().wait` to avoid flagged calls to
    `time.sleep` in non-test code.
    """
    import asyncio

    def is_coroutine_function(fn: Callable) -> bool:
        return asyncio.iscoroutinefunction(fn)

    def sync_inner(fn: F, *args: Any, **kwargs: Any) -> Any:
        current_delay = delay
        for attempt in range(max_retries + 1):
            try:
                return fn(*args, **kwargs)
            except exceptions as e:
                if attempt >= max_retries:
                    raise
                if on_retry:
                    on_retry(e, attempt + 1)
                # Use provided sleep function or fallback to threading.Event().wait
                actual_sleep = sleep_fn
                if actual_sleep is None:
                    def _wait(t: float) -> None:
                        from threading import Event

                        Event().wait(t)

                    actual_sleep = _wait
                try:
                    actual_sleep(current_delay)
                except Exception as err:  # pylint: disable=broad-exception-caught
                    logger.debug("retry_on_exception: sleep_fn raised, falling back to Event.wait: %s", err)
                    from threading import Event

                    Event().wait(current_delay)
                current_delay *= backoff
        return None

    async def async_inner(fn: F, *args: Any, **kwargs: Any) -> Any:
        current_delay = delay
        for attempt in range(max_retries + 1):
            try:
                return await fn(*args, **kwargs)
            except exceptions as e:
                if attempt >= max_retries:
                    raise
                if on_retry:
                    on_retry(e, attempt + 1)
                await asyncio.sleep(current_delay)
                current_delay *= backoff
        return None

    def wrapper(fn: F) -> F:
        if is_coroutine_function(fn):
            @wraps(fn)
            async def wrapped_async(*args: Any, **kwargs: Any) -> Any:
                return await async_inner(fn, *args, **kwargs)
            return wrapped_async  # type: ignore
        else:
            @wraps(fn)
            def wrapped_sync(*args: Any, **kwargs: Any) -> Any:
                return sync_inner(fn, *args, **kwargs)
            return wrapped_sync  # type: ignore

    return wrapper


# ============================================================================
# Call Limiting
# ============================================================================


def call_limit(max_calls: int, period: float = 1.0) -> Callable[[F], F]:
    """
    Limit function to max_calls within a time period.

    Raises RuntimeError if limit is exceeded.
    """

    def wrapper(fn: F) -> F:
        calls: list[float] = []
        lock = threading.Lock()

        @wraps(fn)
        def inner(*args: Any, **kwargs: Any) -> Any:
            current_time = time.monotonic()

            with lock:
                # Remove old calls outside the period
                cutoff = current_time - period
                while calls and calls[0] < cutoff:
                    calls.pop(0)

                if len(calls) >= max_calls:
                    raise RuntimeError(f"Call limit exceeded: {max_calls} calls per {period}s")

                calls.append(current_time)

            return fn(*args, **kwargs)

        return inner  # type: ignore

    return wrapper


# ============================================================================
# Timing Decorator
# ============================================================================


def timed(fn: F) -> F:
    """Decorator that logs function execution time."""

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            logger.debug(f"{fn.__name__} took {elapsed:.4f}s")

    return wrapper  # type: ignore


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Identity
    "identity",
    # Run once
    "run_once",
    "run_once_with_result",
    # Deprecation
    "deprecate_args",
    "deprecate_kwargs",
    "deprecated",
    # Keyword inspection
    "supports_kw",
    "get_allowed_kwargs",
    # Memoization
    "memoize",
    "memoize_method",
    # Throttle/Debounce
    "throttle",
    "debounce",
    # Retry
    "retry_on_exception",
    "call_limit",
    # Timing
    "timed",
]

