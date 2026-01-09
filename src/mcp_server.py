from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from src.classes.specialized.SpecToolAgent import SpecToolAgent
from src.classes.specialized.GraphMemoryAgent import GraphMemoryAgent

app = FastAPI(title="PyAgent MCP Server")
mcp = FastApiMCP(app)

# Initialize agents
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
