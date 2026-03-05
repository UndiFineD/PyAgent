#!/usr/bin/env python3
try:
    # Prefer real implementation if it exists elsewhere
    from src.infrastructure.backend._impl import ABTester as _ABTester  # type: ignore
except Exception:

    class _ABTester:
        def __init__(self, *args, **kwargs):
            raise RuntimeError(
                "ABTester implementation not available in this environment"
            )


ABTester = _ABTester

__all__ = ["ABTester"]
