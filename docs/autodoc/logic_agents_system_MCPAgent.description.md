# Description: `MCPAgent.py`

## Module purpose

Agent specializing in Model Context Protocol (MCP) integration.
Acts as a bridge between the PyAgent fleet and external MCP servers.
Inspired by mcp-server-spec-driven-development and awesome-mcp-servers.

## Location
- Path: `logic\agents\system\MCPAgent.py`

## Public surface
- Classes: MCPAgent
- Functions: (none)

## Behavior summary
- Invokes external commands via `subprocess`.

## Key dependencies
- Top imports: `json`, `logging`, `subprocess`, `pathlib`, `typing`, `src.core.base.BaseAgent`, `src.core.base.utilities`, `src.infrastructure.fleet.MCPConnector`

## Metadata

- SHA256(source): `53e66ab5b4250565`
- Last updated: `2026-01-11 12:54:48`
- File: `logic\agents\system\MCPAgent.py`