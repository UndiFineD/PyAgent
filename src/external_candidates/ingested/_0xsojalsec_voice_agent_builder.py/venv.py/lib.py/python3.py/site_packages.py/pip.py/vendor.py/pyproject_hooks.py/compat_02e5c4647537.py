# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-voice-agent-builder\venv\lib\python3.11\site-packages\pip\_vendor\pyproject_hooks\_compat.py
__all__ = ("tomllib",)

import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    from pip._vendor import tomli as tomllib
