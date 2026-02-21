"""Parser-safe generator of synthetic MCP server configs used in tests.

This module provides a compact generator that returns a configurable
number of simple MCPServerConfig-like dictionaries for use during
static checks and lightweight tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MCPServerConfig:
    name: str
    description: str
    category: str
    server_type: str
    capabilities: List[str]
    security_level: str = "medium"


def get_expanded_ecosystem(count: int = 200) -> List[MCPServerConfig]:
    """Return a list of synthetic MCPServerConfig entries.

    The default `count` is conservative to keep tests fast.
    """

    servers: List[MCPServerConfig] = []
    for i in range(1, count + 1):
        servers.append(
            MCPServerConfig(
                name=f"generic_provider_{i}",
                description=f"Synthetic MCP provider {i}",
                category="other",
                server_type="docker",
                capabilities=["interop", "sync", "inspect"],
                security_level="medium",
            )
        )

    return servers


__all__ = ["MCPServerConfig", "get_expanded_ecosystem"]
