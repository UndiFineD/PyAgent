# Description: `agent-context.py`

## Module purpose
Context Agent: Improves and updates code file descriptions.

Reads a context file (Codefile.description.md), uses Copilot to enhance the description,
and updates the context file with improvements.

# Description
This module provides a Context Agent that reads existing code file descriptions,
uses AI assistance to improve and complete them, and updates the context files
with enhanced documentation.

# Changelog
- 1.0.0: Initial implementation

# Suggested Fixes
- Add validation for context file format
- Improve prompt engineering for better descriptions

# Improvements
- Better integration with other agents
- Enhanced diff reporting

## Location
- Path: `scripts/agent/agent-context.py`

## Public surface
- Classes: ContextAgent
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `pathlib`, `typing`, `base_agent`

## File fingerprint
- SHA256(source): `0196e7229ebfa5b2…`
