"""idea206564 - orjson-3.11.6-cp312-cp312-macosx-10-15-x86-64.macosx-11-0-arm64.macosx-10-15-universal2

Auto-generated implementation from idea: idea206564
"""

__version__ = "0.1.0"
__author__ = "PyAgent Implementation Engine"

from .core import execute, initialize, main, shutdown
from .utils import *

__all__ = [
    'main',
    'execute',
    'initialize',
    'shutdown',
    '__version__',
]

# Module initialization
_initialized = False

def init():
    """Initialize the module"""
    global _initialized
    if not _initialized:
        initialize()
        _initialized = True

# Auto-init on import
init()
