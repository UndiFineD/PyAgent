"""Conservative agent config stubs for repair.

These minimal implementations restore importability while repairs
continue across the codebase.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class AgentConfig:
    name: str = "unknown"
    enabled: bool = True
    metadata: Dict[str, Any] | None = None


def load_agent_config(path: str) -> AgentConfig:
    """Conservative stub that returns an AgentConfig for `path`.

    This does not perform IO during repair runs.
    """
    return AgentConfig(name=path, enabled=True, metadata=None)
