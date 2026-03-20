# prj037-tools-crdt-security — 8QL Security Scan

_Status: IN_PROGRESS_
_Scanner: @8ql | Updated: 2026-03-20T07:57:09Z_


## Scan Scope
| File | Scan type | Tool |
|---|---|---|
| .env.template | CodeQL | code_quality + codeql |
| .github/agents/0master.agent.md | CodeQL | code_quality + codeql |
| .github/agents/1project.agent.md | CodeQL | code_quality + codeql |
| .github/agents/8ql.agent.md | CodeQL | code_quality + codeql |
| .github/workflows/backlinks.yml | CodeQL | code_quality + codeql |
| .github/workflows/ci-crossplatform.yml | CodeQL | code_quality + codeql |
| .github/workflows/ci-docs.yml | CodeQL | code_quality + codeql |
| .github/workflows/ci-python-api.yml | CodeQL | code_quality + codeql |
| .github/workflows/ci-python-core.yml | CodeQL | code_quality + codeql |
| .github/workflows/ci-python-lint.yml | CodeQL | code_quality + codeql |
| .github/workflows/ci-python-providers.yml | CodeQL | code_quality + codeql |
| .github/workflows/ci-python-quality.yml | CodeQL | code_quality + codeql |
| .github/workflows/ci-python-rust-ext.yml | CodeQL | code_quality + codeql |
| .github/workflows/ci-python-tools.yml | CodeQL | code_quality + codeql |
| .github/workflows/ci-rust.yml | CodeQL | code_quality + codeql |
| .github/workflows/ci.yml | CodeQL | code_quality + codeql |
| .github/workflows/codeql.yml | CodeQL | code_quality + codeql |
| .github/workflows/pip-audit.yml | CodeQL | code_quality + codeql |
| .github/workflows/quality.yml | CodeQL | code_quality + codeql |
| .pre-commit-config.yaml | CodeQL | code_quality + codeql |
| MIGRATION.md | CodeQL | code_quality + codeql |
| docs/agents/0master.memory.md | CodeQL | code_quality + codeql |
| docs/agents/2think.memory.md | CodeQL | code_quality + codeql |
| docs/agents/3design.memory.md | CodeQL | code_quality + codeql |
| docs/agents/4plan.memory.md | CodeQL | code_quality + codeql |
| docs/agents/5test.memory.md | CodeQL | code_quality + codeql |
| docs/agents/6code.memory.md | CodeQL | code_quality + codeql |
| docs/agents/7exec.memory.md | CodeQL | code_quality + codeql |
| docs/agents/8ql.memory.md | CodeQL | code_quality + codeql |
| docs/agents/9git.memory.md | CodeQL | code_quality + codeql |
| docs/architecture/Architecture.generated.md | CodeQL | code_quality + codeql |
| docs/architecture/Architecture.md | CodeQL | code_quality + codeql |
| docs/architecture/overview.md | CodeQL | code_quality + codeql |
| docs/architecture/todolist.md | CodeQL | code_quality + codeql |
| docs/onboarding.md | CodeQL | code_quality + codeql |
| docs/project/PROJECT_DASHBOARD.md | CodeQL | code_quality + codeql |
| docs/project/prj001-async-runtime/async-runtime.project.md | CodeQL | code_quality + codeql |
| docs/project/prj001-async-runtime/brainstorm.md | CodeQL | code_quality + codeql |
| docs/project/prj001-async-runtime/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj001-async-runtime/prj001-async-runtime.project.md | CodeQL | code_quality + codeql |
| docs/project/prj001-conftest-typing-fixes/brainstorm.md | CodeQL | code_quality + codeql |
| docs/project/prj001-conftest-typing-fixes/conftest-typing-fixes.project.md | CodeQL | code_quality + codeql |
| docs/project/prj001-conftest-typing-fixes/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj001-conftest-typing-fixes/prj001-conftest-typing-fixes.project.md | CodeQL | code_quality + codeql |
| docs/project/prj001-core-system/brainstorm.md | CodeQL | code_quality + codeql |
| docs/project/prj001-core-system/core-system.project.md | CodeQL | code_quality + codeql |
| docs/project/prj001-core-system/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj001-core-system/prj001-core-system.project.md | CodeQL | code_quality + codeql |
| docs/project/prj002-core-system/brainstorm.md | CodeQL | code_quality + codeql |
| docs/project/prj002-core-system/core-system.project.md | CodeQL | code_quality + codeql |
| docs/project/prj002-core-system/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj002-core-system/prj002-core-system.project.md | CodeQL | code_quality + codeql |
| docs/project/prj002-flm/flm.project.md | CodeQL | code_quality + codeql |
| docs/project/prj002-flm/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj002-flm/prj002-flm.project.md | CodeQL | code_quality + codeql |
| docs/project/prj003-hybrid-llm-security/hybrid-llm-security.project.md | CodeQL | code_quality + codeql |
| docs/project/prj003-hybrid-llm-security/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj003-hybrid-llm-security/prj003-hybrid-llm-security.project.md | CodeQL | code_quality + codeql |
| docs/project/prj004-llm-context-consolidation/brainstorm.md | CodeQL | code_quality + codeql |
| docs/project/prj004-llm-context-consolidation/llm-context-consolidation.project.md | CodeQL | code_quality + codeql |
| docs/project/prj004-llm-context-consolidation/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj004-llm-context-consolidation/prj004-llm-context-consolidation.project.md | CodeQL | code_quality + codeql |
| docs/project/prj004-llm-context-consolidation/prj004-llm-context-consolidation.think.md | CodeQL | code_quality + codeql |
| docs/project/prj005-llm-swarm-architecture/llm-swarm-architecture.project.md | CodeQL | code_quality + codeql |
| docs/project/prj005-llm-swarm-architecture/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj005-llm-swarm-architecture/prj005-llm-swarm-architecture.git.md | CodeQL | code_quality + codeql |
| docs/project/prj005-llm-swarm-architecture/prj005-llm-swarm-architecture.project.md | CodeQL | code_quality + codeql |
| docs/project/prj006-unified-transaction-manager/prj006-unified-transaction-manager.project.md | CodeQL | code_quality + codeql |
| docs/project/prj006-unified-transaction-manager/unified-transaction-manager.project.md | CodeQL | code_quality + codeql |
| docs/project/prj007-advanced_research/advanced_research.project.md | CodeQL | code_quality + codeql |
| docs/project/prj007-advanced_research/prj007-advanced_research.project.md | CodeQL | code_quality + codeql |
| docs/project/prj008-agent_workflow/agent_workflow.project.md | CodeQL | code_quality + codeql |
| docs/project/prj008-agent_workflow/prj008-agent_workflow.project.md | CodeQL | code_quality + codeql |
| docs/project/prj009-community_collaboration/community_collaboration.project.md | CodeQL | code_quality + codeql |
| docs/project/prj009-community_collaboration/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj009-community_collaboration/prj009-community_collaboration.project.md | CodeQL | code_quality + codeql |
| docs/project/prj010-context_management/brainstorm.md | CodeQL | code_quality + codeql |
| docs/project/prj010-context_management/context_management.project.md | CodeQL | code_quality + codeql |
| docs/project/prj010-context_management/prj010-context_management.project.md | CodeQL | code_quality + codeql |
| docs/project/prj011-core_project_structure/core_project_structure.project.md | CodeQL | code_quality + codeql |
| docs/project/prj011-core_project_structure/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj011-core_project_structure/prj011-core_project_structure.project.md | CodeQL | code_quality + codeql |
| docs/project/prj012-deployment_operations/deployment_operations.project.md | CodeQL | code_quality + codeql |
| docs/project/prj012-deployment_operations/prj012-deployment_operations.project.md | CodeQL | code_quality + codeql |
| docs/project/prj013-dev_tools_autonomy_design/dev_tools_autonomy_design.project.md | CodeQL | code_quality + codeql |
| docs/project/prj013-dev_tools_autonomy_design/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj013-dev_tools_autonomy_design/prj013-dev_tools_autonomy_design.project.md | CodeQL | code_quality + codeql |
| docs/project/prj014-dev_tools_capabilities/dev_tools_capabilities.project.md | CodeQL | code_quality + codeql |
| docs/project/prj014-dev_tools_capabilities/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj014-dev_tools_capabilities/prj014-dev_tools_capabilities.project.md | CodeQL | code_quality + codeql |
| docs/project/prj015-dev_tools_implementation_design/dev_tools_implementation_design.project.md | CodeQL | code_quality + codeql |
| docs/project/prj015-dev_tools_implementation_design/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj015-dev_tools_implementation_design/prj015-dev_tools_implementation_design.project.md | CodeQL | code_quality + codeql |
| docs/project/prj016-dev_tools_structure_design/dev_tools_structure_design.project.md | CodeQL | code_quality + codeql |
| docs/project/prj016-dev_tools_structure_design/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj016-dev_tools_structure_design/prj016-dev_tools_structure_design.project.md | CodeQL | code_quality + codeql |
| docs/project/prj017-dev_tools_utilities/dev_tools_utilities.project.md | CodeQL | code_quality + codeql |
| docs/project/prj017-dev_tools_utilities/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj017-dev_tools_utilities/prj017-dev_tools_utilities.project.md | CodeQL | code_quality + codeql |
| docs/project/prj018-documentation_assets/brainstorm.md | CodeQL | code_quality + codeql |
| docs/project/prj018-documentation_assets/documentation_assets.project.md | CodeQL | code_quality + codeql |
| docs/project/prj018-documentation_assets/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj018-documentation_assets/prj018-documentation_assets.project.md | CodeQL | code_quality + codeql |
| docs/project/prj019-future_roadmap/future_roadmap.project.md | CodeQL | code_quality + codeql |
| docs/project/prj019-future_roadmap/prj019-future_roadmap.project.md | CodeQL | code_quality + codeql |
| docs/project/prj020-github-import/github-import.project.md | CodeQL | code_quality + codeql |
| docs/project/prj020-github-import/prj020-github-import.project.md | CodeQL | code_quality + codeql |
| docs/project/prj021-project_management_governance/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj021-project_management_governance/prj021-project_management_governance.project.md | CodeQL | code_quality + codeql |
| docs/project/prj021-project_management_governance/project_management_governance.project.md | CodeQL | code_quality + codeql |
| docs/project/prj022-swarm_architecture/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj022-swarm_architecture/prj022-swarm_architecture.project.md | CodeQL | code_quality + codeql |
| docs/project/prj022-swarm_architecture/swarm_architecture.project.md | CodeQL | code_quality + codeql |
| docs/project/prj023-testing_infrastructure/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj023-testing_infrastructure/prj023-testing_infrastructure.project.md | CodeQL | code_quality + codeql |
| docs/project/prj023-testing_infrastructure/testing_infrastructure.project.md | CodeQL | code_quality + codeql |
| docs/project/prj024-async-runtime/async-runtime.project.md | CodeQL | code_quality + codeql |
| docs/project/prj024-async-runtime/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj024-async-runtime/prj024-async-runtime.project.md | CodeQL | code_quality + codeql |
| docs/project/prj025-core-system/brainstorm.md | CodeQL | code_quality + codeql |
| docs/project/prj025-core-system/core-system.project.md | CodeQL | code_quality + codeql |
| docs/project/prj025-core-system/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj025-core-system/prj025-core-system.project.md | CodeQL | code_quality + codeql |
| docs/project/prj026-test-coverage-quality/prj026-test-coverage-quality.project.md | CodeQL | code_quality + codeql |
| docs/project/prj026-test-coverage-quality/test-coverage-quality.project.md | CodeQL | code_quality + codeql |
| docs/project/prj027-encrypted-memory-blocks/encrypted-memory-blocks.project.md | CodeQL | code_quality + codeql |
| docs/project/prj027-encrypted-memory-blocks/prj027-encrypted-memory-blocks.project.md | CodeQL | code_quality + codeql |
| docs/project/prj028-transport-t1/prj028-transport-t1.project.md | CodeQL | code_quality + codeql |
| docs/project/prj028-transport-t1/transport-t1.project.md | CodeQL | code_quality + codeql |
| docs/project/prj029-llm-ui-backend-worker/brainstorm.md | CodeQL | code_quality + codeql |
| docs/project/prj029-llm-ui-backend-worker/llm-ui-backend-worker.project.md | CodeQL | code_quality + codeql |
| docs/project/prj029-llm-ui-backend-worker/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj029-llm-ui-backend-worker/prj029-llm-ui-backend-worker.project.md | CodeQL | code_quality + codeql |
| docs/project/prj030-agent-doc-frequency/agent-doc-frequency.project.md | CodeQL | code_quality + codeql |
| docs/project/prj030-agent-doc-frequency/brainstorm.md | CodeQL | code_quality + codeql |
| docs/project/prj030-agent-doc-frequency/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj030-agent-doc-frequency/prj030-agent-doc-frequency.project.md | CodeQL | code_quality + codeql |
| docs/project/prj031-streaming-website/brainstorm.md | CodeQL | code_quality + codeql |
| docs/project/prj031-streaming-website/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj031-streaming-website/prj031-streaming-website.project.md | CodeQL | code_quality + codeql |
| docs/project/prj031-streaming-website/streaming-website.project.md | CodeQL | code_quality + codeql |
| docs/project/prj032-agents/agents.project.md | CodeQL | code_quality + codeql |
| docs/project/prj032-agents/brainstorm.md | CodeQL | code_quality + codeql |
| docs/project/prj032-agents/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj032-agents/prj032-agents.project.md | CodeQL | code_quality + codeql |
| docs/project/prj033-chat/chat.project.md | CodeQL | code_quality + codeql |
| docs/project/prj033-chat/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj033-chat/prj033-chat.project.md | CodeQL | code_quality + codeql |
| docs/project/prj034-context-manager/brainstorm.md | CodeQL | code_quality + codeql |
| docs/project/prj034-context-manager/context-manager.project.md | CodeQL | code_quality + codeql |
| docs/project/prj034-context-manager/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj034-context-manager/prj034-context-manager.project.md | CodeQL | code_quality + codeql |
| docs/project/prj035-multimodal/multimodal.project.md | CodeQL | code_quality + codeql |
| docs/project/prj035-multimodal/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj035-multimodal/prj035-multimodal.project.md | CodeQL | code_quality + codeql |
| docs/project/prj036-plugins/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj036-plugins/plugins.project.md | CodeQL | code_quality + codeql |
| docs/project/prj036-plugins/prj036-plugins.project.md | CodeQL | code_quality + codeql |
| docs/project/prj037-tools/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj037-tools/prj037-tools.project.md | CodeQL | code_quality + codeql |
| docs/project/prj037-tools/tools.project.md | CodeQL | code_quality + codeql |
| docs/project/prj038-python-function-coverage/brainstorm.md | CodeQL | code_quality + codeql |
| docs/project/prj038-python-function-coverage/plan.md | CodeQL | code_quality + codeql |
| docs/project/prj038-python-function-coverage/prj038-python-function-coverage.project.md | CodeQL | code_quality + codeql |
| docs/project/prj038-python-function-coverage/python-function-coverage.project.md | CodeQL | code_quality + codeql |
| docs/tools.md | CodeQL | code_quality + codeql |
| experiments.json | CodeQL | code_quality + codeql |
| project/PyAgent.md | CodeQL | code_quality + codeql |
| project/llms-architecture.txt | CodeQL | code_quality + codeql |
| rust_core/Cargo.lock | CodeQL | code_quality + codeql |
| rust_core/Cargo.toml | CodeQL | code_quality + codeql |
| rust_core/crdt/Cargo.lock | CodeQL | code_quality + codeql |
| rust_core/crdt/Cargo.toml | CodeQL | code_quality + codeql |
| rust_core/crdt/src/main.rs | CodeQL | code_quality + codeql |
| rust_core/p2p/Cargo.lock | CodeQL | code_quality + codeql |
| rust_core/p2p/Cargo.toml | CodeQL | code_quality + codeql |
| rust_core/p2p/src/main.rs | CodeQL | code_quality + codeql |
| rust_core/security/Cargo.lock | CodeQL | code_quality + codeql |
| rust_core/security/Cargo.toml | CodeQL | code_quality + codeql |
| rust_core/security/src/main.rs | CodeQL | code_quality + codeql |
| rust_core/src/lib.rs | CodeQL | code_quality + codeql |
| scripts/ci/run_checks.py | CodeQL + Code quality | code_quality + codeql |
| scripts/consolidate_llm_context.py | CodeQL + Code quality | code_quality + codeql |
| scripts/enforce_branch.py | CodeQL + Code quality | code_quality + codeql |
| scripts/generate_llms_architecture.py | CodeQL + Code quality | code_quality + codeql |
| scripts/generate_project_dashboard.py | CodeQL + Code quality | code_quality + codeql |
| scripts/generate_project_dashboard_v2.py | CodeQL + Code quality | code_quality + codeql |
| scripts/prepend_async_note.py | CodeQL + Code quality | code_quality + codeql |
| scripts/prepend_plan_note.py | CodeQL + Code quality | code_quality + codeql |
| scripts/validate_project_implementation.py | CodeQL + Code quality | code_quality + codeql |
| src/core/crdt_bridge.py | CodeQL + Code quality | code_quality + codeql |
| src/core/providers/FlmProviderConfig.py | CodeQL + Code quality | code_quality + codeql |
| src/core/security_bridge.py | CodeQL + Code quality | code_quality + codeql |
| src/runtime/__init__.py | CodeQL + Code quality | code_quality + codeql |
| src/runtime_py/__init__.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/__init__.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/__main__.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/agent_plugins.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/boot.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/code_quality.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/dependency_audit.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/git_utils.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/knock.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/metrics.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/netcalc.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/nettest.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/nginx.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/port_forward.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/proxy_test.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/ql.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/remote.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/self_heal.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/ssl_utils.py | CodeQL + Code quality | code_quality + codeql |
| src/tools/tool_registry.py | CodeQL + Code quality | code_quality + codeql |
| test | CodeQL | code_quality + codeql |
| tests/structure/test_design_doc.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_consolidate_llm_context_cleanup_report.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_consolidate_llm_context_cli.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_consolidate_llm_context_docstrings.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_consolidate_llm_context_integration.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_consolidate_llm_context_outputs.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_crdt_bridge.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_flm_provider_config.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_flm_provider_docs.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_python_function_coverage.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_quality_yaml.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_rust_crdt_merge.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_rust_p2p_binary.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_security_bridge.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_tools_sanity.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_zza_lint_config.py | CodeQL + Code quality | code_quality + codeql |
| tests/test_zzb_mypy_config.py | CodeQL + Code quality | code_quality + codeql |
| tests/tools/test_tools_cli.py | CodeQL + Code quality | code_quality + codeql |
| tests/tools/test_tools_docs.py | CodeQL + Code quality | code_quality + codeql |
| tests/tools/test_tools_registry.py | CodeQL + Code quality | code_quality + codeql |


