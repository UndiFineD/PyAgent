"""Auto-generated module exports."""

from typing import Callable, Optional, List, Dict
# Type alias for the backend function signature
# (prompt, system_prompt, history) -> response
BackendFunction = Callable[[str, Optional[str], Optional[List[Dict[str, str]]]], str]

from .AgentStrategy import AgentStrategy
from .ChainOfThoughtStrategy import ChainOfThoughtStrategy
from .DirectStrategy import DirectStrategy
from .ReflexionStrategy import ReflexionStrategy
