# shell_intelligence

**File**: `src\logic\agents\security\scanners\shell_intelligence.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 128  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for shell_intelligence.

## Classes (1)

### `ShellIntelligence`

Consolidated shell payloads, upgrade logic, and stabilization techniques.

**Methods** (5):
- `get_reverse_shell_payloads(lhost, lport)`
- `get_pty_upgrade_commands()`
- `get_stty_stabilization()`
- `generate_python_agent_payload(shell)`
- `generate_obfuscated_powershell(script, level)`

## Dependencies

**Imports** (9):
- `base64`
- `gzip`
- `io`
- `random`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `zlib`

---
*Auto-generated documentation*
