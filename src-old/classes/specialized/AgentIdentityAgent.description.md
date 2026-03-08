# AgentIdentityAgent

**File**: `src\classes\specialized\AgentIdentityAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 70  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for AgentIdentityAgent.

## Classes (1)

### `AgentIdentityAgent`

Manages Decentralized Identifiers (DIDs) and Verifiable Credentials (VCs)
for agents within the Swarm and across fleet boundaries.

**Methods** (4):
- `__init__(self, workspace_path)`
- `create_agent_did(self, agent_name, fleet_id)`
- `issue_verifiable_credential(self, issuer_did, subject_did, claim_type, claim_value)`
- `verify_credential(self, vc)`

## Dependencies

**Imports** (8):
- `hashlib`
- `json`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uuid`

---
*Auto-generated documentation*
