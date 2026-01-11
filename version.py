"""
Unified Version Gatekeeper for PyAgent.
Redirects to the core versioning logic in src/core/base/version.py.
"""

from src.core.base.version import (
    VERSION,
    SDK_VERSION,
    EVOLUTION_PHASE,
    STABILITY_SCORE,
    COMPATIBLE_CORE_VERSIONS,
    is_gate_open
)

__version__ = VERSION