## Summary
- Base branch: `main`
- Changed files: 235`
- CodeQL enabled: False


## Code Quality Output
```
Using 235 explicit file(s) for quality checks
Running ruff on changed files...
I001 [*] Import block is un-sorted or un-formatted
  --> scripts\ci\run_checks.py:13:1
   |
11 |   """
12 |
13 | / from __future__ import annotations
14 | |
15 | | import argparse
16 | | import subprocess
17 | | import sys
18 | | from pathlib import Path
   | |________________________^
   |
help: Organize imports

D204 [*] 1 blank line required after class docstring
  --> scripts\consolidate_llm_context.py:38:5
   |
36 | @dataclasses.dataclass(frozen=True)
37 | class ConsolidationConfig:
38 |     """Configuration for the consolidation process, derived from CLI arguments."""
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
39 |     repo_root: Path
40 |     output_dir: Path
   |
help: Insert 1 blank line after class docstring

D204 [*] 1 blank line required after class docstring
  --> scripts\consolidate_llm_context.py:48:5
   |
46 |   @dataclasses.dataclass
47 |   class ConsolidationReport:
48 | /     """Report summarizing the consolidation process,
49 | |     including discovered sources, outputs, and any errors.
50 | |     """
   | |_______^
51 |       repo_root: Path
52 |       output_dir: Path
   |
help: Insert 1 blank line after class docstring

D209 [*] Multi-line docstring closing quotes should be on a separate line
   --> scripts\consolidate_llm_context.py:228:5
    |
227 |   def _build_llms_index(source_counts: dict[str, int]) -> str:
228 | /     """Build the content for llms.txt, which serves as an index 
229 | |     to the consolidated LLM context files."""
    | |_____________________________________________^
230 |       lines: list[str] = []
231 |       lines.append("# llms.txt")
    |
help: Move closing quotes to new line

D210 [*] No whitespaces allowed surrounding docstring text
   --> scripts\consolidate_llm_context.py:228:5
    |
227 |   def _build_llms_index(source_counts: dict[str, int]) -> str:
228 | /     """Build the content for llms.txt, which serves as an index 
229 | |     to the consolidated LLM context files."""
    | |_____________________________________________^
230 |       lines: list[str] = []
231 |       lines.append("# llms.txt")
    |
help: Trim surrounding whitespace

W291 Trailing whitespace
   --> scripts\consolidate_llm_context.py:228:64
    |
227 | def _build_llms_index(source_counts: dict[str, int]) -> str:
228 |     """Build the content for llms.txt, which serves as an index 
    |                                                                ^
