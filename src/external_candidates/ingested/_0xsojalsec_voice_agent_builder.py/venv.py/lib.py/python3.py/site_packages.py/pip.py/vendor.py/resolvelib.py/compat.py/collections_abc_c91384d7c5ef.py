# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-voice-agent-builder\venv\lib\python3.11\site-packages\pip\_vendor\resolvelib\compat\collections_abc.py
__all__ = ["Mapping", "Sequence"]

try:
    from collections.abc import Mapping, Sequence
except ImportError:
    from collections import Mapping, Sequence
