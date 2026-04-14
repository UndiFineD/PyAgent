"""Performance optimization for component_41_6."""

import time
from functools import wraps
from typing import Any, Callable, Optional


def cache_result(ttl: int = 300):
    """Cache function results with TTL."""
    def decorator(func: Callable) -> Callable:
        cache = {}
        timestamps = {}

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            key = str((args, sorted(kwargs.items())))
            current_time = time.time()

            if key in cache:
                if current_time - timestamps[key] < ttl:
                    return cache[key]

            result = func(*args, **kwargs)
            cache[key] = result
            timestamps[key] = current_time
            return result

        return wrapper
    return decorator

def profile_execution(func: Callable) -> Callable:
    """Profile function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"{func.__name__} took {duration:.3f}s")
        return result
    return wrapper

@cache_result(ttl=60)
@profile_execution
def optimized_operation():
    """Example optimized operation."""
    time.sleep(0.1)
    return "result"
