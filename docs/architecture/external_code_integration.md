# External Code Integration Strategy

## Overview
PyAgent aims to be a self-sufficient, comprehensive agentic system. To accelerate development, we analyze and integrate logic from external open-source tools located in `.external/`.

## Security & Virus Warning
**CRITICAL**: The `.external` directory contains unchecked, potentially malicious code (viruses, shells, backdoors).
- **NEVER** execute code from `.external` directly.
- **NEVER** add `.external` to PYTHONPATH.
- **ALWAYS** read code as text only.
- Refactoring involves *re-implementing* the logic, not just copying the file.

## Workflow
1.  **Catalog**: All external tools are listed in `.external/tracking.md`.
2.  **Function Gap Analysis**:
    *   Identify specific functions in external tools that are missing in `src`.
    *   Record these in the "Missing Functions" column in `tracking.md`.
3.  **Map**: Identify where this functionality belongs in the PyAgent `src/` hierarchy.
4.  **Refactor**:
    *   Extract pure functions and logic.
    *   Rewrite to match PyAgent coding standards (Classes, Type Hints, specialized error handling).
    *   Remove external dependencies where possible.
5.  **Verify**: Create unit tests in `tests/` to ensure the ported logic works.
6.  **Cleanup**: Delete the source directory from `.external/` once validated.

## Integration Guidelines
- **Safety First**: Treat all external code as untrusted.
- **Do NOT copy-paste blindly.** Understanding the logic is paramount.
- **Maintain Licenses.** If code is copied, ensure license compatibility.
- **Rust Acceleration.** If a tool is performance-critical, consider porting directly to `rust_core/`.
- **Security.** Audit external code for vulnerabilities before integration.

## Current Focus Areas
- **Network Scanning & Discovery**: Integration from `netscan`, `nmap` related tools.
- **LLM Context Management**: Integration from `memgpt` or context-window tools.
- **Exploit/Security Tools**: Integration into `src/logic/security/` (for Red Teaming agents).
