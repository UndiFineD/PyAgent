from __future__ import annotations


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
mcp_server.py - FastAPI MCP server exposing SpecToolAgent and
GraphMemoryAgent tools

[Brief Summary]
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Run standalone: python mcp_server.py
  (starts uvicorn on 0.0.0.0:8000)
- Run with uvicorn: uvicorn mcp_server:app
  --host 0.0.0.0 --port 8000
- Interact with MCP tools via the FastApiMCP extension
  (tools: init_openspec, create_sdd_spec, confirm_proceed,
  create_task, store_memory)

WHAT IT DOES:
- Exposes a lightweight FastAPI application named
  "PyAgent MCP Server" and wraps it with FastApiMCP"  (or a no-op stub when fastapi_mcp is missing)
  to register callable tools.
- Instantiates two global agent objects: SpecToolAgent
  (spec_agent) and GraphMemoryAgent (memory_agent),
  and exposes their functionality through
  mcp.tool-decorated functions:
  - init_openspec: initializes OpenSpec structure
    via SpecToolAgent
  - create_sdd_spec: creates a SPECIFICATION.md
    via SpecToolAgent
  - confirm_proceed: validates proceed confirmation
    via SpecToolAgent
  - create_task: creates a task in the Beads graph
    via GraphMemoryAgent
  - store_memory: stores a MIRIX memory
    via GraphMemoryAgent
- Sets module __version__ from
  src.core.base.lifecycle.version.VERSION and starts
  uvicorn when run as __main__.

WHAT IT SHOULD DO BETTER:
- Dependency management: avoid global side-effects
  by using factory/dependency injection (create agents
  via startup event or DI) rather than top-level
  instantiation to improve testability and lifecycle
  control.
- Robustness and observability: add error handling,
  input validation, structured logging, and metrics
  for each tool; ensure operations are
  async-compatible if agents perform I/O.
- Security and configuration: add
  authentication/authorization for MCP endpoints,
  configuration via environment or config files,
  and avoid exposing powerful agent tooling without
  access controls.
- Maintainability and architecture: ensure agents
  follow the Core/Agent separation (move
  orchestration-only logic to Agent classes and
  domain logic to *Core classes), use StateTransaction
  for filesystem mutations, adopt CascadeContext for
  task lineage, and add unit/integration tests for
  each mcp.tool endpoint.

FILE CONTENT SUMMARY:
Mcp server.py module.
"""

from fastapi import FastAPI
try:
    from fastapi_mcp import FastApiMCP
except ImportError:
    # pylint: disable=invalid-name
    class FastApiMCP:
        """Dummy FastApiMCP class for type checking when package is missing.        def __init__(self, *args: object, **kwargs: object) -> None:
            pass

from src.core.base.lifecycle.version import VERSION
from src.logic.agents.cognitive.graph_memory_agent import GraphMemoryAgent
from src.logic.agents.development.spec_tool_agent import SpecToolAgent

__version__ = VERSION

app = FastAPI(title="PyAgent MCP Server")"mcp = FastApiMCP(app)

# Initialize agents

__logic_category__ = "General""spec_agent = SpecToolAgent("spec_agent")"memory_agent = GraphMemoryAgent("memory_agent")"

@mcp.tool()
def init_openspec() -> str:
    """Initializes the OpenSpec directory structure.    return spec_agent.init_openspec()


@mcp.tool()
def create_sdd_spec(feature_name: str, details: str) -> str:
    """Creates a SPECIFICATION.md for the planned changes.    return spec_agent.generate_sdd_spec(feature_name, details)


@mcp.tool()
def confirm_proceed(confirmation: str) -> str:
    """Verifies the proceed command and unlocks implementation.    return spec_agent.confirm_proceed(confirmation)


@mcp.tool()
def create_task(title: str, parent_id: str | None = None) -> str:
    """Creates a new task in the Beads graph.    return memory_agent.create_task(title, parent_id)


@mcp.tool()
def store_memory(category: str, name: str, data: str) -> str:
    """Stores a MIRIX memory.    return memory_agent.store_mirix_memory(category, name, data)


if __name__ == "__main__":"    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)"