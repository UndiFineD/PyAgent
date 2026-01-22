"""
Core logic for Error Mapping.
(Facade for src.core.base.common.error_mapping_core)
"""

<<<<<<< HEAD
"""
Core logic for Error Mapping.
(Facade for src.core.base.common.error_mapping_core)
"""

from src.core.base.common.error_mapping_core import \
    ErrorMappingCore as StandardErrorMappingCore
=======
from src.core.base.common.error_mapping_core import ErrorMappingCore as StandardErrorMappingCore
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)


class ErrorMappingCore(StandardErrorMappingCore):
    """
    Facade for StandardErrorMappingCore to maintain backward compatibility.
    Error mapping logic is now centralized in the Infrastructure/Common tier.
    """
<<<<<<< HEAD
=======
    pass
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