229 |     to the consolidated LLM context files."""
230 |     lines: list[str] = []
    |
help: Remove trailing whitespace

D209 [*] Multi-line docstring closing quotes should be on a separate line
   --> scripts\consolidate_llm_context.py:278:5
    |
277 |   def _make_docstring_block(markdown: str) -> str:
278 | /     """Format markdown content as a block to be inserted 
279 | |     into a Python module docstring."""
    | |______________________________________^
280 |       marker_start = "LLM CONTEXT (auto-generated) START"
281 |       marker_end = "LLM CONTEXT (auto-generated) END"
    |
help: Move closing quotes to new line

D210 [*] No whitespaces allowed surrounding docstring text
   --> scripts\consolidate_llm_context.py:278:5
    |
277 |   def _make_docstring_block(markdown: str) -> str:
278 | /     """Format markdown content as a block to be inserted 
279 | |     into a Python module docstring."""
    | |______________________________________^
280 |       marker_start = "LLM CONTEXT (auto-generated) START"
281 |       marker_end = "LLM CONTEXT (auto-generated) END"
    |
help: Trim surrounding whitespace

W291 Trailing whitespace
   --> scripts\consolidate_llm_context.py:278:57
    |
277 | def _make_docstring_block(markdown: str) -> str:
278 |     """Format markdown content as a block to be inserted 
    |                                                         ^
