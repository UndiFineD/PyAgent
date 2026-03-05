#!/usr/bin/env python3
"""RetryHelper shim for pytest collection."""


class RetryHelper:
    @staticmethod
    def retry(fn, retries=1, *args, **kwargs):
        last_exc = None
        for _ in range(max(1, retries)):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                last_exc = e
        if last_exc:
            raise last_exc


__all__ = ["RetryHelper"]
