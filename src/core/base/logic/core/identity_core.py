"""
Core logic for Agent Identity.
(Facade for src.core.base.common.identity_core)
"""

from __future__ import annotations
from src.core.base.common.identity_core import IdentityCore as StandardIdentityCore


class IdentityCore(StandardIdentityCore):
    """
    Facade for StandardIdentityCore to maintain backward compatibility.
    Identity logic is now centralized in the Infrastructure/Common tier.
    """
    pass
