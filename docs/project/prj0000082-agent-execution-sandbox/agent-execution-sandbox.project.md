# agent-execution-sandbox

**Project ID:** `prj0000082-agent-execution-sandbox`

## Links

- Plan: `plan.md`
- Design: `brainstorm.md`

## Tasks

- [ ] Define `SandboxConfig` dataclass with `allowed_paths: list[Path]` and `allowed_hosts: list[str]`
- [ ] Implement `SandboxMixin` that reads config and validates every StorageTransaction path
- [ ] Raise `SandboxViolationError` on any unauthorized path or host access
- [ ] Integrate with existing `StateTransaction` validation hook
- [ ] Achieve ≥90% test coverage on sandbox module
- [ ] Zero regressions in existing 129+ structure tests

## Status

0 of 6 tasks completed

## Code detection

- Code detected in:
  - `rust_core\src\agents.rs`
  - `scripts\AgentDocFrequency.py`
  - `src\agents\BaseAgent.py`
  - `src\agents\specialization\specialized_agent_adapter.py`
  - `src\core\agent_registry.py`
  - `src\core\agent_state_manager.py`
  - `src\core\base\mixins\sandbox_mixin.py`
  - `src\core\reasoning\CortAgent.py`
  - `src\core\replay\ShadowExecutionCore.py`
  - `src\core\sandbox\SandboxConfig.py`
  - `src\core\sandbox\SandboxedStorageTransaction.py`
  - `src\core\sandbox\SandboxMixin.py`
  - `src\core\sandbox\SandboxViolationError.py`
  - `src\core\universal\UniversalAgentShell.py`
  - `src\mcp\McpSandbox.py`
  - `src\swarm\agent_registry.py`
  - `src\tools\agent_plugins.py`
  - `tests\agents\specialization\test_specialized_agent_adapter.py`
  - `tests\agents\test_agents.py`
  - `tests\agents\test_base_agent.py`
  - `tests\core\universal\test_universal_agent_shell_specialization_flag.py`
  - `tests\docs\test_agent_workflow_policy_docs.py`
  - `tests\test_agent_doc_frequency.py`
  - `tests\test_agent_memory.py`
  - `tests\test_agent_registry.py`
  - `tests\test_core_agent_registry.py`
  - `tests\test_core_agent_state_manager.py`
  - `tests\test_core_base_mixins_sandbox_mixin.py`
  - `tests\test_pipeline_execution.py`
  - `tests\test_sandbox.py`
  - `tests\test_SandboxConfig.py`
  - `tests\test_SandboxedStorageTransaction.py`
  - `tests\test_SandboxMixin.py`
  - `tests\test_SandboxViolationError.py`
  - `tests\test_ShadowExecutionCore.py`
  - `tests\test_swarm_agent_registry.py`
  - `tests\test_UniversalAgentShell.py`
  - `tests\unit\test_CortAgent.py`
  - `tests\unit\test_McpSandbox.py`