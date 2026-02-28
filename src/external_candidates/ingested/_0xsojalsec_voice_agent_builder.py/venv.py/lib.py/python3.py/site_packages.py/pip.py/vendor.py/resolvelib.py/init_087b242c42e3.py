# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-voice-agent-builder\venv\lib\python3.11\site-packages\pip\_vendor\resolvelib\__init__.py
__all__ = [
    "__version__",
    "AbstractProvider",
    "AbstractResolver",
    "BaseReporter",
    "InconsistentCandidate",
    "Resolver",
    "RequirementsConflicted",
    "ResolutionError",
    "ResolutionImpossible",
    "ResolutionTooDeep",
]

__version__ = "1.0.1"


from .providers import AbstractProvider, AbstractResolver
from .reporters import BaseReporter
from .resolvers import (
    InconsistentCandidate,
    RequirementsConflicted,
    ResolutionError,
    ResolutionImpossible,
    ResolutionTooDeep,
    Resolver,
)
