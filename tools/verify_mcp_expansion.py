#!/usr/bin/env python3
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

import asyncio
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
