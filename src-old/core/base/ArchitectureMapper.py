# c:\DEV\PyAgent\src\core\base\ArchitectureMapper.py
# Evolution Phase 236: Documentation Architecture - Mermaid C4 System Context Diagram

"""LLM_CONTEXT_START

## Source: src-old/core/base/ArchitectureMapper.description.md

# ArchitectureMapper

**File**: `src\\core\base\\ArchitectureMapper.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 90  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for ArchitectureMapper.

## Classes (1)

### `ArchitectureMapper`

Auto-generates a Mermaid C4 System Context Diagram based on the PyAgent project structure.
Maps relations between Core, Infrastructure, Logic, and Observability.

**Methods** (3):
- `__init__(self, workspace_root)`
- `generate_diagram(self)`
- `run(self)`

## Dependencies

**Imports** (2):
- `os`
- `pathlib.Path`

---
*Auto-generated documentation*
## Source: src-old/core/base/ArchitectureMapper.improvements.md

# Improvements for ArchitectureMapper

**File**: `src\\core\base\\ArchitectureMapper.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 90 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ArchitectureMapper_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

import os
from pathlib import Path


class ArchitectureMapper:
    """Auto-generates a Mermaid C4 System Context Diagram based on the PyAgent project structure.
    Maps relations between Core, Infrastructure, Logic, and Observability.
    """

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.output_path = (
            self.workspace_root / "docs" / "architecture" / "system_context.md"
        )

    def generate_diagram(self) -> str:
        """Constructs the Mermaid C4 diagram string."""
        mermaid = [
            "C4Context",
            "    title System Context diagram for PyAgent Fleet",
            "    ",
            '    Person(dev, "Developer", "Lead Architect evolving the Swarm Intelligence.")',
            '    Person(admin, "Administrator", "Manages deployments and fleet health.")',
            "    ",
            '    Enterprise_Boundary(b0, "PyAgent Swarm") {',
            '        System(core, "Core Logic", "Versioning, Dependency Resolving, BLAKE3 Hashing.")',
            '        System(infra, "Infrastructure", "Fleet Manager, Sharding Orchestrator, Storage.")',
            '        System(logic, "Logic Agents", "Cognitive, Development, and Security Agents.")',
            '        System(obs, "Observability", "Structured Logging, Telemetry, and Metrics.")',
            "    }",
            "    ",
            '    System_Ext(llm, "LLM Providers", "GitHub Models, OpenAI, Ollama, VLLM.")',
            '    System_Ext(github, "GitHub", "Version control and Pull Request management.")',
            '    System_Ext(fs, "File System", "Local workspace where the agents operate.")',
            "    ",
            '    Rel(dev, core, "Defines evolving patterns")',
            '    Rel(dev, logic, "Instructs tasks via prompt.txt")',
            '    Rel(admin, infra, "Monitors resource usage")',
            "    ",
            '    Rel(core, infra, "Provides base classes & versions")',
            '    Rel(infra, logic, "Orchestrates agent execution batches")',
            '    Rel(logic, core, "Uses shared interfaces")',
            '    Rel(logic, fs, "Reads/Writes project files")',
            '    Rel(logic, llm, "Requests reasoning & code gen")',
            '    Rel(infra, github, "Creates branches and PRs")',
            '    Rel_D(logic, obs, "Emits events & telemetry")',
            '    Rel_U(obs, core, "Provides self-healing feedback")',
            "    ",
            '    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")',
        ]
        return "\n".join(mermaid)

    def run(self) -> None:
        """Generates and saves the markdown file."""
        print("[*] Mapping PyAgent architecture...")
        diagram = self.generate_diagram()

        md_content = f"""# Architecture: System Context

This diagram provides a high-level overview of the PyAgent Fleet architecture, mapping the inter-dependencies between major system boundaries.

## System Context Diagram

```mermaid
{diagram}
```

## Boundaries

| Boundary | Description | Key Modules |
|----------|-------------|-------------|
| **Core** | Fundamental logic, versioning, and workspace integrity. | `DependencyGraph`, `IncrementalProcessor`, `version.py` |
| **Infrastructure** | Fleet orchestration, sharding, and external resource management. | `AsyncFleetManager`, `ShardingOrchestrator`, `SecretManager` |
| **Logic** | The specialized agents performing the evolution tasks. | `CognitiveAgents`, `CoderAgent`, `SecurityAuditAgent` |
| **Observability** | Telemetry, logging, and metrics aggregation. | `StructuredLogger`, `OTelManager`, `GPUMonitor` |

---
*Generated automatically by `ArchitectureMapper.py` (Phase 236)*
"""

        os.makedirs(self.output_path.parent, exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"[+] Architecture map generated: {self.output_path}")


if __name__ == "__main__":
    mapper = ArchitectureMapper(os.getcwd())
    mapper.run()
