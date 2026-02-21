#!/usr/bin/env python3
"""Simple file lock context manager used in tests and repair runs."""

from __future__ import annotations
import os
import time
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def file_lock(path: str, timeout: float = 5.0, poll: float = 0.05) -> Iterator[None]:
    """Acquire a simple filesystem lock by creating a .lock file.

    This is intentionally minimal and not suitable for production use.
    """
    lockfile = f"{path}.lock"
    start = time.time()
    while True:
        try:
            fd = os.open(lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.close(fd)
            break
        except FileExistsError:
            if time.time() - start > timeout:
                raise TimeoutError(f"Timeout acquiring lock for {path}")
            time.sleep(poll)
    try:
        yield
    finally:
        try:
            os.remove(lockfile)
        except FileNotFoundError:
            pass
