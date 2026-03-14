#!/usr/bin/env python3
"""Compatibility shim: expose version symbols at src.core.base.Version

This file mirrors src.core.base.version to support imports that use the
uppercase module name `Version`.
"""

from src.core.base.lifecycle.version import (
    COMPATIBLE_CORE_VERSIONS,
    EVOLUTION_PHASE,
    GOLDEN_MASTER_SEAL,
    SDK_VERSION,
    STABILITY_SCORE,
    VERSION,
    is_gate_open,
)

__all__ = [
    "VERSION",
    "SDK_VERSION",
    "EVOLUTION_PHASE",
    "STABILITY_SCORE",
    "GOLDEN_MASTER_SEAL",
    "COMPATIBLE_CORE_VERSIONS",
    "is_gate_open",
]
#!/usr/bin/env python3
r"""Compatibility shim: expose version symbols at src.core.base.version

This file re-exports values from src.core.base.lifecycle.version so older
imports (src.core.base.version) continue to work.
"""