279 |     into a Python module docstring."""
280 |     marker_start = "LLM CONTEXT (auto-generated) START"
    |
help: Remove trailing whitespace

D202 [*] No blank lines allowed after function docstring (found 1)
  --> scripts\generate_project_dashboard.py:32:5
   |
31 | def _normalize_topic_key(topic: str) -> str:
32 |     """Normalize a topic string into a stable file-system friendly key."""
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
33 |
34 |     key = re.sub(r"\s+", "-", topic.strip())
   |
help: Remove blank line(s) after function docstring

D202 [*] No blank lines allowed after function docstring (found 1)
  --> scripts\generate_project_dashboard.py:40:5
   |
39 | def _code_search_candidates(topic_key: str) -> Set[str]:
40 |     """Generate a set of search tokens used to detect implementation files."""
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
41 |
42 |     snake = topic_key.replace("-", "_")
   |
help: Remove blank line(s) after function docstring

D202 [*] No blank lines allowed after function docstring (found 1)
  --> scripts\generate_project_dashboard.py:57:5
   |
56 | def _find_code_files(topic_key: str) -> List[Path]:
57 |     """Return a list of repository paths that appear to implement a given topic."""
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
58 |
59 |     candidates = _code_search_candidates(topic_key)
   |
help: Remove blank line(s) after function docstring

E741 Ambiguous variable name: `l`
   --> scripts\generate_project_dashboard.py:116:29
    |
115 |     text = plan.read_text(encoding="utf-8")
116 |     lines = [l.rstrip() for l in text.splitlines() if re.match(r"^[\s\-*]+\[[ xX]\]", l)]
    |                             ^
117 |     total = len(lines)
118 |     done = len([l for l in lines if re.match(r"^[\s\-*]+\[\s*[xX]\s*\]", l)])
    |

E741 Ambiguous variable name: `l`
   --> scripts\generate_project_dashboard.py:118:23
    |
116 |     lines = [l.rstrip() for l in text.splitlines() if re.match(r"^[\s\-*]+\[[ xX]\]", l)]
117 |     total = len(lines)
118 |     done = len([l for l in lines if re.match(r"^[\s\-*]+\[\s*[xX]\s*\]", l)])
    |                       ^
119 |
120 |     match_paths = _find_code_files(topic_key)
    |

F541 [*] f-string without any placeholders
   --> scripts\generate_project_dashboard.py:131:9
    |
129 |         "## Links",
130 |         "",
131 |         f"- Plan: `plan.md`",
    |         ^^^^^^^^^^^^^^^^^^^^
132 |     ]
    |
help: Remove extraneous `f` prefix

F541 [*] f-string without any placeholders
   --> scripts\generate_project_dashboard.py:135:26
    |
134 |     if design_exists:
135 |         out_lines.append(f"- Design: `brainstorm.md`")
    |                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
136 |     else:
137 |         out_lines.append(f"- Design: **MISSING** (`brainstorm.md`)")
    |
help: Remove extraneous `f` prefix

F541 [*] f-string without any placeholders
   --> scripts\generate_project_dashboard.py:137:26
    |
135 |         out_lines.append(f"- Design: `brainstorm.md`")
136 |     else:
137 |         out_lines.append(f"- Design: **MISSING** (`brainstorm.md`)")
    |                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
138 |
139 |     out_lines += ["", "## Tasks", ""]
    |
help: Remove extraneous `f` prefix

D202 [*] No blank lines allowed after function docstring (found 1)
   --> scripts\generate_project_dashboard.py:191:5
    |
190 | def _color_yes_no(value: str) -> str:
191 |     """Return an ANSI-colored yes/no string."""
    |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
192 |
193 |     # Use green for "Yes" and red for "No" (works in most modern terminals).
    |
help: Remove blank line(s) after function docstring

E501 Line too long (135 > 120)
   --> scripts\generate_project_dashboard.py:218:121
    |
216 | â€¦
217 | â€¦
218 | â€¦']}) | code: {_color_yes_no(code)} | missing design: {_color_yes_no(md)}"
    |                                                            ^^^^^^^^^^^^^^^
219 | â€¦
    |

E902 The system cannot find the file specified. (os error 2)
--> scripts\generate_project_dashboard_v2.py:1:1

D202 [*] No blank lines allowed after function docstring (found 1)
  --> scripts\validate_project_implementation.py:27:5
   |
26 | def _check_plan(path: Path) -> Tuple[int, int, List[str]]:
27 |     """Return (total, done, missing_lines) for checkboxes in plan."""
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
28 |
29 |     if not path.exists():
   |
help: Remove blank line(s) after function docstring

D202 [*] No blank lines allowed after function docstring (found 1)
  --> src\core\crdt_bridge.py:24:5
   |
23 | def _rust_crdt_binary() -> Path:
24 |     """Ensure the rust_core/crdt binary is built and return its path."""
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
25 |
26 |     repo_root = Path(__file__).resolve().parents[2]
   |
help: Remove blank line(s) after function docstring

E501 Line too long (141 > 120)
  --> src\core\crdt_bridge.py:28:121
   |
26 | â€¦
27 | â€¦
28 | â€¦v").exists() and __import__("sys").platform == "win32") else "rust_core_crdt"
   |                                                          ^^^^^^^^^^^^^^^^^^^^^
29 | â€¦
   |

I001 [*] Import block is un-sorted or un-formatted
  --> src\core\providers\FlmProviderConfig.py:20:1
   |
18 |   """
19 |
20 | / from __future__ import annotations
21 | |
22 | | import os
23 | |
24 | | from dataclasses import dataclass
25 | | from typing import Any, Mapping
   | |_______________________________^
   |
