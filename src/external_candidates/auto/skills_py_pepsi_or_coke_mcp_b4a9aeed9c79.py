# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\jjannet.py\pepsi_or_coke_mcp.py\pepsi_or_coke_mcp_b4a9aeed9c79.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\jjannet\pepsi-or-coke-mcp\pepsi_or_coke_mcp.py

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pepsi_or_coke_mcp")

@mcp.tool()
def choose_pepsi_or_coke() -> str:
    """

    Decide between Pepsi or Coke.

    """

    return "Coke"

if __name__ == "__main__":
    mcp.run()
