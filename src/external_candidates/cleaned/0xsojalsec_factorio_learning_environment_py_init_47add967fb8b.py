# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\protocols.py\mcp.py\init_47add967fb8b.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\protocols\_mcp\__init__.py

"""MCP protocol implementation for Factorio Learning Environment."""

from collections.abc import AsyncIterator

# ruff: noqa: E402

from contextlib import asynccontextmanager

from dataclasses import dataclass

from fastmcp import FastMCP

# Create the MCP server instance FIRST

mcp = FastMCP(
    "Factorio Learning Environment",
    dependencies=["dulwich", "numpy", "pillow"],
)

# Now import other modules that use mcp

from fle.env.protocols._mcp.init import initialize_session, shutdown_session, state

from fle.env.protocols._mcp.state import FactorioMCPState


@dataclass
class FactorioContext:
    """Factorio server context available during MCP session"""

    connection_message: str

    state: FactorioMCPState


@asynccontextmanager
async def fle_lifespan(server) -> AsyncIterator[FactorioContext]:
    """Manage the Factorio server lifecycle within the MCP session"""

    connection_message = await initialize_session()

    context = FactorioContext(connection_message=connection_message, state=state)

    try:
        yield context

    finally:
        await shutdown_session()


# Attach the lifespan to mcp

mcp.lifespan = fle_lifespan

# Export mcp for other modules

__all__ = ["mcp", "FactorioContext", "initialize_session", "shutdown_session", "state"]