help: Organize imports

ANN202 Missing return type annotation for private function `_run_script`
  --> tests\test_consolidate_llm_context_docstrings.py:23:5
   |
23 | def _run_script(tmp_path, args=None):
   |     ^^^^^^^^^^^
24 |     args = args or []
25 |     cmd = [
   |
help: Add return type annotation

ANN202 Missing return type annotation for private function `_run_script`
  --> tests\test_consolidate_llm_context_outputs.py:27:5
   |
27 | def _run_script(tmp_path, args=None):
   |     ^^^^^^^^^^^
28 |     args = args or []
29 |     cmd = [
   |
help: Add return type annotation

D202 [*] No blank lines allowed after function docstring (found 1)
  --> tests\test_rust_p2p_binary.py:34:5
   |
33 |   def _ensure_protoc_available(tmp_path: Path) -> str:
34 | /     """Ensure a `protoc` binary is available for prost-build.
35 | |
36 | |     The libp2p dependency uses prost-build which requires a `protoc` executable.
37 | |     This helper will download a vendored protoc for Windows when it is missing.
38 | |     """
   | |_______^
39 |
40 |       # If the system already has protoc, use it.
   |
help: Remove blank line(s) after function docstring

Found 27 errors.
[*] 18 fixable with the `--fix` option (2 hidden fixes can be enabled with the `--unsafe-fixes` option).
Running mypy on changed files...
Running pytest on changed test files...
Fixed leading-import lines in 0 files.
................................                                         [100%]
=============================== tests coverage ================================
______________ coverage: platform win32, python 3.13.12-final-0 _______________

Name                                        Stmts   Miss  Cover   Missing
-------------------------------------------------------------------------
src\MemoryTransactionManager.py                17      3    82%   71-72, 78
src\__init__.py                                 1      0   100%
src\benchmarks\simple.py                        2      0   100%
src\chat\__init__.py                            0      0   100%
src\chat\api.py                                39      7    82%   86-88, 99-102, 111
src\chat\mcp_tools.py                           7      1    86%   36
src\chat\models.py                             11      2    82%   38, 43
src\chat\utils.py                               7      0   100%
src\context_manager\__init__.py                15     10    33%   24-25, 30-38, 42
src\core\UnifiedTransactionManager.py          49     49     0%   17-129
src\core\__init__.py                            0      0   100%
src\core\agent_registry.py                     19     19     0%   16-48
src\core\agent_state_manager.py                 3      3     0%   17-23
src\core\base\__init__.py                       2      2     0%   18-21
src\core\crdt_bridge.py                        24      2    92%   32, 68
src\core\memory.py                             19     19     0%   16-48
src\core\observability.py                       8      8     0%   16-35
src\core\providers\FlmChatAdapter.py           79     42    47%   97-105, 109-111, 119-131, 144-147, 173-238, 249-259
src\core\providers\FlmProviderConfig.py        61      8    87%   80, 89, 116-119, 142, 159
src\core\providers\__init__.py                  3      0   100%
src\core\runtime.py                            11     11     0%   20-42
src\core\scaffold\__init__.py                  10     10     0%   20-55
src\core\security_bridge.py                    28      2    93%   30, 90
src\core\task_queue.py                         19     19     0%   16-49
src\cort\__init__.py                           25     15    40%   28-29, 38-42, 56-58, 66-69, 77-78
src\github_app.py                               7      0   100%
src\importer\__init__.py                        4      0   100%
src\importer\compile.py                         6      4    33%   9-12
src\importer\config.py                         13     10    23%   7-16
src\importer\describe.py                        4      1    75%   23
src\importer\downloader.py                      5      2    60%   10-11
src\memory\__init__.py                          2      0   100%
src\multimodal\__init__.py                      2      0   100%
src\observability\stats\legacy_engine.py       11      1    91%   42
src\observability\stats\metrics_engine.py      10      0   100%
src\rl\__init__.py                              2      0   100%
src\roadmap\__init__.py                         2      0   100%
src\roadmap\cli.py                             10      1    90%   29
src\roadmap\innovation.py                      11      0   100%
src\roadmap\milestones.py                       9      4    56%   24-27
src\roadmap\prioritization.py                   2      0   100%
src\roadmap\vision.py                           2      0   100%
src\runtime\__init__.py                        20      2    90%   38, 56
src\runtime_py\__init__.py                    148     49    67%   38, 42, 46-47, 51-52, 68, 79-84, 169-174, 194-200, 204-207, 256-260, 277-303
src\skills_registry\__init__.py                16     10    38%   28, 32-40
src\speculation\__init__.py                     2      0   100%
src\swarm\__init__.py                           0      0   100%
src\swarm\agent_registry.py                    21     12    43%   26-27, 31-37, 41, 45, 50-53, 59-60
src\swarm\message_model.py                     14      1    93%   25
src\swarm\task_scheduler.py                    22     13    41%   16-17, 23-26, 32-36, 40-42
src\tools\__init__.py                          12      2    83%   31-34
src\tools\__main__.py                          23      9    61%   32-41
src\tools\agent_plugins.py                     30     12    60%   22-28, 43-50
src\tools\boot.py                              33     16    52%   30, 50-82
src\tools\code_quality.py                      65     43    34%   30-35, 42-50, 55, 73-116
src\tools\common.py                            13      1    92%   13
src\tools\dependency_audit.py                  41     11    73%   44-47, 55-58, 70-77
src\tools\git_utils.py                         43     21    51%   31, 36-39, 56-73
src\tools\knock.py                             26     11    58%   38-50
src\tools\metrics.py                           31     12    61%   34-39, 61-70
src\tools\netcalc.py                           24      9    62%   39-48
src\tools\nettest.py                           27     11    59%   31-38, 50-52
src\tools\nginx.py                             29     14    52%   38-54
src\tools\pm\__init__.py                        1      0   100%
src\tools\pm\email.py                           5      4    20%   23-26
src\tools\pm\kpi.py                             3      0   100%
src\tools\pm\risk.py                           10      8    20%   24-32
src\tools\port_forward.py                      35     18    49%   36-52, 69-79
src\tools\proxy_test.py                        24     11    54%   37-47, 54
src\tools\ql.py                               110     84    24%   43-51, 56-59, 64-74, 81-84, 89-92, 98-100, 125-160, 192-282
src\tools\remote.py                            19      5    74%   37-42
src\tools\self_heal.py                         34     14    59%   35-40, 46, 61-68
src\tools\ssl_utils.py                         24     10    58%   31-33, 42-49
src\tools\tool_registry.py                     31      5    84%   47, 67-70
src\transport\__init__.py                      63      9    86%   53, 64-68, 81, 110-111
-------------------------------------------------------------------------
TOTAL                                        1560    682    56%
32 passed in 35.89s

warning: The top-level linter settings are deprecated in favour of their counterparts in the `lint` section. Please update the following options in `pyproject.toml`:
  - 'ignore' -> 'lint.ignore'
  - 'select' -> 'lint.select'
warning: `incorrect-blank-line-before-class` (D203) and `no-blank-line-before-class` (D211) are incompatible. Ignoring `incorrect-blank-line-before-class`.
warning: `multi-line-summary-first-line` (D212) and `multi-line-summary-second-line` (D213) are incompatible. Ignoring `multi-line-summary-second-line`.
mypy: can't read file 'scripts\generate_project_dashboard_v2.py': No such file or directory
```


## CodeQL Output
```
CodeQL skipped: CLI not found or --skip-codeql specified.
```