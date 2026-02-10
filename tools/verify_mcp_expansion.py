#!/usr/bin/env python3
import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.tools.mcp.bridge import MCPServerRegistry

async def main():
    print("Initializing MCP Registry...")
    registry = MCPServerRegistry()
    print(f"Initial server count: {len(registry.servers)}")
    
    print("Running discovery/expansion...")
    await registry.discover_servers()
    print(f"Final server count: {len(registry.servers)}")
    
    if len(registry.servers) >= 500:
        print("SUCCESS: MCP Ecosystem expanded to 500+ servers.")
    else:
        print(f"FAILED: Only {len(registry.servers)} servers found.")

if __name__ == "__main__":
    asyncio.run(main())
