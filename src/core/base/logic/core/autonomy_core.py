"""
Core logic for Agent Autonomy and Self-Model.
(Facade for src.core.base.common.autonomy_core)
"""

from src.core.base.common.autonomy_core import AutonomyCore as StandardAutonomyCore


class AutonomyCore(StandardAutonomyCore):
    """
    Facade for StandardAutonomyCore to maintain backward compatibility.
    Autonomy logic is now centralized in the Infrastructure/Common tier.
    """
    pass
