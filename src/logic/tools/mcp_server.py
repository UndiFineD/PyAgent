# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Mcp server.py module.
"""


from __future__ import annotations

from fastapi import FastAPI
try:
    from fastapi_mcp import FastApiMCP
except ImportError:
    # pylint: disable=invalid-name
    class FastApiMCP:
        """Dummy FastApiMCP class for type checking when package is missing."""
        def __init__(self, *args: object, **kwargs: object) -> None:
            pass

from src.core.base.lifecycle.version import VERSION
from src.logic.agents.cognitive.graph_memory_agent import GraphMemoryAgent
from src.logic.agents.development.spec_tool_agent import SpecToolAgent

__version__ = VERSION

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
def create_task(title: str, parent_id: str | None = None) -> str:
    """Creates a new task in the Beads graph."""
    return memory_agent.create_task(title, parent_id)


@mcp.tool()
def store_memory(category: str, name: str, data: str) -> str:
    """Stores a MIRIX memory."""
    return memory_agent.store_mirix_memory(category, name, data)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
