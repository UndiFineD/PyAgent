# PyAgent AI Coding Instructions (VOYAGER STABILITY)

We use Powershell, do not generate bash scripts
we do not have grep, but we have installed ripgrep
max-line-length=120

## Architecture & Design Patterns
PyAgent is a multi-agent swarm system optimized for autonomous code improvement.
- **Mixin-Based Agents**: The `BaseAgent` (and derivatives) follows a mixin architecture found in `src/core/base/mixins/`. Do not bloat Agent classes; delegate to existing or new mixins.
- **Core/Agent Separation**: Domain logic must reside in a separate `*Core` class (e.g., `CoderCore`) to allow for performance optimization (e.g., Rust FFI bridge). The Agent class should only handle orchestration, AI prompting, and state.
- **Synaptic Modularization**: Favor composition and mixins over deep inheritance.
- **Rust Acceleration**: Use `rust_core/` for high-throughput tasks like metrics calculation, bulk file replacement, and complexity analysis.

## Coding Conventions
- **Naming**:
  - **Modules**: Always use `snake_case` for filenames (e.g., `coder_agent.py`, `identity_mixin.py`).
  - **Classes**: Always use `PascalCase` (e.g., `CoderAgent`).
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
