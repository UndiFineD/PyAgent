# Gemini Integration Guide (PyAgent)

## Purpose
This file defines how PyAgent should use Gemini models for planning, coding, and review tasks.
It is the source of truth for Gemini-specific behavior, prompt contract, and output expectations.

## Scope
- Applies to all Gemini-backed agent calls in this repository.
- Covers:
  - prompt structure
  - response format
  - tool usage boundaries
  - retry and fallback behavior
  - safety and quality rules

## Model Selection
- Primary: `gemini-2.5-flash` for fast iterative edits and summaries.
- Secondary: `gemini-3.1-pro` for complex reasoning and architecture tasks.
- Use deterministic settings for code edits when possible.

## Prompt Contract
Every Gemini request should include:
1. **Task**: Exact requested outcome.
2. **Context**: Relevant files, errors, and constraints only.
3. **Constraints**:
   - Follow repository coding instructions.
   - max-line-length=120
   - Windows + PowerShell commands
4. **Output format**:
   - concise explanation
   - patch-ready code blocks
   - explicit file paths

## Output Requirements
Gemini responses should:
- Prefer minimal, safe diffs.
- Preserve existing architecture patterns:
  - mixin-based agents
  - core/agent separation (`*Core` for domain logic)
- Avoid unrelated refactors.
- Include tests for behavior changes.

## Repository Coding Instructions (PyAgent / VOYAGER STABILITY)

### Environment and Tooling
- Use **PowerShell** commands on Windows.
- Do **not** generate Bash scripts.
- `grep` is not available; use **ripgrep** (`rg`).
- `max-line-length=120`.

### Architecture and Design
- PyAgent is a multi-agent swarm optimized for autonomous code improvement.
- Follow **Mixin-Based Agents** (`src/core/base/mixins/`); avoid bloating Agent classes.
- Enforce **Core/Agent separation**:
  - Domain logic in `*Core` classes (e.g., `CoderCore`).
  - Agent classes handle orchestration, prompting, and state only.
- Prefer composition/mixins over deep inheritance (**Synaptic Modularization**).
- Use `rust_core/` for high-throughput tasks (metrics, bulk replace, complexity analysis).

### Python File Header Requirement
Every Python file must include this header once:

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

### Naming and Imports
- Modules/files: `snake_case` (e.g., `coder_agent.py`).
- Classes: `PascalCase` (e.g., `CoderAgent`).
- Variables/methods: `snake_case`.
- `QuantumScalingCoderAgent` must be in `quantum_scaling_coder_agent.py`.
- Tests for it must be in `tests/specialists/test_quantum_scaling_coder_agent.py`.
- Imports must use `snake_case` module names, including on Windows.

### Concurrency and State Safety
- Use `asyncio` for I/O, network requests, and subprocesses.
- All filesystem modifications must use:
  - `StateTransaction` from `src/core/base/agent_state_manager.py`.
- For context lineage/task attribution and recursion safety, use:
  - `CascadeContext` from `src/core/base/models/communication_models.py`.

### Workflows and Entry Points
- Run tests with: 
  - `& .\venv\Scripts\activate.ps1 ; python -m pytest -v src/ > .\pytest_results.txt 2>&1`
- Reuse fixtures from `tests/conftest.py` for sandboxing.
- CLI entry point:
  - `src/interface/ui/cli/pyagent_cli.py`
- Web/API entry point:
  - `src/interface/ui/web/py_agent_web.py`
- External tool discovery via MCP:
  - `MCPAgent`

### Core References
- `src/core/base/base_agent.py`
- `src/core/base/agent_state_manager.py`
- `src/core/base/models/communication_models.py`
- `docs/ARCHITECTURE.md`
- `docs/AGENTS.md`
- `rust_core/`

## Error Handling and Retries
- Retry transient provider/network failures with bounded exponential backoff.
- Do not retry deterministic validation errors without changing input.
- Return actionable failure messages (what failed, where, next step).

## Security and Safety
- Never include secrets in prompts or logs.
- Redact tokens, keys, and credentials from error output.
- Reject unsafe instructions that violate project or policy constraints.

## Testing Expectations
For code changes, Gemini should propose:
- unit tests for modified logic
- regression tests for bug fixes
- exact PowerShell commands to run tests:
  - `pytest tests/ -q`
  - targeted test paths where applicable

## Observability
Log per request:
- model name
- token usage (if available)
- latency
- retry count
- success/failure reason

Do not log:
- API keys
- raw secrets
- full sensitive payloads

## Gemini Output Enforcement for This Repo
For any code/task response:
1. Keep changes minimal and architecture-aligned.
2. Include explicit file paths in patches.
3. Provide PowerShell test commands.
4. Avoid unrelated refactors.
5. Add/adjust tests for behavior changes and bug fixes.

## Definition of Done
A Gemini-generated change is done when:
- code is syntactically valid
- tests pass locally
- architecture constraints are respected
- response includes clear file-level diffs and verification steps
