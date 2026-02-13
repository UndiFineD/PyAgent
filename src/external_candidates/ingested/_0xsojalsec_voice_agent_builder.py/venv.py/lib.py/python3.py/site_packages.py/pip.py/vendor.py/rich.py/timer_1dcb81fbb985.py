# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-voice-agent-builder\venv\lib\python3.11\site-packages\pip\_vendor\rich\_timer.py
"""
Timer context manager, only used in debug.

"""

import contextlib
from time import time
from typing import Generator


@contextlib.contextmanager
def timer(subject: str = "time") -> Generator[None, None, None]:
    """print the elapsed time. (only used in debugging)"""
    start = time()
    yield
    elapsed = time() - start
    elapsed_ms = elapsed * 1000
    print(f"{subject} elapsed {elapsed_ms:.1f}ms")
