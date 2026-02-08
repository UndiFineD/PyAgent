# PyAgent AI Coding Instructions (VOYAGER STABILITY)

## Environment & Tooling
- Use PowerShell only; do not generate bash scripts.
- `grep` and `sed` are unavailable; use `rg` (ripgrep) for earch.
- max-line-length=120

## Architecture & Design Patterns
PyAgent is a multi-agent swarm system optimized for autonomous code improvement.
- **Mixin-Based Agents**: The `BaseAgent` (and derivatives) follows a mixin architecture found in `src/core/base/mixins/`. Do not bloat Agent classes; delegate to existing or new mixins.
- **Core/Agent Separation**: Domain logic must reside in a separate `*Core` class (e.g., `CoderCore`) to allow for performance optimization (e.g., Rust FFI bridge). The Agent class should only handle orchestration, AI prompting, and state.
- **Synaptic Modularization**: Favor composition and mixins over deep inheritance.
- **Rust Acceleration**: Use `rust_core/` for high-throughput tasks like metrics calculation, bulk file replacement, and complexity analysis.

## Coding Conventions

Every Python file should have the following header once:
```python
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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
```

- **Naming**:
  - **Modules**: Always use `snake_case` for filenames (e.g., `coder_agent.py`, `identity_mixin.py`).
  - **Classes**: Always use `PascalCase` (e.g., `CoderAgent`).
  - **Specific Naming Rules**:
    - `QuantumScalingCoderAgent` must be in `quantum_scaling_coder_agent.py`.
    - Tests for it must be in `tests/specialists/test_quantum_scaling_coder_agent.py`.
  - **Variables/Methods**: Use `snake_case`.

- **Imports**: Modules should be imported using their `snake_case` filenames, even on Windows.
- **Concurrency**: Use `asyncio` for all I/O, network requests, and subprocess execution.
- **Transactional FS**: Use `StateTransaction` from `src/core/base/agent_state_manager.py` for all file-system modifications to ensure atomicity and rollback capability.
- **Context Lineage**: Use `CascadeContext` from `src/core/base/models/communication_models.py` to prevent infinite recursion and ensure task attribution in the swarm.

## Workflows & Tools
- **Testing**: Run comprehensive tests using `pytest tests/`. Use fixtures from `tests/conftest.py` for agent sandboxing.
- **CLI Interaction**: Entry point is `src/interface/ui/cli/pyagent_cli.py`.
- **API/Web**: Entry point is `src/interface/ui/web/py_agent_web.py` (Fleet Load Balancer).
- **Tool Discovery**: Discover external tools via the MCP protocol using `MCPAgent`.

## Core Components for Reference
- `src/core/base/base_agent.py`: Principal agent interface.
- `src/core/base/agent_state_manager.py`: FS transaction integrity.
- `src/core/base/models/communication_models.py`: Task lineage and priority.
- `docs/ARCHITECTURE.md`: High-level system design.
- `docs/AGENTS.md`: Full catalog of specialized agents.
- `rust_core/`: Performance-critical logic.
