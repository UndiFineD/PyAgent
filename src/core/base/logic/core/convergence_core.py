"""
Core logic for Fleet Convergence and Health Management.
(Facade for src.core.base.common.convergence_core)
"""

from src.core.base.common.convergence_core import ConvergenceCore as StandardConvergenceCore


class ConvergenceCore(StandardConvergenceCore):
    """
    Facade for StandardConvergenceCore to maintain backward compatibility.
    Convergence logic is now centralized in the Infrastructure/Common tier.
    """
    pass
