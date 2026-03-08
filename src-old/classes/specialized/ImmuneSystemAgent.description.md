# ImmuneSystemAgent

**File**: `src\classes\specialized\ImmuneSystemAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 155  
**Complexity**: 8 (moderate)

## Overview

Immune System Agent for PyAgent.
Specializes in biological resilience, detecting malicious prompt injections,
and monitoring swarm health for corrupted nodes.

## Classes (1)

### `ImmuneSystemAgent`

**Inherits from**: BaseAgent

Detects and mitigates security threats and prompt injections across the swarm.

**Methods** (8):
- `__init__(self, path)`
- `trigger_self_healing(self, node_id, issue_type)`
- `scan_for_injections(self, input_text)`
- `monitor_swarm_behavior(self, agent_logs)`
- `quarantine_node(self, agent_id)`
- `sanitize_input(self, input_text)`
- `propose_autonomous_patch(self, vulnerability, insecure_code)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `logging`
- `re`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
