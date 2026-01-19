# SPDX-License-Identifier: Apache-2.0
"""
Mamba SSM Package - Implementation of State Space Models.
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .config import MambaConfig, MambaState, MambaOutput
    from .mixer import MambaMixer, Mamba2Mixer
    from .hybrid import HybridMambaMixer
    from .ops import CausalConv1d, SelectiveScan

def __getattr__(name: str) -> Any:
    if name in ("MambaConfig", "MambaState", "MambaOutput"):
        from .config import MambaConfig, MambaState, MambaOutput
        return locals()[name]
    if name in ("MambaMixer", "Mamba2Mixer"):
        from .mixer import MambaMixer, Mamba2Mixer
        return locals()[name]
    if name == "HybridMambaMixer":
        from .hybrid import HybridMambaMixer
        return HybridMambaMixer
    if name in ("CausalConv1d", "SelectiveScan"):
        from .ops import CausalConv1d, SelectiveScan
        return locals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "MambaConfig",
    "MambaState",
    "MambaOutput",
    "MambaMixer",
    "Mamba2Mixer",
    "HybridMambaMixer",
    "CausalConv1d",
    "SelectiveScan",
]

