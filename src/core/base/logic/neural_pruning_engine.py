"""
Engine for neural synaptic pruning.
(Facade for src.core.base.common.pruning_core)
"""

<<<<<<< HEAD

"""
Engine for neural synaptic pruning.
(Facade for src.core.base.common.pruning_core)
"""

from src.core.base.common.pruning_core import \
    PruningCore as NeuralPruningEngine
from src.core.base.common.pruning_core import SynapticWeight

__all__ = ["NeuralPruningEngine", "SynapticWeight"]
=======
from src.core.base.common.pruning_core import (
    PruningCore as NeuralPruningEngine,
    SynapticWeight
)
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
