#!/usr/bin/env python3
"""Small collection of function utilities used by tests.

This module implements a compact subset of decorators and helpers so tests
can import stable behavior without depending on the original project's
complex and possibly-corrupted implementations.
"""

from __future__ import annotations

import functools
import inspect
import threading
import time
import warnings
from collections.abc import Callable
from typing import Any, Dict, Iterable, Tuple, TypeVar

P = TypeVar("P")
T = TypeVar("T")
F = TypeVar("F")


def identity(value: T, **_kwargs: Any) -> T:
    return value


def run_once(fn: Callable[..., Any]) -> Callable[..., Any]:
    lock = threading.Lock()
    has_run = False

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        nonlocal has_run
        if has_run:
            return None
        with lock:
            if not has_run:
                has_run = True
                return fn(*args, **kwargs)
        return None

    wrapper.reset = lambda: setattr(wrapper, "_has_run", False)  # type: ignore
    return wrapper


def run_once_with_result(fn: Callable[..., T]) -> Callable[..., T]:
    lock = threading.Lock()
    has_run = False
    result: T | None = None

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        nonlocal has_run, result
        if has_run:
            return result  # type: ignore
        with lock:
            if not has_run:
                result = fn(*args, **kwargs)
                has_run = True
        return result  # type: ignore

    return wrapper


def deprecate_kwargs(*kws: str, additional_message: str | None = None):
    """Decorator to mark specific keyword arguments as deprecated.

    Args:
        *kws: Names of keyword arguments to mark as deprecated.
        additional_message: Optional additional message to include in the deprecation warning.

    Returns:
        A decorator function that wraps the target function and warns when deprecated kwargs are used.
    """
    deprecated = set(kws)

    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            used = set(kwargs.keys()) & deprecated
            if used:
                msg = f"Deprecated kwargs used: {used}"
                if additional_message:
                    msg += f"; {additional_message}"
                warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return fn(*args, **kwargs)

        return wrapper

    return deco


def deprecate_args(start_index: int, additional_message: str | None = None):
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if len(args) > start_index:
                msg = f"Positional args at or after index {start_index} are deprecated"
                if additional_message:
                    msg += f"; {additional_message}"
                warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return fn(*args, **kwargs)

        return wrapper

    return deco


def deprecated(reason: str | None = None):
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            msg = f"{fn.__name__} is deprecated"
            if reason:
                msg += f": {reason}"
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return fn(*args, **kwargs)

        return wrapper

    return deco


def supports_kw(callable_obj: Callable[..., Any], kw_name: str) -> bool:
    try:
        sig = inspect.signature(callable_obj)
    except Exception:
        return False
    return kw_name in sig.parameters


def get_allowed_kwargs(callable_obj: Callable[..., Any], overrides: Dict[str, Any] | None) -> Dict[str, Any]:
    if not overrides:
        return {}
    return {k: v for k, v in overrides.items() if supports_kw(callable_obj, k)}


def memoize(fn: Callable[..., T]) -> Callable[..., T]:
    cache: Dict[Tuple[Any, ...], T] = {}
    lock = threading.Lock()

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        key = (args, tuple(sorted(kwargs.items())))
        with lock:
            if key in cache:
                return cache[key]
        res = fn(*args, **kwargs)
        with lock:
            cache[key] = res
        return res

    wrapper.cache = cache  # type: ignore
    return wrapper


def memoize_method(fn: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(fn)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> T:
        cache_attr = f"_memo_{fn.__name__}"
        if not hasattr(self, cache_attr):
            setattr(self, cache_attr, {})
        cache = getattr(self, cache_attr)
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = fn(self, *args, **kwargs)
        return cache[key]

    return wrapper


def debounce(wait: float):
    """Return a decorator that debounces calls to the function by `wait` seconds."""
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        timer = None

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> None:
            nonlocal timer

            def _call():
                fn(*args, **kwargs)

            if timer is not None:
                timer.cancel()  # type: ignore[attr-defined]
            timer_obj = threading.Timer(wait, _call)
            timer_obj.daemon = True
            timer_obj.start()

        return wrapper

    return deco


def retry_on_exception(retries: int = 3, delay: float = 0.0):
    def deco(fn: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exc = None
            for _ in range(retries):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if delay:
                        time.sleep(delay)
            raise last_exc  # type: ignore

        return wrapper

    return deco


def call_limit(max_calls: int):
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        count = 0

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal count
            if count >= max_calls:
                raise RuntimeError("call limit exceeded")
            count += 1
            return fn(*args, **kwargs)

        return wrapper

    return deco


def timed(fn: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        start = time.time()
        try:
            return fn(*args, **kwargs)
        finally:
            end = time.time()
            # simple timing side-effect for debugging; not printed in tests
            _ = end - start

    return wrapper


def throttle(min_interval: float):
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        last = 0.0
        lock = threading.Lock()

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal last
            now = time.monotonic()
            with lock:
                if now - last < min_interval:
                    return None
                last = now
            return fn(*args, **kwargs)

        return wrapper

    return deco


__all__ = [
    "identity",
    "run_once",
    "run_once_with_result",
    "deprecate_kwargs",
    "deprecated",
    "supports_kw",
    "get_allowed_kwargs",
    "memoize",
    "memoize_method",
    "throttle",
]
