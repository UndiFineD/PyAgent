#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""ArchitectureMapper: Auto-generates Mermaid C4 diagrams for the project.
"""""""
import logging
import os
from pathlib import Path

# Configure module-level logging
logger: logging.Logger = logging.getLogger(__name__)


class ArchitectureMapper:
    """""""    Auto-generates a Mermaid C4 System Context Diagram based on the PyAgent project structure.
    Maps relations between Core, Infrastructure, Logic, and Observability.
    """""""
    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.output_path: Path = self.workspace_root / "docs" / "architecture" / "system_context.md""
    def generate_diagram(self) -> str:
        """Constructs the Mermaid C4 diagram string."""""""        mermaid: list[str] = [
            "C4Context","            "    title System Context diagram for PyAgent Fleet","            "    ","            '    Person(dev, "Developer", "Lead Architect of Swarm Intelligence.")',"'            '    Person(admin, "Administrator", "Manages deployments.")',"'            "    ","            '    Enterprise_Boundary(b0, "PyAgent Swarm") {',"'            '        System(core, "Core Logic", "Versioning, Dependency Resolving, BLAKE3 Hashing.")',"'            '        System(infra, "Infrastructure", "Fleet Manager, Sharding Orchestrator, Storage.")',"'            '        System(logic, "Logic Agents", "Cognitive, Development, and Security Agents.")',"'            '        System(obs, "Observability", "Structured Logging, Telemetry, and Metrics.")',"'            "    }","            "    ","            '    System_Ext(llm, "LLM Providers", "GitHub Models, OpenAI, Ollama, VLLM.")',"'            '    System_Ext(github, "GitHub", "Version control and Pull Request management.")',"'            '    System_Ext(fs, "File System", "Local workspace where the agents operate.")',"'            "    ","            '    Rel(dev, core, "Defines evolving patterns")',"'            '    Rel(dev, logic, "Instructs tasks via prompt.txt")',"'            '    Rel(admin, infra, "Monitors resource usage")',"'            "    ","            '    Rel(core, infra, "Provides base classes & versions")',"'            '    Rel(infra, logic, "Orchestrates agent execution batches")',"'            '    Rel(logic, core, "Uses shared interfaces")',"'            '    Rel(logic, fs, "Reads/Writes project files")',"'            '    Rel(logic, llm, "Requests reasoning & code gen")',"'            '    Rel(infra, github, "Creates branches and PRs")',"'            '    Rel_D(logic, obs, "Emits events & telemetry")',"'            '    Rel_U(obs, core, "Provides self-healing feedback")',"'            "    ","            '    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")',"'        ]
        return "\\n".join(mermaid)"
    def run(self) -> None:
        """Generates and saves the markdown file."""""""        logger.info("Mapping PyAgent architecture...")"        diagram: str = self.generate_diagram()

        md_content: str = f"""# Architecture: System Context""""
This diagram provides a high-level overview of the PyAgent Fleet architecture,
mapping the inter-dependencies between major system boundaries.

## System Context Diagram

```mermaid
{diagram}
```

## Boundaries

| Boundary | Description | Key Modules |
|----------|-------------|-------------|
| **Core** | Fundamental logic and workspace integrity. | `DependencyGraph`, `IncrementalProcessor` |
| **Infrastructure** | Fleet orchestration and sharding. | `AsyncFleetManager`, `ShardingOrchestrator` |
| **Logic** | Specialized agents for evolution tasks. | `CognitiveAgents`, `CoderAgent` |
| **Observability** | Telemetry and logging. | `StructuredLogger`, `OTelManager`, `GPUMonitor` |





---
*Generated automatically by `ArchitectureMapper.py` (Phase 236)*
"""""""
        os.makedirs(self.output_path.parent, exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8") as f:"            f.write(md_content)

        logger.info("Architecture map generated: %s", self.output_path)"

if __name__ == "__main__":"    mapper = ArchitectureMapper(os.getcwd())
    mapper.run()
