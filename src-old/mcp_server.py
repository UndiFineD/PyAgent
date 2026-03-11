r"""LLM_CONTEXT_START

## Source: src-old/mcp_server.description.md

# Description: `mcp_server.py`

## Module purpose

(No module docstring found)

## Location
- Path: `src\mcp_server.py`

## Public surface
- Classes: (none)
- Functions: init_openspec, create_sdd_spec, confirm_proceed, create_task, store_memory

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `fastapi`, `fastapi_mcp`, `src.classes.specialized.SpecToolAgent`, `src.classes.specialized.GraphMemoryAgent`, `uvicorn`

## Metadata

- SHA256(source): `4e102647e274573a`
- Last updated: `2026-01-08 22:51:34`
- File: `src\mcp_server.py`
## Source: src-old/mcp_server.improvements.md

# Improvements: `mcp_server.py`

## Suggested improvements

- Add a concise module docstring describing purpose / usage.
- Function `confirm_proceed` is missing type annotations.
- Function `create_sdd_spec` is missing type annotations.
- Function `create_task` is missing type annotations.
- Function `init_openspec` is missing type annotations.
- Function `store_memory` is missing type annotations.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\mcp_server.py`

LLM_CONTEXT_END
"""

from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from src.classes.specialized.GraphMemoryAgent import GraphMemoryAgent
from src.classes.specialized.SpecToolAgent import SpecToolAgent

app = FastAPI(title="PyAgent MCP Server")
mcp = FastApiMCP(app)

# Initialize agents


__logic_category__ = "General"
spec_agent = SpecToolAgent("spec_agent")
memory_agent = GraphMemoryAgent("memory_agent")


@mcp.tool()
def init_openspec() -> str:
    """Initializes the OpenSpec directory structure."""
    return spec_agent.init_openspec()


@mcp.tool()
def create_sdd_spec(feature_name: str, details: str) -> str:
    """Creates a SPECIFICATION.md for the planned changes."""
    return spec_agent.generate_sdd_spec(feature_name, details)


@mcp.tool()
def confirm_proceed(confirmation: str) -> str:
    """Verifies the proceed command and unlocks implementation."""
    return spec_agent.confirm_proceed(confirmation)


@mcp.tool()
def create_task(title: str, parent_id: str = None) -> str:
    """Creates a new task in the Beads graph."""
    return memory_agent.create_task(title, parent_id)


@mcp.tool()
def store_memory(category: str, name: str, data: str) -> str:
    """Stores a MIRIX memory."""
    return memory_agent.store_mirix_memory(category, name, data)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
