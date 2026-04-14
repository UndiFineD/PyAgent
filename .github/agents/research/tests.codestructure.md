# Code Structure Index

Domain index for `tests` paths.

Format: `## <file>` followed by `- line: code` entries.

## tests/agents/test_agents.py

- 5: def test_placeholder() -> None:

## tests/agents/test_base_agent.py

- 16: from __future__ import annotations
- 18: import asyncio
- 19: from typing import Any
- 21: import pytest
- 23: from src.agents.BaseAgent import AgentLifecycle, AgentManifest, BaseAgent
- 30: class EchoAgent(BaseAgent):
- 33: async def run(self, task: dict[str, Any]) -> dict[str, Any]:
- 42: def test_manifest_defaults() -> None:
- 50: def test_manifest_custom_fields() -> None:
- 66: def test_initial_state_is_idle() -> None:
- 71: def test_start_transitions_to_running() -> None:
- 77: def test_stop_transitions_to_stopped() -> None:
- 84: def test_reset_from_stopped_to_idle() -> None:
- 92: def test_start_raises_if_already_running() -> None:
- 99: def test_reset_raises_if_running() -> None:
- 112: async def test_dispatch_echoes_payload() -> None:
- 121: async def test_dispatch_raises_if_not_running() -> None:
- 128: async def test_dispatch_respects_max_concurrency() -> None:
- 132: class OrderedAgent(BaseAgent):
- 133: async def run(self, task: dict[str, Any]) -> dict[str, Any]:
- 155: def test_validate_returns_true() -> None:
- 164: def test_repr_contains_name() -> None:

## tests/ci/test_ci_parallelization.py

- 18: def _load_ci_yml() -> dict:
- 19: import yaml
- 25: def _load_requirements_ci() -> str:
- 35: def test_ci_workflow_has_matrix():
- 47: def test_ci_matrix_has_three_shards():
- 51: assert sorted(shards) == list(range(1, 11))
- 59: def test_requirements_ci_has_xdist():
- 69: def test_ci_uses_parallel_flag():

## tests/ci/test_ci_workflow.py

- 4: import os
- 6: import yaml
- 9: def test_ci_workflow_exists() -> None:
- 15: def test_ci_workflow_sanity() -> None:

## tests/ci/test_workflow_count.py

- 24: from pathlib import Path
- 26: import yaml
- 28: _WORKFLOWS_DIR = Path(".github/workflows")
- 29: _SECURITY_YML = _WORKFLOWS_DIR / "security.yml"
- 30: _CI_YML = _WORKFLOWS_DIR / "ci.yml"
- 33: def _load_security_yml() -> dict:
- 43: def test_exactly_two_workflow_files() -> None:
- 57: def test_security_yml_exists_and_has_analyze_job() -> None:
- 70: def test_security_yml_has_security_events_write_permission() -> None:
- 85: def test_security_yml_uses_codeql_action_steps() -> None:
- 107: def test_security_yml_has_schedule_trigger() -> None:
- 125: def test_security_yml_references_custom_python_queries() -> None:

## tests/core/test_core.py

- 5: def test_placeholder() -> None:

## tests/deploy/test_compose_dockerfile_paths.py

- 22: from __future__ import annotations
- 24: from pathlib import Path
- 25: from typing import Any
- 27: REPO_ROOT = Path(__file__).resolve().parents[2]
- 28: COMPOSE_FILE = REPO_ROOT / "deploy" / "compose.yaml"
- 29: EXPECTED_DOCKERFILE = "deploy/Dockerfile.pyagent"
- 32: def _load_compose_contract() -> dict[str, Any]:
- 44: import yaml  # type: ignore[import-not-found]
- 53: def _fallback_parse_compose_contract(compose_text: str) -> dict[str, Any]:
- 118: def _resolve_pyagent_dockerfile_path(compose_obj: dict[str, Any]) -> Path:
- 146: def test_compose_reference_contract_uses_expected_pyagent_dockerfile_path() -> None:
- 165: def test_compose_referenced_dockerfile_path_exists_in_repository() -> None:

## tests/docs/test_allowed_websites_governance.py

- 15: from pathlib import Path
- 17: REPO_ROOT = Path(__file__).resolve().parents[2]
- 18: CANONICAL_ALLOWLIST_PATH = REPO_ROOT / ".github" / "agents" / "data" / "allowed_websites.md"
- 19: ROOT_ALLOWLIST_PATH = REPO_ROOT / "allowed_websites.md"
- 22: def _read_allowlist_text() -> str:
- 32: def _allowed_domains(text: str) -> set[str]:
- 51: def test_canonical_allowlist_location_and_root_absence() -> None:
- 57: def test_allowlist_includes_required_domains() -> None:

## tests/docs/test_api_docs_exist.py

- 18: import os
- 20: _API_DOCS_ROOT = "docs/api"
- 22: _REQUIRED_FILES = [
- 30: _MIN_SIZE_BYTES = 1024  # each file must be ? 1 KB
- 33: def test_api_docs_files_exist() -> None:
- 40: def test_api_docs_files_non_empty() -> None:
- 48: def test_api_docs_no_todo_markers() -> None:
- 57: def test_index_contains_required_sections() -> None:
- 66: def test_authentication_contains_required_sections() -> None:
- 75: def test_rest_endpoints_covers_all_methods() -> None:
- 84: def test_websocket_contains_mermaid_and_close_codes() -> None:
- 93: def test_errors_contains_rate_limit_and_close_codes() -> None:

## tests/docs/test_changelog.py

- 15: import pytest
- 17: from scripts.changelog import generate_entry
- 20: def test_generate_entry_empty(monkeypatch: pytest.MonkeyPatch) -> None:
- 26: def test_generate_entry_various(monkeypatch: pytest.MonkeyPatch) -> None:

## tests/docs/test_copilot_instructions_governance.py

- 15: from pathlib import Path
- 17: REPO_ROOT = Path(__file__).resolve().parents[2]
- 18: COPILOT_INSTRUCTIONS_PATH = REPO_ROOT / ".github" / "copilot-instructions.md"
- 21: def _read_copilot_instructions() -> str:
- 31: def test_copilot_instructions_reference_local_search_first() -> None:
- 39: def test_copilot_instructions_reference_canonical_allowlist_path() -> None:

## tests/docs/test_diagrams_compile.py

- 4: import subprocess
- 5: from pathlib import Path
- 6: from typing import Any
- 9: def test_compile_diagrams(tmp_path: Path, monkeypatch: Any) -> None:
- 19: import scripts.compile_diagrams as cd
- 24: def fake_run(cmd: list[str], **kwargs: Any) -> None:

## tests/docs/test_docs_exist.py

- 1: import os
- 3: FILES = [
- 12: DIAGRAMS = [
- 17: def test_document_files_exist() -> None:
- 23: def test_diagram_sources_exist() -> None:

## tests/fakeconftest.py

- 4: import os
- 5: import sys
- 8: ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
- 9: SRC = os.path.join(ROOT, "src")

## tests/fixtures/conftest_fixtures.py

- 23: from __future__ import annotations
- 25: from pathlib import Path
- 26: from typing import Any
- 28: import pytest
- 36: def tmp_agent_dir(tmp_path: Path) -> Path:
- 44: def tmp_project_dir(tmp_path: Path) -> Path:
- 58: def sample_task() -> dict[str, Any]:
- 64: def sample_message() -> dict[str, Any]:
- 79: def sample_risk_table(tmp_path: Path) -> Path:

## tests/fixtures/mypy_strict_lane/bad_case.py

- 5: def require_int(value: int) -> int:
- 18: BROKEN_VALUE: str = "not-an-int"
- 19: BROKEN_RESULT: int = require_int(BROKEN_VALUE)

## tests/guards/test_rl_speculation_import_scope.py

- 17: from __future__ import annotations
- 19: import ast
- 20: from pathlib import Path
- 22: ROOT = Path(".")
- 23: SCAN_ROOTS: tuple[Path, ...] = (ROOT / "tests", ROOT / "src")
- 24: ALLOWED_IMPORT_FILES: set[str] = {
- 32: def _iter_python_files() -> list[Path]:
- 50: def _contains_target_import(node: ast.AST) -> bool:
- 67: def _find_disallowed_import_sites() -> list[str]:
- 76: source = path.read_text(encoding="utf-8")
- 89: def test_allowlist_files_exist_for_rl_speculation_behavior_and_deprecation() -> None:
- 95: def test_no_disallowed_rl_or_speculation_import_sites() -> None:

## tests/integration/test_context_and_skills.py

- 4: from pathlib import Path
- 6: import pytest
- 8: from context_manager import ContextManager
- 9: from cort import ChainOfThought
- 10: from skills_registry import SkillsRegistry
- 14: async def test_context_and_skills(tmp_path: Path) -> None:
- 17: assert hasattr(cm, "push")
- 20: assert isinstance(skills, list)

## tests/observability/test_legacy_engine.py

- 1: import asyncio
- 3: import pytest
- 5: from observability.stats import legacy_engine
- 9: async def test_legacy_engine_async_loop():

## tests/observability/test_metrics_engine.py

- 1: import asyncio
- 3: import pytest
- 5: from observability.stats import metrics_engine  # type: ignore[import-not-found]
- 9: async def test_async_tick_loop() -> None:

## tests/rl/test_discounted_return.py

- 17: from __future__ import annotations
- 19: import math
- 20: from collections.abc import Callable
- 22: import pytest
- 24: import rl
- 27: def _discounted_return_callable() -> Callable[[list[float], float], float]:
- 39: def test_discounted_return_computes_expected_value() -> None:
- 51: def test_discounted_return_returns_zero_for_empty_rewards() -> None:
- 61: def test_discounted_return_rejects_invalid_gamma(gamma: float) -> None:
- 75: def test_discounted_return_rejects_non_finite_rewards(bad_reward: float) -> None:

## tests/rl/test_rl_deprecation.py

- 17: from __future__ import annotations
- 19: import re
- 20: from collections.abc import Callable
- 22: import pytest
- 24: import rl
- 27: def _validate_callable() -> Callable[[], bool]:
- 39: def test_rl_validate_emits_deprecation_warning_with_migration_message() -> None:

## tests/runtime/test_event_bus.py

- 1: import asyncio
- 3: import pytest
- 5: from runtime_py import emit, on
- 9: async def test_event_bus() -> None:
- 13: async def handler1(x: int) -> None:
- 17: async def handler2(x: int) -> None:

## tests/runtime/test_http_server.py

- 1: import asyncio
- 3: import httpx
- 4: import pytest
- 6: from runtime_py import run_http_server
- 10: async def test_http_server() -> None:
- 14: async def handler(uri: str) -> tuple[int, str]:

## tests/runtime/test_queue.py

- 1: import asyncio
- 3: import runtime_py as runtime
- 6: def test_queue_basic() -> None:
- 9: async def inner() -> None:
- 13: await put("hello")

## tests/runtime/test_runtime_import.py

- 16: import asyncio
- 18: import pytest
- 25: def test_core_runtime_module_importable():
- 27: from src.core import runtime as r
- 29: assert hasattr(r, "Runtime")
- 30: assert hasattr(r, "spawn_task")
- 31: assert hasattr(r, "set_timeout")
- 32: assert hasattr(r, "create_queue")
- 33: assert hasattr(r, "validate")
- 36: def test_validate_passes():
- 37: from src.core.runtime import validate
- 48: async def test_spawn_task_runs_coro():
- 49: from src.core.runtime import spawn_task
- 53: async def work() -> None:
- 67: async def test_set_timeout_fires():
- 68: from src.core.runtime import set_timeout
- 72: async def work() -> None:
- 75: await set_timeout(lambda: work(), delay=0.01)
- 85: def test_create_queue_unbounded():
- 86: from src.core.runtime import create_queue
- 89: assert isinstance(q, asyncio.Queue)
- 93: async def test_queue_put_get():
- 94: from src.core.runtime import create_queue
- 108: async def test_runtime_start():
- 109: from src.core.runtime import Runtime
- 116: async def test_runtime_submit_and_pending():
- 117: from src.core.runtime import Runtime
- 122: async def noop() -> None:
- 127: assert isinstance(tid, str)
- 134: async def test_runtime_cancel():
- 135: from src.core.runtime import Runtime
- 139: async def long_task() -> None:
- 152: def test_runtime_stubs_present():
- 154: from src.core import runtime
- 156: assert hasattr(runtime, "spawn_task")
- 157: assert hasattr(runtime, "set_timeout")
- 158: assert hasattr(runtime, "create_queue")

## tests/runtime/test_spawn_task.py

- 1: import os
- 2: import subprocess
- 3: import sys
- 4: from pathlib import Path
- 7: def test_spawn_simple() -> None:
- 11: import asyncio
- 12: import runtime
- 14: async def inner():
- 17: async def worker():

## tests/runtime/test_timeout.py

- 1: import asyncio
- 3: import runtime_py as runtime
- 6: def test_sleep_delay() -> None:
- 10: async def inner() -> None:

## tests/runtime/test_watch_file.py

- 4: import asyncio
- 5: from pathlib import Path
- 7: import pytest
- 9: import src.runtime_py
- 13: async def test_watch_file(tmp_path: Path) -> None:
- 20: async def cb(_event_str: str) -> None:

## tests/runtime/tmp_spawn_test.py

- 1: import asyncio
- 3: import src.runtime as _rt
- 6: async def inner() -> None:
- 10: async def worker() -> None:

## tests/security/fixtures/scan_samples.py

- 3: from __future__ import annotations
- 5: from typing import Any
- 8: def sample_tree_findings() -> list[dict[str, Any]]:
- 33: def sample_history_findings() -> list[dict[str, Any]]:

## tests/security/test_ci_secret_guardrail_job.py

- 3: from __future__ import annotations
- 5: from pathlib import Path
- 7: WORKFLOW_PATH = Path(".github/workflows/security.yml")
- 10: def test_security_workflow_defines_secret_scan_job() -> None:
- 16: def test_security_workflow_fails_closed_on_secret_findings() -> None:
- 25: assert any(signal in content for signal in fail_closed_signals)

## tests/security/test_containment_cleanup.py

- 3: from __future__ import annotations
- 5: from pathlib import Path
- 7: RUNBOOK_PATH = Path("docs/security/private-key-remediation-runbook.md")
- 8: VERIFIER_SCRIPT_PATH = Path("scripts/security/verify_no_key_material.py")
- 11: def test_runbook_includes_containment_evidence_section() -> None:
- 19: def test_cleanup_verifier_exists_and_is_repo_path_scoped() -> None:

## tests/security/test_pre_commit_secret_hook.py

- 3: from __future__ import annotations
- 5: from pathlib import Path
- 7: PRE_COMMIT_PATH = Path(".pre-commit-config.yaml")
- 10: def test_pre_commit_config_includes_secret_scan_hook() -> None:
- 16: def test_pre_commit_secret_scan_hook_runs_before_commit() -> None:
- 23: def test_pre_commit_and_ci_share_tree_profile_invocation() -> None:

## tests/security/test_private_key_artifact_absence.py

- 3: from __future__ import annotations
- 5: from pathlib import Path
- 7: PRIVATE_KEY_ARTIFACT_PATH = Path("rust_core/2026-03-11-keys.priv")
- 10: def test_active_tree_excludes_private_key_artifact_path() -> None:

## tests/security/test_rotation_checkpoint_service.py

- 3: from __future__ import annotations
- 5: import importlib
- 6: from typing import Any
- 8: import pytest
- 11: def _load_rotation_symbol(module_name: str, symbol_name: str) -> Any:
- 36: def test_begin_incident_records_incident_and_fingerprint() -> None:
- 51: def test_record_rotation_step_requires_evidence_uri() -> None:

## tests/security/test_rotation_gate_decision.py

- 3: from __future__ import annotations
- 5: import importlib
- 6: from typing import Any
- 8: import pytest
- 11: def _load_rotation_service() -> Any:
- 31: def test_evaluate_gate_transitions_blocked_to_partial_to_complete() -> None:

## tests/security/test_rust_p2p_deps.py

- 30: import re
- 31: from pathlib import Path
- 33: import pytest
- 38: REPO_ROOT = Path(__file__).parent.parent.parent
- 39: P2P_DIR = REPO_ROOT / "rust_core" / "p2p"
- 40: CARGO_LOCK = P2P_DIR / "Cargo.lock"
- 41: CARGO_TOML = P2P_DIR / "Cargo.toml"
- 46: VULNERABLE_VERSIONS = [
- 56: def _parse_lock_packages(lock_text: str) -> list[tuple[str, str]]:
- 73: def cargo_lock_packages():
- 81: def test_vulnerable_version_not_in_cargo_lock(cargo_lock_packages, pkg, vuln_version):
- 100: def test_libp2p_version_is_056_in_cargo_toml():
- 122: def _extract_libp2p_version(toml_text: str) -> str \| None:

## tests/security/test_scan_report_schema.py

- 3: from __future__ import annotations
- 5: import importlib
- 6: from typing import Any
- 8: import pytest
- 11: def _load_scan_report_model() -> Any:
- 32: def test_scan_report_requires_run_id_and_status_enum() -> None:
- 47: def test_scan_report_computes_blocking_from_high_and_critical_findings() -> None:

## tests/security/test_secret_guardrail_policy.py

- 3: from __future__ import annotations
- 5: import importlib
- 6: from typing import Any
- 8: import pytest
- 11: def _load_policy_class() -> Any:
- 31: def test_validate_pr_blocks_when_high_or_critical_findings_exist() -> None:
- 46: def test_validate_push_blocks_when_critical_findings_exist() -> None:
- 53: assert any("CRITICAL" in item for item in decision.blocking_reasons)

## tests/security/test_secret_scan_service_contract.py

- 3: from __future__ import annotations
- 5: import importlib
- 6: from typing import Any
- 8: import pytest
- 10: from tests.security.fixtures.scan_samples import sample_history_findings, sample_tree_findings
- 13: def _load_symbol(module_name: str, symbol_name: str) -> Any:
- 41: def test_secret_scan_service_exposes_profile_specific_scan_methods() -> None:
- 53: def test_secret_scan_service_deterministically_orders_finding_keys() -> None:
- 66: def test_secret_scan_service_fails_closed_on_scanner_execution_error() -> None:
- 71: def _raise_tool_error(*_: Any, **__: Any) -> dict[str, Any]:
- 78: raise RuntimeError("scanner crashed")

## tests/speculation/test_select_candidate.py

- 17: from __future__ import annotations
- 19: import math
- 20: from collections.abc import Callable
- 22: import pytest
- 24: import speculation
- 27: def _select_candidate_callable() -> Callable[[dict[str, float], float], str \| None]:
- 39: def test_select_candidate_applies_threshold_and_picks_highest_score() -> None:
- 49: def test_select_candidate_returns_none_for_empty_input() -> None:
- 58: def test_select_candidate_returns_none_when_no_scores_meet_threshold() -> None:
- 68: def test_select_candidate_uses_lexicographic_tie_break_deterministically() -> None:
- 79: def test_select_candidate_rejects_non_finite_scores(bad_score: float) -> None:

## tests/speculation/test_speculation_deprecation.py

- 17: from __future__ import annotations
- 19: import re
- 20: from collections.abc import Callable
- 22: import pytest
- 24: import speculation
- 27: def _validate_callable() -> Callable[[], bool]:
- 39: def test_speculation_validate_emits_deprecation_warning_with_migration_message() -> None:

## tests/structure/test_architecture_naming.py

- 24: import re
- 25: from pathlib import Path
- 27: REPO_ROOT = Path(__file__).resolve().parents[2]
- 28: ARCH_DIR = REPO_ROOT / "docs" / "architecture"
- 30: _NUMBERED_RE = re.compile(r"^\d.*\.md$")
- 33: def _top_level_md_files() -> list[Path]:
- 38: def test_architecture_dir_exists() -> None:
- 43: def test_no_md_files_exceed_eight() -> None:
- 50: def test_all_md_files_have_numbered_names() -> None:
- 58: def test_no_todolist_md() -> None:
- 63: def test_no_generated_md() -> None:
- 69: def test_0overview_exists() -> None:
- 74: def test_1agents_exists() -> None:

## tests/structure/test_base_dirs.py

- 5: def test_root_project_dir_exists(tmp_path) -> None:
- 8: from scripts.setup_structure import create_core_structure

## tests/structure/test_ci_yaml.py

- 4: from pathlib import Path
- 5: from typing import Any
- 7: import yaml
- 10: def _load_ci_workflow() -> dict[str, Any]:
- 21: def _find_coverage_gate_steps(ci_workflow: dict[str, Any]) -> list[dict[str, Any]]:
- 43: def test_ci_runs_pytest() -> None:
- 52: assert any("pytest" in (step.get("run") or "") for step in steps)
- 55: def test_ci_does_not_run_shared_precommit_profile() -> None:
- 67: def test_setup_md_has_local_testing_section() -> None:
- 81: def test_ci_has_mypy_strict_lane_blocking_step() -> None:
- 97: def test_ci_mypy_strict_lane_step_is_blocking() -> None:
- 119: def test_ci_has_coverage_gate_step() -> None:
- 134: def test_ci_coverage_gate_path_is_blocking() -> None:

## tests/structure/test_config_files.py

- 4: import os
- 7: def test_pytest_config_present() -> None:
- 12: def test_conftest_imports_src() -> None:

## tests/structure/test_coverage_option.py

- 5: def test_cov_option_present() -> None:

## tests/structure/test_data_script.py

- 4: from pathlib import Path
- 6: from scripts.generate_test_data import generate_sample_fixture
- 9: def test_data_script(tmp_path: Path) -> None:

## tests/structure/test_deployment_dirs.py

- 4: import os
- 7: def test_deployment_tree_absent() -> None:

## tests/structure/test_design_doc.py

- 4: import os
- 7: def test_design_doc_present() -> None:

## tests/structure/test_dev_tools_dirs.py

- 4: from pathlib import Path
- 7: def test_dev_tools_structure(tmp_path: Path) -> None:
- 9: from scripts.setup_structure import create_core_structure
- 17: def test_required_tool_modules_exist() -> None:
- 19: import src.tools  # noqa: F401 ? triggers auto-registration
- 36: def test_pm_subpackage_exists() -> None:
- 44: def test_tools_package_importable() -> None:
- 46: import importlib

## tests/structure/test_files.py

- 4: import os
- 5: from pathlib import Path
- 8: def test_important_files_exist(tmp_path: Path) -> None:
- 11: from scripts.setup_structure import create_core_structure

## tests/structure/test_fixtures.py

- 16: from __future__ import annotations
- 18: import importlib
- 21: def test_fixtures_module_importable():
- 27: def test_fixtures_module_exports_expected_names():
- 33: def test_sample_task_structure():
- 41: def test_sample_message_structure():
- 42: from swarm.message_model import validate_message

## tests/structure/test_governance_creation.py

- 4: import os
- 5: import subprocess
- 6: from pathlib import Path
- 9: def run_setup_script() -> None:
- 15: def test_governance_docs_created(tmp_path, monkeypatch) -> None:
- 36: def test_status_email_template(tmp_path, monkeypatch) -> None:

## tests/structure/test_install_script.py

- 20: from pathlib import Path
- 22: import pytest
- 24: REPO_ROOT = Path(__file__).parent.parent.parent
- 25: _SCRIPT_PATH = REPO_ROOT / "install.ps1"
- 34: _FILE_MISSING = content == ""
- 42: def test_install_script_exists() -> None:
- 52: def _require_file(func):
- 63: def test_has_cmdletbinding() -> None:
- 69: def test_has_param_block() -> None:
- 75: def test_has_skiprrust_param() -> None:
- 81: def test_has_skipweb_param() -> None:
- 87: def test_has_skipdev_param() -> None:
- 93: def test_has_ci_param() -> None:
- 99: def test_has_force_param() -> None:
- 110: def test_has_synopsis() -> None:
- 116: def test_has_description() -> None:
- 127: def test_has_write_status_function() -> None:
- 133: def test_has_test_prerequisites_function() -> None:
- 139: def test_has_initialize_venv_function() -> None:
- 145: def test_has_install_python_function() -> None:
- 151: def test_has_build_rust_function() -> None:
- 157: def test_has_install_scaffold_function() -> None:
- 163: def test_has_install_node_function() -> None:
- 169: def test_has_show_summary_function() -> None:
- 180: def test_references_requirements_txt() -> None:
- 186: def test_references_backend_requirements() -> None:
- 192: def test_references_requirements_ci() -> None:
- 203: def test_has_venv_creation() -> None:
- 209: def test_has_venv_activate() -> None:
- 220: def test_has_maturin() -> None:
- 226: def test_has_maturin_develop() -> None:
- 232: def test_has_rust_core_manifest() -> None:
- 243: def test_has_npm_install() -> None:
- 254: def test_has_summary_complete_message() -> None:
- 265: def test_has_python_version_check() -> None:
- 276: def test_has_os_guard() -> None:
- 287: def test_has_error_action_preference() -> None:
- 298: def test_has_requires_version() -> None:

## tests/structure/test_kanban.py

- 25: import json
- 26: import re
- 27: from pathlib import Path
- 29: import pytest
- 31: REPO_ROOT = Path(__file__).parent.parent.parent
- 32: _PROJECTS_PATH = REPO_ROOT / "data" / "projects.json"
- 33: _KANBAN_PATH = REPO_ROOT / "docs" / "project" / "kanban.md"
- 34: _NEXTPROJECT_PATH = REPO_ROOT / "data" / "nextproject.md"
- 58: def _expected_project_count() -> int \| None:
- 77: _PROJECTS_MISSING = not _PROJECTS_PATH.exists()
- 79: _KANBAN_MISSING = (
- 83: _SKIP_PROJECTS = pytest.mark.skipif(
- 87: _SKIP_KANBAN = pytest.mark.skipif(
- 96: REQUIRED_FIELDS = {
- 110: VALID_LANES = {
- 120: VALID_PRIORITIES = {"P1", "P2", "P3", "P4"}
- 122: VALID_BUDGET_TIERS = {"XS", "S", "M", "L", "XL", "unknown"}
- 125: KANBAN_REQUIRED_H2S = [
- 142: def test_projects_json_exists() -> None:
- 152: def test_projects_json_valid() -> None:
- 159: def test_projects_json_entry_count() -> None:
- 171: def test_projects_json_required_fields() -> None:
- 187: def test_projects_json_lane_values() -> None:
- 201: def test_projects_json_priority_values() -> None:
- 216: def test_projects_json_budget_tier_values() -> None:
- 231: def test_projects_json_prj0000052_present() -> None:
- 246: def test_kanban_exists() -> None:
- 261: def test_kanban_required_h2s(heading: str) -> None:
- 270: def test_kanban_total_rows() -> None:
- 283: def test_kanban_prj0000052_present() -> None:
- 289: def test_kanban_no_todo_fixme() -> None:

## tests/structure/test_mirror_dirs.py

- 5: def test_mirror_dirs_initial(tmp_path) -> None:
- 7: assert not (tmp_path / "tests" / "core").exists()
- 8: assert not (tmp_path / "tests" / "agents").exists()

## tests/structure/test_mypy_strict_lane_config.py

- 4: from configparser import ConfigParser
- 5: from pathlib import Path
- 7: STRICT_CONFIG_PATH = Path("mypy-strict-lane.ini")
- 8: EXPECTED_ALLOWLIST = [
- 22: def _load_strict_config() -> ConfigParser:
- 40: def _normalize_files_value(files_value: str) -> list[str]:
- 54: def test_mypy_strict_lane_required_options() -> None:
- 76: def test_mypy_strict_lane_allowlist_locked() -> None:

## tests/structure/test_readme.py

- 22: import re
- 23: from pathlib import Path
- 25: import pytest
- 27: REPO_ROOT = Path(__file__).parent.parent.parent
- 28: _README_PATH = REPO_ROOT / "README.md"
- 44: _FILE_MISSING = not _README_PATH.exists() or not _lines or _lines[0].strip() != "# PyAgent"
- 46: _SKIP_CONTENT = pytest.mark.skipif(_FILE_MISSING, reason="README not yet written (awaiting @6code)")
- 54: def _section_lines(heading_prefix: str) -> list:
- 74: def test_readme_exists() -> None:
- 91: def test_readme_h1() -> None:
- 101: _REQUIRED_H2S = [
- 117: def test_required_h2_headings(heading: str) -> None:
- 130: def test_what_is_single_paragraph() -> None:
- 155: def test_key_numbers_present(token: str) -> None:
- 167: def test_install_flags_documented(flag: str) -> None:
- 179: def test_start_commands_documented(cmd: str) -> None:
- 190: def test_project_history_count() -> None:
- 203: def test_future_roadmap_count() -> None:
- 216: def test_no_todo_fixme() -> None:
- 231: def test_powershell_fences() -> None:
- 245: def test_architecture_decisions_numbered() -> None:
- 261: def test_rust_keywords(keyword: str) -> None:
- 273: def test_nebula_apps(app: str) -> None:
- 285: def test_backend_endpoints(endpoint: str) -> None:
- 296: def test_install_ps1_mentioned() -> None:
- 307: def test_start_ps1_mentioned() -> None:
- 318: def test_line_length() -> None:

## tests/structure/test_setup_tests_script.py

- 16: from __future__ import annotations
- 18: from pathlib import Path
- 20: from scripts.SetupTests import create_test_structure
- 23: def test_creates_mirror_for_new_package(tmp_path: Path):
- 36: def test_skips_existing_mirror(tmp_path: Path):
- 46: def test_dry_run_does_not_write(tmp_path: Path):
- 55: assert not (tests / "newpkg").exists()
- 58: def test_skips_dunder_packages(tmp_path: Path):

## tests/test_AuditEvent.py

- 16: from __future__ import annotations
- 18: from importlib import import_module
- 19: from typing import Any
- 21: import pytest
- 24: def _load_auditevent() -> Any:
- 35: def test_auditevent_exposes_canonical_methods() -> None:
- 38: assert hasattr(audit_event_cls, "to_canonical_dict")
- 39: assert hasattr(audit_event_cls, "to_json_dict")
- 40: assert hasattr(audit_event_cls, "from_json_dict")
- 43: def test_auditevent_schema_version_default_is_one() -> None:

## tests/test_AuditExceptions.py

- 16: from src.core.audit.exceptions import (
- 26: def test_audit_exception_types_inherit_from_audittrailerror() -> None:
- 34: assert issubclass(error_type, AuditTrailError)
- 37: def test_exceptions_module_validate_returns_true() -> None:

## tests/test_AuditHasher.py

- 16: from __future__ import annotations
- 18: from importlib import import_module
- 19: from typing import Any
- 21: import pytest
- 24: def _load_symbol(module_name: str, symbol_name: str) -> Any:
- 38: def test_audithasher_produces_deterministic_hash_for_equivalent_events() -> None:
- 77: def test_audithasher_validate_hash_format_accepts_and_rejects_expected_values() -> None:

## tests/test_AuditTrailCore.py

- 16: from __future__ import annotations
- 18: from importlib import import_module
- 19: from pathlib import Path
- 20: from typing import Any
- 22: import pytest
- 25: def _load_symbol(module_name: str, symbol_name: str) -> Any:
- 39: def _new_event() -> Any:
- 56: def test_audittrailcore_append_event_returns_hash_string(tmp_path: Path) -> None:
- 61: assert isinstance(event_hash, str)
- 65: def test_audittrailcore_verify_file_returns_result_object(tmp_path: Path) -> None:
- 71: assert hasattr(result, "is_valid")
- 72: assert hasattr(result, "total_events")
- 73: assert hasattr(result, "validated_events")

## tests/test_AuditTrailMixin.py

- 16: from __future__ import annotations
- 18: from importlib import import_module
- 19: from typing import Any
- 21: import pytest
- 24: def _load_mixin() -> Any:
- 35: def test_audittrailmixin_returns_none_when_no_core() -> None:
- 39: class _Host(audit_trail_mixin_cls):
- 42: def _get_audit_trail_core(self) -> Any:
- 55: def test_audittrailmixin_delegates_to_core_append_event_dict() -> None:
- 59: class _FakeCore:
- 62: def __init__(self) -> None:
- 66: def append_event_dict(self, **kwargs: Any) -> str:
- 71: class _Host(audit_trail_mixin_cls):
- 74: def __init__(self) -> None:
- 78: def _get_audit_trail_core(self) -> Any:

## tests/test_AuditVerificationResult.py

- 16: from __future__ import annotations
- 18: from dataclasses import FrozenInstanceError
- 19: from importlib import import_module
- 20: from typing import Any
- 22: import pytest
- 25: def _load_result_type() -> Any:
- 42: def test_auditverificationresult_fields_are_exposed() -> None:
- 60: def test_auditverificationresult_is_immutable() -> None:

## tests/test_AutoMemCore.py

- 21: from __future__ import annotations
- 23: from src.core.memory.AutoMemCore import AutoMemCore, validate
- 26: def test_auto_mem_core_validate() -> None:
- 31: def test_auto_mem_core_is_importable() -> None:
- 34: assert issubclass(AutoMemCore, object)

## tests/test_BenchmarkRunner.py

- 22: from __future__ import annotations
- 24: from src.core.memory.BenchmarkRunner import BenchmarkRunner, validate
- 27: def test_benchmark_runner_validate() -> None:
- 32: def test_benchmark_runner_is_importable() -> None:
- 35: assert issubclass(BenchmarkRunner, object)

## tests/test_CircuitBreakerConfig.py

- 21: from __future__ import annotations
- 23: from src.core.resilience.CircuitBreakerConfig import CircuitBreakerConfig, validate  # type: ignore[import]
- 26: def test_circuit_breaker_config_validate() -> None:
- 31: def test_circuit_breaker_config_defaults_are_constructible() -> None:

## tests/test_CircuitBreakerCore.py

- 21: from __future__ import annotations
- 23: from src.core.resilience.CircuitBreakerCore import CircuitBreakerCore, validate  # type: ignore[import]
- 24: from src.core.resilience.CircuitBreakerState import CircuitBreakerState, CircuitState  # type: ignore[import]
- 27: def test_circuit_breaker_core_validate() -> None:
- 32: def test_circuit_breaker_core_reset_moves_state_to_closed() -> None:

## tests/test_CircuitBreakerMixin.py

- 21: from __future__ import annotations
- 23: import pytest
- 25: from src.core.resilience.CircuitBreakerConfig import CircuitBreakerConfig  # type: ignore[import]
- 26: from src.core.resilience.CircuitBreakerMixin import CircuitBreakerMixin, validate  # type: ignore[import]
- 27: from src.core.resilience.CircuitBreakerRegistry import CircuitBreakerRegistry  # type: ignore[import]
- 30: class _Agent(CircuitBreakerMixin):
- 33: def __init__(self) -> None:
- 38: def test_circuit_breaker_mixin_validate() -> None:
- 44: async def test_circuit_breaker_mixin_cb_call_success_path() -> None:
- 49: async def _ok() -> int:

## tests/test_CircuitBreakerRegistry.py

- 21: from __future__ import annotations
- 23: import pytest
- 25: from src.core.resilience.CircuitBreakerConfig import CircuitBreakerConfig  # type: ignore[import]
- 26: from src.core.resilience.CircuitBreakerRegistry import CircuitBreakerRegistry, validate  # type: ignore[import]
- 29: def test_circuit_breaker_registry_validate() -> None:
- 35: async def test_circuit_breaker_registry_get_or_create_returns_state() -> None:

## tests/test_CircuitBreakerState.py

- 17: from src.core.resilience.CircuitBreakerState import CircuitBreakerState, CircuitState, validate
- 20: def test_circuit_breaker_state_defaults() -> None:
- 29: def test_circuit_breaker_state_validate_hook() -> None:

## tests/test_ContextTransactionManager.py

- 37: from __future__ import annotations
- 39: import uuid
- 41: import pytest
- 48: from src.core.ContextTransactionManager import ContextTransaction as _CoreContextTx
- 49: from src.core.ContextTransactionManager import RecursionGuardError as _CoreRecursionGuardError
- 50: from src.core.ContextTransactionManager import validate as _core_context_validate
- 60: def _skip_if_no_core_context() -> None:
- 65: def _skip_if_no_tx_context() -> None:
- 67: import src.transactions.ContextTransactionManager  # noqa: F401
- 77: class TestContextTransactionShim:
- 81: def test_shim_exports_context_transaction_and_recursion_guard_error(self) -> None:
- 84: from src.core.ContextTransactionManager import (  # noqa: PLC0415
- 90: assert callable(ContextTransaction)
- 91: assert issubclass(RecursionGuardError, Exception)
- 94: def test_shim_validate_returns_true(self) -> None:
- 97: from src.core.ContextTransactionManager import validate  # noqa: PLC0415
- 99: assert callable(validate)
- 103: def test_transaction_id_is_uuid4_on_construction(self) -> None:
- 106: from src.core.ContextTransactionManager import ContextTransaction  # noqa: PLC0415
- 118: def test_nested_context_has_parent_id_linked_to_outer(self) -> None:
- 121: from src.core.ContextTransactionManager import ContextTransaction  # noqa: PLC0415
- 135: def test_active_contexts_reflects_enter_and_exit(self) -> None:
- 138: from src.core.ContextTransactionManager import ContextTransaction  # noqa: PLC0415
- 155: def test_recursion_guard_error_on_reentrant_context_id(self) -> None:
- 158: from src.core.ContextTransactionManager import ContextTransaction, RecursionGuardError  # noqa: PLC0415
- 166: def test_empty_context_id_raises_value_error(self) -> None:
- 169: from src.core.ContextTransactionManager import ContextTransaction  # noqa: PLC0415
- 175: def test_current_classmethod_returns_innermost(self) -> None:
- 178: from src.core.ContextTransactionManager import ContextTransaction  # noqa: PLC0415
- 193: async def test_async_context_manager_enters_and_exits(self) -> None:
- 196: from src.core.ContextTransactionManager import ContextTransaction  # noqa: PLC0415
- 203: assert isinstance(ctx, ContextTransaction)
- 215: class TestContextTransactionFull:
- 219: def test_package_import_and_validate(self) -> None:
- 222: from src.transactions.ContextTransactionManager import (
- 228: assert callable(validate)
- 232: def test_uuid_lineage_outer_has_no_parent_inner_linked(self) -> None:
- 235: from src.transactions.ContextTransactionManager import ContextTransaction  # noqa: PLC0415
- 245: def test_current_returns_none_when_no_active_context(self) -> None:
- 248: from src.transactions.ContextTransactionManager import ContextTransaction  # noqa: PLC0415
- 255: def test_recursion_guard_leaves_no_state_leak_after_error(self) -> None:
- 260: from src.transactions.ContextTransactionManager import (  # noqa: PLC0415

## tests/test_FuzzCase.py

- 17: from __future__ import annotations
- 19: from tests.test_fuzzing_core import _build_case, _require_symbol
- 22: def test_fuzz_case_exposes_contract_fields() -> None:

## tests/test_FuzzCorpus.py

- 17: from __future__ import annotations
- 19: from tests.test_fuzzing_core import _require_symbol
- 22: def test_fuzz_corpus_exposes_indexed_bytes_entries() -> None:

## tests/test_FuzzEngineCore.py

- 17: from __future__ import annotations
- 19: from tests.test_fuzzing_core import _require_symbol
- 22: def test_fuzz_engine_core_exposes_campaign_scheduler_contract() -> None:
- 25: assert hasattr(engine_cls, "schedule_cases")

## tests/test_FuzzMutator.py

- 17: from __future__ import annotations
- 19: from tests.test_fuzzing_core import _require_symbol
- 22: def test_fuzz_mutator_mutate_contract_returns_bytes() -> None:
- 26: assert isinstance(payload, bytes)

## tests/test_FuzzResult.py

- 17: from __future__ import annotations
- 19: from tests.test_fuzzing_core import _build_case, _require_symbol
- 22: def test_fuzz_result_aggregator_contract_from_case_results() -> None:

## tests/test_FuzzSafetyPolicy.py

- 17: from __future__ import annotations
- 19: from tests.test_fuzzing_core import _require_symbol
- 22: def test_fuzz_safety_policy_exposes_local_guard_contract() -> None:
- 33: assert hasattr(policy, "validate_target")

## tests/test_MemoryTransactionManager.py

- 35: from __future__ import annotations
- 37: from pathlib import Path
- 39: import pytest
- 44: from src.MemoryTransactionManager import MemoryTransaction  # must work NOW
- 47: class TestMemoryTransactionShim:
- 51: def test_import_memory_transaction(self) -> None:
- 54: assert callable(MemoryTransaction)
- 57: def test_sync_context_manager_reentrant(self) -> None:
- 67: def test_sync_context_manager_releases_lock(self) -> None:
- 79: async def test_async_context_manager_completes(self) -> None:
- 84: assert isinstance(tx, MemoryTransaction)
- 88: def test_module_level_validate_exists_and_returns_true(self) -> None:
- 94: import src.MemoryTransactionManager as _mod
- 108: def _skip_if_no_tx_memory() -> None:
- 111: import src.transactions.MemoryTransactionManager  # noqa: F401
- 116: class TestMemoryTransactionUpgraded:
- 120: def test_package_import_and_validate(self) -> None:
- 123: from src.transactions.MemoryTransactionManager import MemoryTransaction as MTx  # noqa: PLC0415
- 124: from src.transactions.MemoryTransactionManager import validate  # noqa: PLC0415
- 126: assert callable(validate)
- 132: async def test_set_get_delete_key_value(self) -> None:
- 135: from src.transactions.MemoryTransactionManager import MemoryTransaction as MTx  # noqa: PLC0415
- 148: async def test_commit_flushes_pending_into_store(self) -> None:
- 151: from src.transactions.MemoryTransactionManager import MemoryTransaction as MTx  # noqa: PLC0415
- 163: async def test_rollback_discards_pending(self) -> None:
- 166: from src.transactions.MemoryTransactionManager import MemoryTransaction as MTx  # noqa: PLC0415
- 177: async def test_sync_remote_dry_run_returns_payload_dict(self) -> None:
- 180: from src.transactions.MemoryTransactionManager import MemoryTransaction as MTx  # noqa: PLC0415
- 192: async def test_encrypt_decrypt_roundtrip_with_real_security_bridge(
- 199: from src.core import security_bridge  # noqa: PLC0415
- 200: from src.transactions.MemoryTransactionManager import MemoryTransaction as MTx  # noqa: PLC0415
- 207: source = {"k": "v", "n": 7}
- 210: assert isinstance(raw, dict)
- 218: async def test_encrypt_without_key_file_env_raises_value_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
- 221: from src.transactions.MemoryTransactionManager import MemoryTransaction as MTx  # noqa: PLC0415

## tests/test_N8nBridgeConfig.py

- 17: from __future__ import annotations
- 19: from importlib import import_module
- 20: from typing import Any
- 22: import pytest
- 25: def _load_symbol(module_name: str, symbol_name: str) -> Any:
- 39: def test_n8n_bridge_config_from_env_loads_expected_values() -> None:
- 60: def test_n8n_bridge_config_validate_rejects_invalid_runtime_values() -> None:

## tests/test_N8nBridgeCore.py

- 17: from __future__ import annotations
- 19: from importlib import import_module
- 20: from typing import Any
- 22: import pytest
- 25: def _load_symbol(module_name: str, symbol_name: str) -> Any:
- 39: def _new_config() -> Any:
- 58: async def test_n8n_bridge_core_rejects_duplicate_event_ids_within_ttl() -> None:
- 82: async def test_n8n_bridge_core_trigger_workflow_returns_bridge_result() -> None:
- 95: assert isinstance(result, dict)

## tests/test_N8nBridgeMixin.py

- 17: from __future__ import annotations
- 19: from importlib import import_module
- 20: from typing import Any
- 22: import pytest
- 25: def _load_symbol(module_name: str, symbol_name: str) -> Any:
- 40: async def test_n8n_bridge_mixin_n8n_trigger_delegates_to_core() -> None:
- 44: class _Core:
- 47: async def trigger_workflow(
- 73: class _Host(mixin_cls):
- 76: def __init__(self) -> None:
- 88: async def test_n8n_bridge_mixin_n8n_handle_callback_delegates_to_core() -> None:
- 92: class _Core:
- 95: async def handle_inbound_event(
- 114: class _Host(mixin_cls):
- 117: def __init__(self) -> None:

## tests/test_N8nEventAdapter.py

- 17: from __future__ import annotations
- 19: from importlib import import_module
- 20: from typing import Any
- 22: import pytest
- 25: def _load_symbol(module_name: str, symbol_name: str) -> Any:
- 39: def test_n8n_event_adapter_maps_valid_inbound_payload() -> None:
- 60: def test_n8n_event_adapter_rejects_missing_required_ids() -> None:

## tests/test_N8nHttpClient.py

- 17: from __future__ import annotations
- 19: from importlib import import_module
- 20: from typing import Any
- 22: import pytest
- 25: def _load_symbol(module_name: str, symbol_name: str) -> Any:
- 39: def _new_config() -> Any:
- 58: async def test_n8n_http_client_post_json_includes_auth_and_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
- 66: class _Response:
- 71: def read(self) -> bytes:
- 75: def getheaders(self) -> list[tuple[str, str]]:
- 79: def _fake_urlopen(request: Any, timeout: float) -> _Response:
- 93: async def test_n8n_http_client_retries_retryable_failures(monkeypatch: pytest.MonkeyPatch) -> None:
- 100: class _Response:
- 105: def read(self) -> bytes:
- 109: def getheaders(self) -> list[tuple[str, str]]:
- 113: def _fake_urlopen(_: Any, __: float) -> _Response:
- 117: raise OSError("temporary")

## tests/test_ProcessTransactionManager.py

- 36: from __future__ import annotations
- 38: import sys
- 40: import pytest
- 47: from src.core.ProcessTransactionManager import ProcessTransaction as _CoreProcessTx
- 48: from src.core.ProcessTransactionManager import validate as _core_process_validate
- 57: def _skip_if_no_core_process() -> None:
- 62: def _skip_if_no_tx_process() -> None:
- 64: import src.transactions.ProcessTransactionManager  # noqa: F401
- 74: class TestProcessTransactionShim:
- 78: def test_shim_import_provides_process_transaction(self) -> None:
- 81: from src.core.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415
- 84: assert callable(ProcessTransaction)
- 87: def test_shim_validate_returns_true(self) -> None:
- 90: from src.core.ProcessTransactionManager import validate  # noqa: PLC0415
- 92: assert callable(validate)
- 96: def test_start_creates_popen_with_pipe(self) -> None:
- 99: import subprocess  # noqa: PLC0415
- 101: from src.core.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415
- 117: def test_wait_returns_returncode_and_sets_stdout(self) -> None:
- 120: from src.core.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415
- 133: def test_rollback_terminates_running_process(self) -> None:
- 136: from src.core.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415
- 148: def test_exception_in_context_triggers_rollback(self) -> None:
- 151: from src.core.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415
- 160: raise ValueError("abort-test")
- 168: async def test_async_start_and_wait_returns_zero(self) -> None:
- 171: from src.core.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415
- 186: class TestProcessTransactionFull:
- 190: def test_package_import_and_validate(self) -> None:
- 193: from src.transactions.ProcessTransactionManager import (
- 199: assert callable(validate)
- 204: async def test_async_run_returns_three_tuple(self) -> None:
- 207: from src.transactions.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415
- 222: async def test_async_run_returncode_matches_exit_status(self) -> None:
- 225: from src.transactions.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415
- 239: async def test_async_run_stdout_captures_output(self) -> None:
- 242: from src.transactions.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415
- 253: async def test_async_rollback_terminates_async_process(self) -> None:
- 256: from src.transactions.ProcessTransactionManager import ProcessTransaction  # noqa: PLC0415

## tests/test_ReplayEnvelope.py

- 17: from __future__ import annotations
- 19: from typing import Any
- 21: from tests.test_shadow_replay import _replay_envelope_payload, _require_symbol
- 24: def test_replay_envelope_exposes_contract_constructor() -> None:

## tests/test_ReplayMixin.py

- 17: from __future__ import annotations
- 19: from typing import Any
- 21: import pytest
- 23: from tests.test_shadow_replay import _require_symbol
- 27: async def test_replay_mixin_replay_session_delegates_with_flag() -> None:
- 31: class _Orchestrator:
- 34: def __init__(self) -> None:
- 38: async def replay_session(
- 49: class _Host(replay_mixin_cls):
- 52: def __init__(self) -> None:

## tests/test_ReplayOrchestrator.py

- 17: from __future__ import annotations
- 19: from typing import Any
- 21: import pytest
- 23: from tests.test_shadow_replay import _build_envelope, _require_symbol
- 27: async def test_replay_orchestrator_replay_session_returns_summary() -> None:
- 31: class _Store:
- 34: async def load_session(self, _session_id: str) -> list[Any]:
- 41: class _ShadowCore:
- 44: async def execute_envelope(self, _envelope: Any, *, deterministic_seed: int \| None = None) -> Any:

## tests/test_ReplayStore.py

- 17: from __future__ import annotations
- 19: from typing import Any
- 21: import pytest
- 23: from tests.test_shadow_replay import _build_envelope, _require_symbol
- 27: async def test_replay_store_persists_and_loads_one_envelope(tmp_path: Any) -> None:

## tests/test_SandboxConfig.py

- 21: from __future__ import annotations
- 23: from src.core.sandbox.SandboxConfig import SandboxConfig, validate
- 26: def test_sandbox_config_validate() -> None:
- 31: def test_sandbox_config_from_strings_round_trips() -> None:
- 39: def test_sandbox_config_agent_id_auto_generated() -> None:
- 42: assert isinstance(cfg.agent_id, str)

## tests/test_SandboxMixin.py

- 21: from __future__ import annotations
- 23: from src.core.sandbox.SandboxConfig import SandboxConfig
- 24: from src.core.sandbox.SandboxMixin import SandboxMixin, validate
- 25: from src.core.sandbox.SandboxViolationError import SandboxViolationError
- 28: def test_sandbox_mixin_validate() -> None:
- 33: def test_sandbox_mixin_sandbox_tx_returns_transaction() -> None:
- 36: class Agent(SandboxMixin):
- 39: def __init__(self) -> None:
- 48: def test_sandbox_mixin_validate_host_raises_on_blocked_host() -> None:
- 50: import pytest
- 52: class Agent(SandboxMixin):
- 55: def __init__(self) -> None:

## tests/test_SandboxViolationError.py

- 21: from __future__ import annotations
- 23: from src.core.sandbox.SandboxViolationError import SandboxViolationError, validate
- 26: def test_sandbox_violation_error_validate() -> None:
- 31: def test_sandbox_violation_error_is_runtime_error() -> None:
- 33: assert issubclass(SandboxViolationError, RuntimeError)
- 36: def test_sandbox_violation_error_stores_fields() -> None:

## tests/test_SandboxedStorageTransaction.py

- 21: from __future__ import annotations
- 23: from pathlib import Path
- 25: import pytest
- 27: from src.core.sandbox.SandboxConfig import SandboxConfig
- 28: from src.core.sandbox.SandboxedStorageTransaction import SandboxedStorageTransaction, validate
- 31: def test_sandboxed_storage_transaction_validate() -> None:
- 36: def test_sandboxed_storage_transaction_is_importable() -> None:
- 39: assert issubclass(SandboxedStorageTransaction, object)
- 43: async def test_sandboxed_storage_transaction_delete_inside_allowed_path(tmp_path: Path) -> None:
- 54: async def test_sandboxed_storage_transaction_mkdir_inside_allowed_path(tmp_path: Path) -> None:
- 64: def test_sandboxed_storage_transaction_commit_none_target_is_noop(tmp_path: Path) -> None:

## tests/test_ShadowExecutionCore.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass
- 20: from typing import Any
- 22: import pytest
- 24: from tests.test_shadow_replay import _build_envelope, _require_symbol
- 28: class _Tx:
- 34: async def commit(self) -> None:
- 38: async def rollback(self) -> None:
- 43: def _make_shadow_core() -> Any:
- 52: def _factory() -> _Tx:
- 65: async def test_shadow_execution_core_execute_envelope_returns_structured_result() -> None:
- 69: assert hasattr(result, "success")

## tests/test_StorageTransactionManager.py

- 37: from __future__ import annotations
- 39: from pathlib import Path
- 41: import pytest
- 48: from src.core.StorageTransactionManager import StorageTransaction as _CoreStorageTx
- 49: from src.core.StorageTransactionManager import validate as _core_storage_validate
- 58: def _skip_if_no_core_storage() -> None:
- 63: def _skip_if_no_tx_storage() -> None:
- 65: import src.transactions.StorageTransactionManager  # noqa: F401
- 75: class TestStorageTransactionShim:
- 79: def test_shim_import_provides_storage_transaction(self) -> None:
- 82: from src.core.StorageTransactionManager import StorageTransaction  # noqa: PLC0415
- 85: assert callable(StorageTransaction)
- 88: def test_shim_validate_returns_true(self) -> None:
- 91: from src.core.StorageTransactionManager import validate  # noqa: PLC0415
- 93: assert callable(validate)
- 97: def test_stage_and_commit_writes_bytes_to_target(self, tmp_path: Path) -> None:
- 100: from src.core.StorageTransactionManager import StorageTransaction  # noqa: PLC0415
- 110: def test_rollback_on_exception_leaves_original_file(self, tmp_path: Path) -> None:
- 113: from src.core.StorageTransactionManager import StorageTransaction  # noqa: PLC0415
- 122: raise RuntimeError("simulated abort")
- 127: def test_double_commit_raises(self, tmp_path: Path) -> None:
- 130: from src.core.StorageTransactionManager import StorageTransaction  # noqa: PLC0415
- 141: def test_commit_without_stage_does_not_crash(self, tmp_path: Path) -> None:
- 144: from src.core.StorageTransactionManager import StorageTransaction  # noqa: PLC0415
- 154: async def test_async_context_manager_commits(self, tmp_path: Path) -> None:
- 157: from src.core.StorageTransactionManager import StorageTransaction  # noqa: PLC0415
- 172: class TestStorageTransactionFull:
- 176: def test_package_import_and_validate(self) -> None:
- 179: from src.transactions.StorageTransactionManager import (
- 185: assert callable(validate)
- 190: async def test_async_write_and_acommit_creates_file(self, tmp_path: Path) -> None:
- 193: from src.transactions.StorageTransactionManager import StorageTransaction  # noqa: PLC0415
- 204: async def test_async_rollback_removes_tmp_target_absent(self, tmp_path: Path) -> None:
- 207: from src.transactions.StorageTransactionManager import StorageTransaction  # noqa: PLC0415
- 220: async def test_async_delete_removes_existing_file(self, tmp_path: Path) -> None:
- 223: from src.transactions.StorageTransactionManager import StorageTransaction  # noqa: PLC0415
- 236: async def test_async_mkdir_creates_directory(self, tmp_path: Path) -> None:
- 239: from src.transactions.StorageTransactionManager import StorageTransaction  # noqa: PLC0415
- 250: async def test_encryption_raises_without_master_key(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
- 256: from src.transactions.StorageTransactionManager import (  # noqa: PLC0415

## tests/test_UnifiedTransactionManager.py

- 17: from __future__ import annotations
- 19: import importlib
- 22: def test_unified_transaction_manager_module_has_validate() -> None:
- 25: assert hasattr(module, "validate")
- 26: assert callable(module.validate)
- 29: def test_unified_transaction_manager_validate_returns_bool() -> None:
- 32: assert isinstance(module.validate(), bool)

## tests/test_UniversalAgentShell.py

- 17: from __future__ import annotations
- 19: import asyncio
- 20: import importlib
- 21: from dataclasses import dataclass
- 22: from types import SimpleNamespace
- 23: from typing import Any
- 25: import pytest
- 28: def _import_or_fail(module_name: str) -> Any:
- 51: class _FakeRouter:
- 58: def classify(self, envelope: Any) -> Any:
- 77: class _FakeHandler:
- 84: async def execute(self, envelope: Any) -> dict[str, Any]:
- 105: raise AssertionError(f"Unknown fake mode: {self.mode}")
- 109: class _FakeRegistry:
- 116: def resolve(self, intent: str) -> _FakeHandler:
- 139: def _make_envelope(router_mod: Any, *, intent: str \| None = "summarize") -> Any:
- 159: async def test_dispatch_routes_allowlisted_intent_to_core() -> None:
- 179: async def test_dispatch_routes_non_allowlisted_intent_to_legacy() -> None:
- 186: async def _legacy(envelope: Any) -> dict[str, str]:
- 213: async def test_dispatch_falls_back_on_registry_miss_once() -> None:
- 220: async def _legacy(envelope: Any) -> dict[str, str]:
- 247: async def test_dispatch_falls_back_on_core_execution_error() -> None:
- 253: async def _legacy(envelope: Any) -> dict[str, str]:
- 279: async def test_dispatch_falls_back_on_core_timeout() -> None:
- 285: async def _legacy(envelope: Any) -> dict[str, str]:
- 311: async def test_dispatch_raises_envelope_validation_error_for_invalid_envelope() -> None:
- 328: async def test_dispatch_does_not_retry_fallback_when_legacy_dispatch_fails() -> None:
- 335: async def _legacy(envelope: Any) -> dict[str, str]:
- 347: raise RuntimeError("legacy failed")
- 363: async def test_dispatch_result_includes_route_intent_and_fallback_reason() -> None:
- 369: async def _legacy(envelope: Any) -> dict[str, str]:
- 390: assert hasattr(result, "route")
- 391: assert hasattr(result, "intent")
- 392: assert hasattr(result, "fallback_reason")

## tests/test_UniversalCoreRegistry.py

- 17: from __future__ import annotations
- 19: import importlib
- 20: import inspect
- 21: from dataclasses import dataclass
- 22: from typing import Any
- 24: import pytest
- 27: def _import_or_fail(module_name: str) -> Any:
- 50: class _Handler:
- 55: async def execute(self, envelope: Any) -> dict[str, str]:
- 69: def test_register_valid_factory_succeeds() -> None:
- 79: def test_register_duplicate_intent_raises_core_registration_error() -> None:
- 90: def test_resolve_registered_intent_returns_handler_with_execute() -> None:
- 98: assert hasattr(handler, "execute")
- 102: def test_resolve_missing_intent_raises_core_not_registered_error() -> None:
- 112: def test_list_intents_returns_stable_tuple() -> None:
- 122: assert isinstance(first, tuple)
- 123: assert isinstance(second, tuple)

## tests/test_UniversalIntentRouter.py

- 17: from __future__ import annotations
- 19: import importlib
- 20: from typing import Any
- 22: import pytest
- 25: def _import_or_fail(module_name: str) -> Any:
- 47: def _make_envelope(router_mod: Any, *, intent: str \| None) -> Any:
- 66: def test_normalize_intent_lowercases_known_value() -> None:
- 75: def test_normalize_intent_none_returns_unknown() -> None:
- 84: def test_classify_allowlisted_intent_prefers_core() -> None:
- 95: def test_classify_non_allowlisted_intent_prefers_legacy() -> None:
- 106: def test_classify_is_deterministic_for_identical_envelope() -> None:

## tests/test_agent_doc_frequency.py

- 19: from __future__ import annotations
- 21: import sys
- 22: from datetime import datetime, timezone
- 23: from pathlib import Path
- 25: import pytest
- 30: from AgentDocFrequency import DocStats, analyse_docs, format_table  # type: ignore[import]  # noqa: E402
- 35: def test_docstats_defaults():
- 43: def test_docstats_fields_assignable():
- 55: def test_format_table_contains_header():
- 62: def test_format_table_contains_separator():
- 68: def test_format_table_includes_doc_name():
- 80: def test_format_table_never_for_no_last_updated():
- 89: REPO_ROOT = Path(__file__).parent.parent
- 90: DOCS_DIR = REPO_ROOT / ".github" / "agents" / "data"
- 94: def test_analyse_docs_returns_all_memory_files():
- 98: assert len(result) == len(expected)
- 102: def test_analyse_docs_sorted_by_staleness_desc():
- 110: def test_analyse_docs_staleness_in_range():
- 118: def test_analyse_docs_commit_count_non_negative():
- 126: def test_analyse_docs_full_table_output():
- 137: def test_main_runs_without_error(capsys):
- 139: import sys
- 141: import AgentDocFrequency  # type: ignore[import]

## tests/test_agent_memory.py

- 19: from __future__ import annotations
- 21: from unittest.mock import AsyncMock, MagicMock, patch
- 23: import pytest
- 24: from fastapi.testclient import TestClient
- 26: from backend.app import app
- 27: from backend.memory_store import MemoryStore, _memory_path
- 29: client = TestClient(app)
- 35: _AGENT = "test-agent-memory-prj65"
- 38: def _make_store_with_entries(entries: list[dict]) -> MagicMock:
- 60: def test_append_creates_entry():
- 84: def test_read_returns_entries():
- 101: assert isinstance(entries, list)
- 106: def test_read_limit_param():
- 125: def test_clear_removes_entries():
- 134: def test_unauthenticated_get_rejected():
- 136: import backend.auth as _auth
- 151: def test_invalid_role_missing_content():
- 167: def test_memory_path_rejects_traversal():
- 173: def test_memory_path_rejects_slash():

## tests/test_agent_registry.py

- 4: import time
- 6: from swarm.agent_registry import AgentRegistry
- 9: def test_register_and_query() -> None:
- 16: def test_heartbeat_marks_healthy() -> None:
- 24: def test_missing_heartbeat_unhealthy() -> None:

## tests/test_api_ideas.py

- 19: from __future__ import annotations
- 21: import json
- 22: import re
- 23: from pathlib import Path
- 25: from fastapi.testclient import TestClient
- 27: from backend.app import app
- 29: _CLIENT = TestClient(app, raise_server_exceptions=False)
- 30: _ROOT = Path(__file__).resolve().parents[1]
- 31: _IDEAS_DIR = _ROOT / "docs" / "project" / "ideas"
- 32: _PROJECTS_PATH = _ROOT / "data" / "projects.json"
- 33: _PLANNED_MAPPING_PATTERN = re.compile(r"^Planned project mapping:\s*(.+)$", re.IGNORECASE)
- 34: _PROJECT_ID_PATTERN = re.compile(r"prj\d{7}", re.IGNORECASE)
- 35: _IDEA_ID_PATTERN = re.compile(r"(idea\d{6})", re.IGNORECASE)
- 38: def _idea_files() -> list[Path]:
- 48: def _extract_idea_id(idea_file: Path) -> str:
- 66: def _mapped_project_ids(idea_file: Path) -> list[str]:
- 96: def _project_lane_map() -> dict[str, str]:
- 107: def _expected_ids_for_implemented_exclude(mode: str) -> set[str]:
- 132: def test_api_ideas_returns_ideas_loaded_from_docs_project_ideas() -> None:
- 141: assert isinstance(payload, list)
- 146: assert all(str(item["source_path"]).replace("\\", "/").startswith("docs/project/ideas/") for item in payload)
- 149: def test_implemented_false_excludes_ideas_mapped_to_active_or_released_lanes() -> None:
- 161: assert isinstance(payload, list)
- 168: def test_implemented_mode_released_only_excludes_released_lanes_only() -> None:
- 180: assert isinstance(payload, list)
- 187: def test_rank_sort_is_stable_with_idea_id_tie_break() -> None:
- 203: assert isinstance(payload, list)
- 214: def test_malformed_idea_file_does_not_crash_endpoint() -> None:
- 225: assert isinstance(payload, list)
- 230: def test_patch_idea_updates_title_summary_and_mapping() -> None:
- 273: def test_patch_idea_ensures_swot_and_risk_sections() -> None:

## tests/test_api_projects_lane_sync.py

- 16: from __future__ import annotations
- 18: import shutil
- 19: from pathlib import Path
- 21: from fastapi.testclient import TestClient
- 23: import backend.app as app_mod
- 26: def test_projects_auto_advance_to_in_sprint_from_stage_artifacts(monkeypatch) -> None:
- 69: def test_projects_auto_advance_to_review_from_exec_or_ql_artifacts(monkeypatch) -> None:

## tests/test_api_versioning.py

- 19: from __future__ import annotations
- 21: import pytest
- 22: from fastapi.testclient import TestClient
- 24: from backend.app import app
- 26: client = TestClient(app)
- 29: def test_v1_health_routable():
- 36: def test_v1_livez_routable():
- 43: def test_v1_readyz_routable():
- 51: def test_readyz_degraded_when_forced(path: str, monkeypatch: pytest.MonkeyPatch):
- 65: def test_v1_agent_log_routable():
- 71: def test_v1_projects_routable():
- 77: def test_v1_returns_version_header():
- 83: def test_v1_agent_memory_routable():
- 89: def test_unversioned_returns_deprecation_header():

## tests/test_async_loops.py

- 4: import ast
- 5: import pathlib
- 7: import pytest
- 9: KNOWN_SYNC_LOOP_PATHS: set[str] = {
- 22: class LoopChecker(ast.NodeVisitor):
- 25: def __init__(self, path: pathlib.Path) -> None:
- 30: def visit(self, node: ast.AST) -> None:
- 37: def visit_For(self, node: ast.For) -> None:
- 42: def visit_While(self, node: ast.While) -> None:
- 47: def _check_loop(self, node: ast.stmt) -> None:
- 61: def test_no_sync_loops() -> None:
- 71: source = path.read_text(encoding="utf-8")

## tests/test_async_transport.py

- 20: import struct
- 22: import pytest
- 25: import rust_core
- 31: pytestmark = pytest.mark.skipif(not HAS_RUST, reason="rust_core not compiled")
- 39: def _make_transport(capacity: int = 64):
- 49: def test_module_importable():
- 54: def test_pyasynctransport_instantiation():
- 60: def test_get_capacity_small():
- 66: def test_get_capacity_large():
- 72: def test_get_capacity_zero():
- 78: def test_create_channel_returns_two_elements():
- 85: def test_create_channel_send_handle_encodes_capacity():
- 94: def test_create_channel_recv_handle_encodes_capacity():
- 103: def test_multiple_instances_independent():

## tests/test_audit_trail.py

- 16: from __future__ import annotations
- 18: import json
- 19: import re
- 20: from importlib import import_module
- 21: from pathlib import Path
- 22: from typing import Any
- 23: from uuid import uuid4
- 25: import pytest
- 28: def _load_audit_symbol(module_name: str, symbol_name: str) -> Any:
- 57: def _new_event_payload() -> dict[str, Any]:
- 67: def _make_event(payload: dict[str, Any] \| None = None) -> Any:
- 92: def _make_core(tmp_path: Path, *, fail_closed: bool = True) -> Any:
- 108: def _audit_file_for(core: Any) -> Path:
- 125: def _read_jsonl(path: Path) -> list[dict[str, Any]]:
- 141: def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
- 155: def _append_three(core: Any) -> list[str]:
- 172: def test_event_canonical_dict_contains_required_keys_and_schema_version() -> None:
- 193: def test_event_canonical_dict_stable_across_payload_insertion_order() -> None:
- 202: def test_hasher_canonical_event_bytes_deterministic_for_same_event() -> None:
- 214: def test_compute_event_hash_returns_64_lowercase_hex() -> None:
- 220: assert isinstance(event_hash, str)
- 224: def test_get_last_hash_returns_genesis_for_empty_and_latest_for_non_empty(tmp_path: Path) -> None:
- 236: def test_mixin_emit_event_returns_none_when_core_not_configured() -> None:
- 240: class _Host(audit_trail_mixin_cls):
- 243: def _get_audit_trail_core(self) -> Any:
- 256: def test_exception_hierarchy_preserves_specific_types_under_audittrailerror() -> None:
- 271: raise exc_type("x")
- 273: assert isinstance(caught, exc_type)
- 276: def test_append_event_uses_genesis_previous_hash_for_first_record(tmp_path: Path) -> None:
- 285: def test_append_event_links_previous_hash_to_prior_event_hash(tmp_path: Path) -> None:
- 295: def test_append_event_dict_matches_equivalent_auditevent_hash(tmp_path: Path) -> None:
- 335: def test_iter_records_preserves_append_order(tmp_path: Path) -> None:
- 359: def test_verify_file_valid_chain_with_three_events_returns_valid_result(tmp_path: Path) -> None:
- 371: def test_verify_file_empty_chain_is_valid_and_deterministic(tmp_path: Path) -> None:
- 381: def test_verify_file_detects_tampered_payload_in_middle_record(tmp_path: Path) -> None:
- 395: def test_verify_file_detects_broken_previous_hash_link(tmp_path: Path) -> None:
- 409: def test_verify_file_detects_malformed_hash_format(tmp_path: Path) -> None:
- 423: def test_verify_file_detects_malformed_json_line(tmp_path: Path) -> None:
- 436: def test_fail_closed_true_raises_auditpersistenceerror_on_unwritable_path(tmp_path: Path) -> None:
- 446: def test_event_canonical_handles_nested_lists_and_dicts() -> None:
- 455: def test_event_to_canonical_rejects_unsupported_schema_version() -> None:
- 476: def test_event_from_json_dict_rejects_missing_key() -> None:
- 492: def test_event_from_json_dict_rejects_invalid_payload_type() -> None:
- 509: def test_event_from_json_dict_rejects_non_integer_schema_version() -> None:
- 526: def test_append_event_returns_empty_string_when_fail_open_on_persistence_error(tmp_path: Path) -> None:
- 533: def test_append_event_returns_empty_string_when_hasher_raises_oserror(
- 541: def _raise_oserror(_: Any) -> bytes:
- 542: raise OSError("boom")
- 548: def test_iter_records_skips_blank_lines(tmp_path: Path) -> None:
- 557: def test_iter_records_rejects_non_object_json_line(tmp_path: Path) -> None:
- 567: def test_iter_records_rejects_malformed_json_line(tmp_path: Path) -> None:
- 577: def test_verify_file_skips_blank_lines_between_records(tmp_path: Path) -> None:
- 589: def test_verify_file_detects_malformed_non_object_record(tmp_path: Path) -> None:
- 599: def test_verify_file_detects_missing_hash_fields(tmp_path: Path) -> None:
- 612: def test_verify_file_detects_serialization_error_from_event_shape(tmp_path: Path) -> None:
- 625: def test_verify_file_reports_persistence_error_when_open_fails(tmp_path: Path) -> None:
- 629: class _BrokenPath:
- 632: def exists(self) -> bool:
- 636: def open(self, *_args: Any, **_kwargs: Any) -> Any:
- 638: raise OSError("cannot open")
- 646: def test_get_last_hash_falls_back_to_genesis_for_invalid_last_hash(tmp_path: Path) -> None:
- 653: def test_get_last_sequence_falls_back_to_record_count_when_non_integer(tmp_path: Path) -> None:
- 660: def test_append_event_creates_missing_parent_directory(tmp_path: Path) -> None:
- 669: def test_append_record_wraps_oserror_as_auditpersistenceerror(
- 678: def _patched_open(path_obj: Path, *args: Any, **kwargs: Any) -> Any:
- 680: raise OSError("forced open failure")
- 688: def test_audittrailmixin_base_get_core_returns_none() -> None:
- 694: def test_audittrailmixin_returns_none_on_audittrailerror_from_core() -> None:
- 699: class _FailingCore:
- 702: def append_event_dict(self, **_kwargs: Any) -> str:
- 704: raise audit_persistence_error("nope")
- 706: class _Host(audit_trail_mixin_cls):
- 709: def _get_audit_trail_core(self) -> Any:
- 717: def test_audittrailmixin_success_and_failure_helpers_delegate_event_types() -> None:
- 721: class _Core:
- 724: def __init__(self) -> None:
- 728: def append_event_dict(self, **kwargs: Any) -> str:
- 733: class _Host(audit_trail_mixin_cls):
- 736: def __init__(self) -> None:
- 740: def _get_audit_trail_core(self) -> Any:
- 753: def test_validate_helpers_return_true_for_all_audit_modules() -> None:

## tests/test_backend_auth.py

- 16: from __future__ import annotations
- 18: import jwt
- 19: import pytest
- 22: from fastapi.testclient import TestClient
- 26: import backend.app as app_mod
- 27: import backend.auth as auth_mod
- 34: def test_verify_api_key_match() -> None:
- 39: def test_verify_api_key_wrong() -> None:
- 44: def test_verify_api_key_none_provided() -> None:
- 49: def test_verify_api_key_empty_expected() -> None:
- 59: def test_verify_jwt_valid(monkeypatch: pytest.MonkeyPatch) -> None:
- 68: def test_verify_jwt_wrong_secret(monkeypatch: pytest.MonkeyPatch) -> None:
- 75: def test_verify_jwt_expired(monkeypatch: pytest.MonkeyPatch) -> None:
- 83: def test_verify_jwt_garbage(monkeypatch: pytest.MonkeyPatch) -> None:
- 89: def test_verify_jwt_none() -> None:
- 99: def test_health_no_auth_always_200(monkeypatch: pytest.MonkeyPatch) -> None:
- 108: def test_livez_no_auth_always_200(monkeypatch: pytest.MonkeyPatch) -> None:
- 117: def test_readyz_no_auth_always_200(monkeypatch: pytest.MonkeyPatch) -> None:
- 126: def test_rest_no_creds_returns_401(monkeypatch: pytest.MonkeyPatch) -> None:
- 135: def test_rest_valid_api_key_returns_200(monkeypatch: pytest.MonkeyPatch) -> None:
- 145: def test_rest_invalid_api_key_returns_401(monkeypatch: pytest.MonkeyPatch) -> None:
- 155: def test_rest_valid_jwt_returns_200(monkeypatch: pytest.MonkeyPatch) -> None:
- 166: def test_rest_invalid_jwt_returns_401(monkeypatch: pytest.MonkeyPatch) -> None:
- 177: def test_dev_mode_no_creds_passes(monkeypatch: pytest.MonkeyPatch) -> None:
- 184: def test_both_api_key_and_jwt_accepted(monkeypatch: pytest.MonkeyPatch) -> None:

## tests/test_backend_models.py

- 16: from backend.models import (
- 25: def test_init_message_valid():
- 30: def test_run_task_message_valid():
- 35: def test_task_delta_message_valid():
- 40: def test_action_request_message_valid():
- 45: def test_signal_message_valid():

## tests/test_backend_session_manager.py

- 16: from unittest.mock import AsyncMock
- 18: import pytest
- 20: from backend.session_manager import SessionManager
- 24: async def test_connect_returns_session_id():
- 28: assert isinstance(session_id, str)
- 35: async def test_disconnect_removes_session():
- 43: def test_disconnect_nonexistent_session_is_safe():

## tests/test_backend_system_metrics.py

- 21: from __future__ import annotations
- 23: import time
- 24: from unittest.mock import MagicMock, patch
- 26: import pytest
- 27: from fastapi.testclient import TestClient
- 29: import backend.app as _app_module
- 30: from backend.app import app
- 34: _CLIENT = TestClient(app)
- 40: def _vmem(
- 52: def _net_counter(bytes_sent: int = 0, bytes_recv: int = 0) -> MagicMock:
- 59: def _disk_counter(read_bytes: int = 0, write_bytes: int = 0) -> MagicMock:
- 66: def _psutil_mock(
- 84: def test_endpoint_returns_200():
- 92: def test_response_has_correct_shape():
- 103: def test_cpu_percent_is_in_valid_range():
- 114: def test_memory_fields_correct():
- 140: def test_network_entries_have_required_fields():
- 158: def test_loopback_and_virtual_interfaces_excluded():
- 183: def test_disk_fields_are_non_negative_numbers():
- 203: def test_sampled_at_is_positive_and_recent():
- 222: def test_first_call_returns_zero_rates():

## tests/test_backend_worker.py

- 19: from __future__ import annotations
- 21: import base64
- 22: import importlib
- 23: import json
- 25: from fastapi.testclient import TestClient
- 27: from backend.app import app
- 28: from backend.models import (
- 40: from backend.session_manager import SessionManager
- 41: from backend.ws_crypto import (
- 49: def test_backend_package_importable():
- 54: def test_backend_app_importable():
- 56: assert hasattr(mod, "app")
- 62: def test_init_message_schema():
- 69: def test_run_task_message_schema():
- 74: def test_task_started_message_type():
- 79: def test_task_delta_message_type():
- 86: def test_task_complete_status_default():
- 91: def test_task_error_code_default():
- 96: def test_action_request_message_schema():
- 101: def test_control_message_action():
- 106: def test_speech_transcript_is_final_default():
- 111: def test_signal_message_schema():
- 125: def test_session_manager_initially_empty():
- 130: def test_session_manager_get_unknown_returns_none():
- 135: def test_session_manager_disconnect_unknown_is_safe():
- 142: client = TestClient(app)
- 145: def test_health_endpoint():
- 154: def _ws_handshake(ws) -> bytes:  # type: ignore[no-untyped-def]
- 162: def _ws_send(ws, session_key: bytes, obj: dict) -> None:  # type: ignore[no-untyped-def]
- 168: def _ws_recv(ws, session_key: bytes) -> dict:  # type: ignore[no-untyped-def]
- 177: def test_ws_init_ack():
- 186: def test_ws_run_task_streams_tokens():
- 202: def test_ws_control_ack():
- 211: def test_ws_unknown_type_returns_error():
- 219: def test_ws_invalid_json_returns_error():

## tests/test_backend_ws_handler.py

- 16: import json
- 17: from unittest.mock import AsyncMock
- 19: import pytest
- 21: from backend.session_manager import SessionManager
- 22: from backend.ws_handler import handle_message
- 26: def ws():
- 33: def sessions():
- 38: async def test_init_message_sends_ack(ws, sessions):
- 39: await handle_message(sessions, "s1", ws, {"type": "init", "session_id": "s1"})
- 46: async def test_unknown_message_sends_error(ws, sessions):
- 47: await handle_message(sessions, "s1", ws, {"type": "unknownXYZ"})
- 54: async def test_run_task_streams_deltas(ws, sessions):

## tests/test_benchmarks.py

- 4: import importlib
- 5: import sys
- 6: from pathlib import Path
- 7: from types import ModuleType
- 8: from typing import Protocol, cast
- 11: benchmarks_path = Path(__file__).parent.parent / "benchmarks"
- 15: class SupportsRun(Protocol):
- 18: def run(self) -> dict[str, int]:
- 22: def test_simple_benchmark() -> None:
- 30: def mock_run() -> dict[str, int]:
- 37: assert isinstance(result, dict)

## tests/test_chat_api.py

- 4: import importlib
- 5: from typing import Callable, Protocol, TypedDict, cast
- 7: import pytest
- 8: from _pytest.monkeypatch import MonkeyPatch
- 13: from fastapi import FastAPI
- 14: from fastapi.testclient import TestClient
- 19: class CounterValueProtocol(Protocol):
- 22: def set(self, value: int) -> None:
- 25: def get(self) -> int:
- 29: class CounterProtocol(Protocol):
- 35: class MessagePayload(TypedDict):
- 42: class CapturedPost(TypedDict, total=False):
- 49: def _load_app() -> FastAPI:
- 55: def _load_messages_counter() -> CounterProtocol:
- 61: def test_create_and_post() -> None:
- 73: def test_tool_posts(monkeypatch: MonkeyPatch) -> None:
- 78: def fake_post(url: str, json: MessagePayload) -> object:
- 83: class Dummy:
- 88: def json(self) -> dict[str, bool]:
- 107: def test_metric_increment() -> None:
- 120: def test_duplicate_room_fails() -> None:
- 129: def test_post_to_missing_room() -> None:
- 137: def test_get_history_missing_room() -> None:

## tests/test_chat_mcp.py

- 4: import importlib
- 5: from typing import Callable, cast, get_type_hints
- 8: def _load_send_message_tool() -> Callable[..., object]:
- 14: def test_mcp_tool_signature() -> None:

## tests/test_chat_models.py

- 4: from chat.models import ChatRoom
- 7: def test_room_post_and_history() -> None:

## tests/test_chat_streaming.py

- 17: from __future__ import annotations
- 19: import json
- 21: import pytest
- 23: from chat.streaming import (
- 36: async def test_word_chunks_yields_each_word() -> None:
- 44: async def test_word_chunks_empty_string() -> None:
- 52: async def test_word_chunks_single_word() -> None:
- 58: async def test_word_chunks_preserves_leading_spaces() -> None:
- 75: async def test_collect_joins_all_chunks() -> None:
- 76: async def gen():
- 86: async def test_collect_empty_stream() -> None:
- 87: async def gen():
- 101: async def test_stream_to_sse_emits_token_events() -> None:
- 120: async def test_stream_to_sse_custom_event_names() -> None:
- 132: async def test_stream_to_sse_sequential_ids() -> None:
- 149: async def test_session_accumulates_full_text() -> None:
- 161: async def test_session_clear_resets_state() -> None:
- 172: async def test_session_not_finished_mid_stream() -> None:
- 176: async def check_progress():
- 182: await check_progress()
- 188: async def test_session_to_dict() -> None:
- 201: async def test_session_multiple_streams() -> None:

## tests/test_chat_utils.py

- 4: import importlib
- 5: from collections.abc import Callable, Sequence
- 6: from typing import Protocol, cast
- 9: class ChatRoomLike(Protocol):
- 16: def _load_chat_symbols() -> tuple[type[object], Callable[[str], ChatRoomLike]]:
- 25: def test_personal_room_creation() -> None:
- 29: assert isinstance(room, chat_room_type)
- 33: assert any(p.startswith("agent-") for p in room.participants)

## tests/test_circuit_breaker.py

- 21: from __future__ import annotations
- 23: import asyncio
- 24: from typing import Any, Awaitable, Callable
- 26: import pytest
- 28: import src.core.resilience as resilience_pkg
- 29: from src.core.resilience import (  # type: ignore[import]
- 39: from src.core.resilience.CircuitBreakerConfig import validate as validate_config
- 40: from src.core.resilience.CircuitBreakerCore import validate as validate_core
- 41: from src.core.resilience.CircuitBreakerMixin import validate as validate_mixin
- 42: from src.core.resilience.CircuitBreakerRegistry import validate as validate_registry
- 43: from src.core.resilience.CircuitBreakerState import validate as validate_state
- 44: from src.core.resilience.exceptions import validate as validate_exceptions
- 47: class _Agent(CircuitBreakerMixin):
- 50: def __init__(self, registry: CircuitBreakerRegistry) -> None:
- 60: def test_core_initial_state_closed() -> None:
- 68: def test_core_record_failure_increments_consecutive() -> None:
- 81: def test_core_opens_after_failure_threshold(monkeypatch: pytest.MonkeyPatch) -> None:
- 98: def test_core_half_open_after_recovery_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
- 113: def test_core_probe_success_transitions_to_closed() -> None:
- 131: def test_core_probe_failure_resets_to_open(monkeypatch: pytest.MonkeyPatch) -> None:
- 146: def test_core_half_open_probe_exclusivity() -> None:
- 159: def test_core_reset_forces_closed() -> None:
- 176: def test_core_record_success_increments_counters() -> None:
- 188: def test_core_should_allow_denies_open_before_recovery(monkeypatch: pytest.MonkeyPatch) -> None:
- 202: def test_core_check_state_returns_existing_non_open_state() -> None:
- 219: async def test_registry_get_or_create_same_key_returns_same_object() -> None:
- 231: async def test_registry_get_fallback_returns_first_closed_provider() -> None:
- 249: async def test_registry_get_fallback_returns_none_when_all_open() -> None:
- 264: async def test_registry_record_and_allow_delegate_to_core() -> None:
- 280: async def test_registry_state_creation_and_config_resolution_paths() -> None:
- 309: async def test_mixin_cb_call_returns_coro_result_on_success() -> None:
- 315: async def _ok() -> int:
- 327: async def test_mixin_cb_call_records_failure_and_reraises() -> None:
- 333: async def _boom() -> int:
- 335: raise RuntimeError("boom")
- 345: async def test_mixin_cb_call_open_circuit_raises_circuit_open_error_without_calling_coro() -> None:
- 356: async def _should_not_run() -> int:
- 368: async def test_mixin_cb_call_routes_to_fallback_when_primary_open() -> None:
- 379: async def _ok() -> str:
- 391: async def test_mixin_cb_call_raises_all_circuits_open_when_exhausted() -> None:
- 406: async def _never() -> int:
- 422: async def test_integration_open_then_half_open_then_closed_full_cycle(monkeypatch: pytest.MonkeyPatch) -> None:
- 449: async def test_integration_concurrent_half_open_only_one_probe_passes() -> None:
- 457: async def _attempt() -> bool:
- 467: def test_module_validate_helpers_and_exception_attributes() -> None:

## tests/test_compile.py

- 4: import asyncio
- 5: import importlib
- 6: from pathlib import Path
- 7: from typing import Protocol, cast
- 10: class CompileModuleProtocol(Protocol):
- 13: async def compile_architecture(self, descs: list[dict[str, str]], out: Path) -> None:
- 17: def test_compile_architecture(tmp_path: Path) -> None:
- 22: async def inner() -> None:

## tests/test_conftest.py

- 18: from __future__ import annotations
- 20: from pathlib import Path
- 21: from unittest.mock import Mock, patch
- 23: import pytest
- 25: import conftest as repo_conftest
- 28: def test_session_finish_sets_exitstatus_when_git_dirty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
- 40: from conftest import SessionManager
- 51: def test_session_finish_does_not_raise_with_minimal_session() -> None:
- 60: from conftest import _mgr
- 68: def test_resolve_import_fixer_prefers_scripts_then_scripts_old(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
- 81: from conftest import SessionManager
- 105: def test_resolve_import_fixer_prefers_scripts_dir(tmp_path: Path) -> None:
- 123: def test_resolve_import_fixer_falls_back_to_scripts_old(tmp_path: Path) -> None:
- 138: def test_resolve_import_fixer_returns_none_when_missing(tmp_path: Path) -> None:

## tests/test_consolidate_llm_context_cleanup_report.py

- 17: from __future__ import annotations
- 19: import subprocess
- 20: import sys
- 23: def test_apply_mode_writes_report_and_deletes_sources(tmp_path):

## tests/test_consolidate_llm_context_cli.py

- 17: from __future__ import annotations
- 19: import subprocess
- 20: import sys
- 23: def test_default_is_dry_run(tmp_path):
- 34: def test_apply_flag_changes_behavior(tmp_path):

## tests/test_consolidate_llm_context_docstrings.py

- 17: from __future__ import annotations
- 19: import subprocess
- 20: import sys
- 23: def _run_script(tmp_path, args=None) -> subprocess.CompletedProcess[str]:
- 41: def test_migrate_docstrings_inserts_block_and_is_idempotent(tmp_path):

## tests/test_consolidate_llm_context_integration.py

- 17: from __future__ import annotations
- 19: import subprocess
- 20: import sys
- 23: def test_full_integration_happy_path(tmp_path):
- 59: assert not (tmp_path / "docs" / "architecture" / "a.md").exists()
- 60: assert not (tmp_path / "pkg" / "m.description.md").exists()

## tests/test_consolidate_llm_context_outputs.py

- 21: from __future__ import annotations
- 23: import subprocess
- 24: import sys
- 25: from pathlib import Path
- 28: def _run_script(tmp_path, args=None) -> Path:
- 45: def test_outputs_are_created_and_contain_sources(tmp_path):

## tests/test_context_components.py

- 4: import importlib
- 5: from collections.abc import Callable
- 6: from pathlib import Path
- 7: from typing import Protocol, cast
- 9: import pytest
- 12: class ContextManagerProtocol(Protocol):
- 15: def push(self, *args: object, **kwargs: object) -> object:
- 19: class SkillsRegistryProtocol(Protocol):
- 22: async def list_skills(self) -> list[str]:
- 27: async def test_context_components_exist(tmp_path: Path) -> None:
- 36: assert hasattr(cm, "push")
- 39: assert isinstance(skills, list)

## tests/test_context_manager.py

- 4: import asyncio
- 5: import importlib
- 6: from collections.abc import Callable
- 7: from pathlib import Path
- 8: from typing import Protocol, cast
- 11: class ContextManagerProtocol(Protocol):
- 14: async def push(self, text: str) -> None:
- 17: def snapshot(self) -> str:
- 21: def _load_context_manager_factory() -> Callable[..., ContextManagerProtocol]:
- 27: def test_context_manager_basic(tmp_path: Path) -> None:
- 32: async def inner() -> None:
- 41: def test_context_manager_windowing(tmp_path: Path) -> None:
- 46: async def inner() -> None:

## tests/test_context_window.py

- 17: from __future__ import annotations
- 19: import pytest
- 21: from context_manager.window import ContextSegment, ContextWindow
- 28: def test_segment_token_count_basic() -> None:
- 33: def test_segment_token_count_empty() -> None:
- 38: def test_segment_to_dict_contains_expected_keys() -> None:
- 49: def test_segment_default_label_and_priority() -> None:
- 61: async def test_window_push_and_snapshot() -> None:
- 69: async def test_window_token_count() -> None:
- 77: async def test_window_clear() -> None:
- 86: async def test_window_push_returns_segment() -> None:
- 89: assert isinstance(seg, ContextSegment)
- 96: async def test_window_to_dict() -> None:
- 111: async def test_window_prunes_oldest_when_over_budget() -> None:
- 125: async def test_window_prunes_low_priority_first() -> None:
- 139: async def test_window_never_exceeds_max_tokens() -> None:
- 147: async def test_window_metadata_preserved() -> None:
- 155: async def test_window_segments_oldest_first() -> None:

## tests/test_core_agent_registry.py

- 5: def test_agent_registry_register_and_get() -> None:
- 7: import importlib

## tests/test_core_agent_state_manager.py

- 4: from src.core import agent_state_manager
- 7: def test_module_imports_and_validate() -> None:

## tests/test_core_config.py

- 17: from __future__ import annotations
- 19: import json
- 20: from pathlib import Path
- 22: import pytest
- 24: from src.core.config import AgentConfig, SwarmConfig, load_config, save_config
- 31: def test_agent_config_defaults() -> None:
- 42: def test_agent_config_custom_values() -> None:
- 60: def test_agent_config_empty_name_raises() -> None:
- 65: def test_agent_config_blank_name_raises() -> None:
- 70: def test_agent_config_negative_max_tokens_raises() -> None:
- 75: def test_agent_config_negative_timeout_raises() -> None:
- 80: def test_agent_config_empty_llm_model_raises() -> None:
- 90: def test_agent_config_to_dict_round_trip() -> None:
- 99: def test_agent_config_from_dict_unknown_keys_go_to_extra() -> None:
- 111: def test_swarm_config_defaults() -> None:
- 119: def test_swarm_config_log_level_normalised_to_upper() -> None:
- 124: def test_swarm_config_invalid_log_level_raises() -> None:
- 129: def test_swarm_config_nonpositive_concurrency_raises() -> None:
- 134: def test_swarm_config_nonpositive_heartbeat_raises() -> None:
- 144: def test_swarm_add_and_get_agent() -> None:
- 151: def test_swarm_remove_agent() -> None:
- 159: def test_swarm_remove_nonexistent_returns_none() -> None:
- 164: def test_swarm_enabled_agents_filters_disabled() -> None:
- 179: def test_swarm_config_to_dict_round_trip() -> None:
- 187: def test_swarm_config_from_dict() -> None:
- 207: def test_save_and_load_round_trip(tmp_path: Path) -> None:
- 222: def test_load_config_file_not_found(tmp_path: Path) -> None:
- 227: def test_load_config_invalid_json(tmp_path: Path) -> None:
- 234: def test_save_config_creates_parent_dirs(tmp_path: Path) -> None:

## tests/test_core_helpers.py

- 17: from __future__ import annotations
- 19: import asyncio
- 20: import importlib
- 23: def test_agent_registry_validate() -> None:
- 25: from src.core import agent_registry
- 30: def test_memory_validate() -> None:
- 32: from src.core import memory
- 37: def test_observability_validate() -> None:
- 39: from src.core import observability
- 44: def test_base_validate() -> None:
- 46: from src.core.base import validate as base_validate
- 51: def test_agent_state_manager_validate() -> None:
- 53: from src.core import agent_state_manager
- 58: def test_workflow_components() -> None:
- 79: def test_workflow_queue_and_task_validate() -> None:
- 88: def test_scaffold_import_and_example() -> None:
- 90: from src.core import scaffold
- 98: def test_basic_runtime_modules_validate() -> None:

## tests/test_core_memory.py

- 16: from src.core.memory import MemoryStore, validate
- 19: def test_memory_store_set_and_get():
- 25: def test_memory_store_default_for_missing():
- 31: def test_memory_store_overwrite():
- 38: def test_memory_store_multiple_keys():
- 46: def test_memory_store_stores_complex_values():
- 53: def test_memory_validate():

## tests/test_core_observability.py

- 4: from src.core import observability
- 7: def test_observability_import_and_validate() -> None:

## tests/test_core_providers_FlmChatAdapter.py

- 4: import pytest
- 9: from src.core.providers import FlmChatAdapter
- 14: def test_module_imports_and_validate() -> None:

## tests/test_core_providers_FlmModelProbe.py

- 17: from __future__ import annotations
- 19: import asyncio
- 20: import json
- 21: from unittest.mock import AsyncMock, patch
- 23: import pytest
- 25: from src.core.providers.FlmModelProbe import (
- 37: def test_probe_result_reachable_when_no_error() -> None:
- 47: def test_probe_result_not_reachable_when_error() -> None:
- 58: def test_probe_result_to_dict_keys() -> None:
- 78: def test_select_model_empty_returns_none() -> None:
- 82: def test_select_model_exact_match() -> None:
- 86: def test_select_model_prefix_match() -> None:
- 90: def test_select_model_substring_match() -> None:
- 95: def test_select_model_no_preferred_returns_first() -> None:
- 99: def test_select_model_preferred_not_found_returns_first() -> None:
- 108: def test_parse_models_body_happy_path() -> None:
- 113: def test_parse_models_body_empty_data() -> None:
- 118: def test_parse_models_body_missing_data_key() -> None:
- 123: def test_parse_models_body_invalid_json_raises() -> None:
- 128: def test_parse_models_body_data_not_list() -> None:
- 133: def test_parse_models_body_ignores_entries_without_id() -> None:
- 143: def _make_models_json(*ids: str) -> str:
- 148: async def test_probe_models_success() -> None:
- 161: async def test_probe_models_selects_preferred_exact() -> None:
- 171: async def test_probe_models_timeout() -> None:
- 172: async def _slow(*_a, **_kw):
- 182: async def test_probe_models_connection_error() -> None:
- 183: async def _fail(*_a, **_kw):
- 184: raise OSError("Connection refused")
- 193: async def test_probe_models_parse_error() -> None:
- 204: async def test_probe_models_base_url_normalisation() -> None:
- 208: async def _capture(url: str) -> str:
- 213: await probe_models("http://127.0.0.1:52625/")

## tests/test_core_providers_FlmProviderConfig.py

- 4: from src.core.providers import FlmProviderConfig
- 7: def test_module_imports_and_validate() -> None:

## tests/test_core_quality.py

- 8: from __future__ import annotations
- 10: import ast
- 11: import pathlib
- 12: from typing import Set
- 14: ROOT = pathlib.Path(".")
- 15: SRC = ROOT / "src"
- 16: TESTS = ROOT / "tests"
- 18: NO_VALIDATE_ALLOWED: Set[str] = {
- 40: def _iter_py_files(root: pathlib.Path) -> list[pathlib.Path]:
- 45: def test_core_components_exist() -> None:
- 60: def test_each_core_has_test_file() -> None:
- 82: def test_test_files_have_assertions() -> None:
- 103: def test_validate_function_exists() -> None:
- 129: def test_no_circular_imports_within_src() -> None:
- 137: def _imports_of(p: pathlib.Path) -> Set[str]:
- 173: def visit(n: str) -> bool:

## tests/test_core_runtime.py

- 16: import asyncio
- 17: import importlib
- 20: def test_runtime_import_and_validate() -> None:
- 31: def test_runtime_start_is_awaitable() -> None:
- 33: from src.core.runtime import Runtime
- 37: async def _run() -> None:

## tests/test_core_task_queue.py

- 16: import asyncio
- 17: import importlib
- 20: async def _producer_consumer_cycle() -> None:
- 22: import src.core.task_queue as tq
- 32: def test_task_queue_validate_and_async_cycle() -> None:
- 42: def test_task_queue_validate_executes() -> None:
- 44: from src.core.task_queue import validate
- 50: def test_task_queue_module() -> None:
- 53: assert hasattr(qmod, "TaskQueue")
- 54: assert callable(getattr(qmod, "validate", None))

## tests/test_core_workflow_engine.py

- 4: from src.core.workflow import engine
- 7: def test_engine_imports_and_validate() -> None:

## tests/test_cort.py

- 4: import pytest
- 6: from context_manager import ContextManager
- 7: from cort import ChainOfThought
- 11: async def test_cort_simple_branching() -> None:

## tests/test_coverage_config.py

- 16: import subprocess
- 17: import sys
- 18: import tomllib
- 19: from pathlib import Path
- 20: from typing import Any
- 22: PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"
- 25: def _load_pyproject_toml() -> dict[str, Any]:
- 35: def test_pyproject_has_coverage_run_section() -> None:
- 46: def test_coverage_run_has_source() -> None:
- 57: def test_pyproject_has_coverage_report_section() -> None:
- 68: def test_coverage_report_fail_under_is_present() -> None:
- 80: def test_coverage_report_fail_under_stage1_minimum() -> None:
- 93: def test_pytest_cov_importable() -> None:
- 109: def test_coverage_branch_enabled() -> None:

## tests/test_coverage_meta.py

- 17: source file under ``src/``.  The goal is *coverage completeness* rather
- 29: from __future__ import annotations
- 31: import pathlib
- 34: def test_force_coverage() -> None:
- 43: source = pyfile.read_text().splitlines()

## tests/test_crdt_bridge.py

- 20: from __future__ import annotations
- 22: from src.core import crdt_bridge
- 25: def test_crdt_bridge_merge_deterministic():

## tests/test_describe.py

- 4: from pathlib import Path
- 6: from src.importer import describe
- 9: def test_describe_file(tmp_path: Path) -> None:

## tests/test_downloader.py

- 4: from pathlib import Path
- 6: from src.importer import downloader
- 9: def test_download_repo(tmp_path: Path) -> None:

## tests/test_dryrun_lists_moves.py

- 6: import os
- 7: from pathlib import Path
- 9: from scripts import dryrun_move
- 12: def test_dryrun_writes_mapping(tmp_path: Path) -> None:

## tests/test_encrypted_memory.py

- 19: import pytest
- 22: from rust_core import MemoryBlockRegistry  # type: ignore[import]
- 28: pytestmark = pytest.mark.skipif(
- 35: def registry():
- 40: def test_create_block_returns_uuid_string(registry):
- 43: assert isinstance(block_id, str)
- 47: def test_put_returns_slab_index(registry):
- 54: def test_multiple_puts_increment_slab_index(registry):
- 65: def test_encrypt_decrypt_roundtrip(registry):
- 74: def test_roundtrip_binary_payload(registry):
- 82: def test_slab_count(registry):
- 92: def test_purge_wipes_slabs(registry):
- 101: def test_remove_block(registry):
- 111: def test_different_blocks_are_independent(registry):
- 121: def test_separate_registries_cannot_share_blocks():
- 132: def test_get_invalid_slab_index_raises(registry):
- 140: def test_empty_payload_roundtrip(registry):

## tests/test_enforce_branch.py

- 16: from __future__ import annotations
- 18: import sys
- 19: from pathlib import Path
- 20: from unittest.mock import patch
- 22: import pytest
- 27: import enforce_branch  # noqa: E402
- 35: def test_base_branches_allowed_no_staged(branch: str) -> None:
- 52: def test_project_branches_pass_naming(branch: str) -> None:
- 70: def test_bad_branch_names_blocked(branch: str) -> None:
- 83: _PRJ6_FILE = "docs/project/prj0000006/prj006-unified-transaction-manager.project.md"
- 84: _PRJ7_FILE = "docs/project/prj0000007/prj007-advanced_research.project.md"
- 87: def test_single_project_file_on_main_blocked() -> None:
- 96: def test_single_project_file_on_correct_branch_passes() -> None:
- 105: def test_single_project_file_on_wrong_branch_blocked() -> None:
- 114: def test_multi_project_governance_on_main_allowed() -> None:
- 123: def test_ci_file_on_main_allowed() -> None:
- 137: def test_extract_project_ids_empty() -> None:
- 142: def test_extract_project_ids_no_project_paths() -> None:
- 147: def test_extract_project_ids_single() -> None:
- 152: def test_extract_project_ids_multiple() -> None:
- 157: def test_extract_project_ids_windows_backslash() -> None:

## tests/test_exceptions.py

- 17: from src.core.audit.exceptions import AuditTrailError
- 18: from src.core.audit.exceptions import validate as audit_validate
- 19: from src.core.fuzzing.exceptions import FuzzingError
- 20: from src.core.n8nbridge.exceptions import N8nBridgeError
- 21: from src.core.replay.exceptions import ReplayError
- 22: from src.core.resilience.CircuitBreakerState import CircuitState
- 23: from src.core.resilience.exceptions import CircuitOpenError
- 24: from src.core.resilience.exceptions import validate as resilience_validate
- 25: from src.core.universal.exceptions import UniversalShellError
- 26: from src.core.universal.exceptions import validate as universal_validate
- 29: def test_exception_modules_are_importable() -> None:
- 31: assert issubclass(AuditTrailError, Exception)
- 32: assert issubclass(FuzzingError, Exception)
- 33: assert issubclass(N8nBridgeError, Exception)
- 34: assert issubclass(ReplayError, Exception)
- 35: assert issubclass(UniversalShellError, Exception)
- 38: def test_exception_module_validate_hooks() -> None:
- 45: def test_circuit_open_error_carries_provider_and_state() -> None:

## tests/test_file_watcher.py

- 15: import asyncio
- 16: import json
- 17: import os
- 18: import tempfile
- 19: import time
- 20: from unittest.mock import MagicMock, patch
- 22: import src.tools.FileWatcher as fw_module
- 23: from src.tools.FileWatcher import FileWatcher, _python_scan
- 30: def test_filewatcher_scan_uses_rust_when_available():
- 38: async def run():
- 57: def test_filewatcher_scan_falls_back_to_python():
- 75: def test_get_changes_returns_and_clears():
- 92: def test_invalid_root_returns_empty():
- 103: def test_start_stop_lifecycle():
- 106: async def run():

## tests/test_flm_chat_adapter.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass
- 20: from typing import Any, cast
- 22: import pytest
- 28: from src.core.providers.FlmChatAdapter import FlmChatAdapter
- 29: from src.core.providers.FlmProviderConfig import FlmProviderConfig
- 35: class _FakeFunction:
- 43: class _FakeToolCall:
- 52: class _FakeMessage:
- 60: class _FakeChoice:
- 67: class _FakeResponse:
- 73: class _FakeCompletions:
- 76: def __init__(self, responses: list[_FakeResponse]) -> None:
- 81: def create(self, **kwargs: object) -> _FakeResponse:
- 87: class _FakeClient:
- 90: def __init__(self, responses: list[_FakeResponse]) -> None:
- 96: def test_create_completion_uses_default_model() -> None:
- 108: def _client_factory(*, base_url: str, api_key: str) -> _FakeClient:
- 123: def test_run_until_terminal_returns_final_content() -> None:
- 135: def _client_factory(*, base_url: str, api_key: str) -> _FakeClient:
- 142: import asyncio

## tests/test_flm_dashboard.py

- 19: from __future__ import annotations
- 21: from fastapi.testclient import TestClient
- 23: from backend.app import app
- 25: _CLIENT = TestClient(app)
- 28: def test_flm_metrics_endpoint_returns_200() -> None:
- 34: def test_flm_response_has_samples_key() -> None:
- 41: def test_flm_samples_count_is_10() -> None:
- 48: def test_flm_sample_has_required_fields() -> None:
- 59: def test_flm_avg_tokens_is_numeric() -> None:
- 64: assert isinstance(avg, (int, float))

## tests/test_flm_provider_config.py

- 17: from __future__ import annotations
- 19: import pytest
- 21: from src.core.providers.FlmProviderConfig import FlmProviderConfig
- 24: def test_flm_provider_config_parses_required_and_optional_fields() -> None:
- 45: def test_flm_provider_config_applies_defaults() -> None:
- 61: def test_flm_provider_config_requires_required_fields(missing_key: str) -> None:
- 73: def test_flm_provider_config_rejects_invalid_timeout() -> None:
- 85: def test_flm_provider_config_rejects_invalid_path() -> None:
- 97: def test_flm_provider_config_from_env(monkeypatch: pytest.MonkeyPatch) -> None:

## tests/test_flm_provider_docs.py

- 17: from pathlib import Path
- 20: def test_flm_docs_use_fastflow_expansion() -> None:

## tests/test_flm_runtime_errors.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass
- 21: import pytest
- 25: from src.core.providers.FlmChatAdapter import FlmChatAdapter, FlmRuntimeError
- 26: from src.core.providers.FlmProviderConfig import FlmProviderConfig
- 32: class _FakeModel:
- 39: class _FakeModelsList:
- 45: class _FakeModels:
- 48: def __init__(self, mode: str = "ok") -> None:
- 52: def list(self) -> _FakeModelsList:
- 55: raise RuntimeError("connection refused")
- 59: class _FailingCompletions:
- 62: def create(self, **_kwargs: object) -> object:
- 64: raise RuntimeError("connection refused")
- 67: class _FailingClient:
- 70: def __init__(self) -> None:
- 72: from types import SimpleNamespace
- 79: class _ModelErrorClient:
- 82: def __init__(self) -> None:
- 84: from types import SimpleNamespace
- 91: def _make_config() -> FlmProviderConfig:
- 102: def test_create_completion_wraps_runtime_error_with_context() -> None:
- 113: def test_check_endpoint_available_wraps_errors() -> None:
- 124: def test_ensure_model_available_reports_missing_model() -> None:

## tests/test_flm_tool_loop.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass
- 20: from typing import Any, cast
- 22: import pytest
- 28: from src.core.providers.FlmChatAdapter import FlmChatAdapter, FlmRuntimeError
- 29: from src.core.providers.FlmProviderConfig import FlmProviderConfig
- 35: class _FakeFunction:
- 43: class _FakeToolCall:
- 52: class _FakeMessage:
- 60: class _FakeChoice:
- 67: class _FakeResponse:
- 73: class _FakeCompletions:
- 76: def __init__(self, responses: list[_FakeResponse]) -> None:
- 81: def create(self, **kwargs: object) -> _FakeResponse:
- 87: class _FakeClient:
- 90: def __init__(self, responses: list[_FakeResponse]) -> None:
- 96: def _make_config() -> FlmProviderConfig:
- 107: async def test_tool_loop_executes_and_returns_terminal_answer() -> None:
- 128: def _client_factory(*, base_url: str, api_key: str) -> _FakeClient:
- 144: assert any(message.get("role") == "assistant" for message in second_call_messages)
- 145: assert any(message.get("role") == "tool" for message in second_call_messages)
- 149: async def test_tool_loop_raises_when_iterations_exceeded() -> None:
- 169: def _client_factory(*, base_url: str, api_key: str) -> _FakeClient:

## tests/test_fuzzing_core.py

- 21: from __future__ import annotations
- 23: import importlib
- 24: from typing import Any
- 26: import pytest
- 29: def _require_symbol(module_name: str, symbol_name: str) -> Any:
- 60: def _build_case(
- 94: def test_test_01_policy_violation_exception_typing() -> None:
- 98: assert issubclass(policy_error, base_error)
- 101: def test_test_02_execution_and_config_exception_typing() -> None:
- 106: assert issubclass(config_error, base_error)
- 107: assert issubclass(execution_error, base_error)
- 110: def test_test_03_fuzz_case_immutability_contract() -> None:
- 117: def test_test_04_fuzz_case_replay_key_is_deterministic() -> None:
- 124: def test_test_05_fuzz_result_case_typing_and_state() -> None:
- 133: def test_test_06_fuzz_result_campaign_summary_counts() -> None:
- 147: def test_test_07_safety_policy_rejects_non_local_target() -> None:
- 163: def test_test_08_safety_policy_rejects_disallowed_operator() -> None:
- 179: def test_test_09_safety_policy_enforces_budget_limits() -> None:
- 195: def test_test_10_fuzz_corpus_normalizes_inputs_to_bytes() -> None:
- 203: def test_test_11_fuzz_corpus_deduplicates_repeated_payloads() -> None:
- 210: def test_test_12_fuzz_corpus_deterministic_indexed_selection() -> None:
- 219: def test_test_13_fuzz_mutator_registry_exposes_allowed_operators() -> None:
- 227: def test_test_14_fuzz_mutator_seeded_deterministic_mutation() -> None:
- 240: def test_test_15_fuzz_mutator_output_bytes_and_bounded() -> None:
- 245: assert isinstance(result, bytes)
- 249: def test_test_16_engine_schedules_bounded_case_count() -> None:
- 272: def test_test_17_engine_applies_policy_before_execution() -> None:
- 299: def test_test_18_engine_replay_stable_ordering_and_case_ids() -> None:
- 335: def test_test_19_fuzz_case_validation_rejects_invalid_fields(
- 367: def test_test_20_safety_policy_validate_rejects_invalid_config(
- 388: def test_test_21_safety_policy_payload_and_budget_guards() -> None:
- 411: def test_test_22_mutator_validation_and_unknown_operator_paths() -> None:
- 424: def test_test_23_mutator_empty_payload_branch_is_deterministic() -> None:
- 431: assert isinstance(left, bytes)
- 435: def test_test_24_corpus_validate_and_type_guards() -> None:
- 455: def test_test_25_case_result_validation_branches(
- 475: def test_test_26_campaign_result_validate_mismatch_branch() -> None:
- 493: def test_test_27_engine_schedule_zero_requested_returns_empty() -> None:

## tests/test_github_app.py

- 4: import pytest
- 9: from fastapi.testclient import TestClient
- 13: from src.github_app import app
- 15: client = TestClient(app)
- 18: def test_health_endpoint() -> None:
- 25: def test_webhook_receives() -> None:
- 31: def test_webhook_ping_event() -> None:
- 44: def test_webhook_push_event() -> None:
- 63: def test_webhook_pull_request_event() -> None:
- 82: def test_webhook_issues_event() -> None:
- 100: def test_webhook_unknown_event() -> None:
- 117: import hashlib  # noqa: E402
- 118: import hmac as _hmac  # noqa: E402
- 119: import json as _json  # noqa: E402
- 121: import src.github_app as _gha  # noqa: E402
- 124: def _sign(secret: str, body: bytes) -> str:
- 133: def test_verify_signature_helper_true() -> None:
- 141: def test_verify_signature_helper_false_wrong_hash() -> None:
- 146: def test_verify_signature_helper_false_missing_header() -> None:
- 151: def test_verify_signature_helper_false_empty_secret() -> None:
- 159: def test_webhook_valid_hmac(monkeypatch: pytest.MonkeyPatch) -> None:
- 173: def test_webhook_invalid_hmac(monkeypatch: pytest.MonkeyPatch) -> None:
- 186: def test_webhook_missing_signature_header(monkeypatch: pytest.MonkeyPatch) -> None:
- 199: def test_webhook_no_secret_configured(monkeypatch: pytest.MonkeyPatch) -> None:

## tests/test_import_config.py

- 4: import asyncio
- 5: from pathlib import Path
- 7: from src.importer import config
- 10: def test_parse_manifest(tmp_path: Path) -> None:
- 13: async def inner() -> None:

## tests/test_importer_config.py

- 17: from __future__ import annotations
- 19: import asyncio
- 20: from pathlib import Path
- 23: def test_parse_manifest(tmp_path: Path) -> None:
- 25: from src.importer.config import parse_manifest

## tests/test_importer_flow.py

- 4: import asyncio
- 5: from pathlib import Path
- 8: def test_importer_flow(tmp_path: Path) -> None:
- 11: from src.importer.compile import compile_architecture
- 12: from src.importer.config import parse_manifest
- 13: from src.importer.describe import describe_file
- 14: from src.importer.downloader import download_repo

## tests/test_innovation_tracker.py

- 4: from pathlib import Path
- 6: from src.roadmap import innovation
- 9: def test_record_experiment(tmp_path: Path) -> None:

## tests/test_lint_config.py

- 16: import subprocess
- 17: import sys
- 18: from pathlib import Path
- 20: PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"
- 21: MYPY_INI = Path(__file__).parent.parent / "mypy.ini"
- 24: def test_pyproject_has_ruff_section():
- 30: def test_ruff_line_length_120():
- 36: def test_ruff_selects_core_rules():
- 44: def test_mypy_section_present():
- 50: def test_mypy_ignore_missing_imports():
- 56: def test_ruff_binary_importable():
- 62: def test_ruff_check_exits_cleanly_on_good_file(tmp_path):

## tests/test_memory.py

- 4: import pytest
- 7: import rust_core
- 13: SharedMemory = rust_core.SharedMemory
- 16: def test_shared_memory_put_get() -> None:

## tests/test_memory_package.py

- 5: def test_memory_package_import() -> None:
- 7: import memory  # noqa: F401
- 9: assert hasattr(memory, "__name__")

## tests/test_message_model.py

- 4: import pytest
- 9: from src.swarm.message_model import validate_message
- 14: def test_validate_message_accepts_valid() -> None:
- 26: assert validate_message(valid)
- 29: def test_validate_message_rejects_missing_field() -> None:

## tests/test_metrics.py

- 4: from swarm.agent_registry import AgentRegistry
- 7: def test_metrics_contains_agent_count() -> None:

## tests/test_milestone_generator.py

- 4: import asyncio
- 5: from pathlib import Path
- 7: from src.roadmap import milestones
- 10: def test_generate_milestones(tmp_path: Path) -> None:

## tests/test_multimodal_package.py

- 16: from __future__ import annotations
- 18: import pytest
- 20: import multimodal
- 21: from multimodal.models import Modality, MultiModalData, MultiModalInputs
- 22: from multimodal.processor import (
- 34: def test_multimodal_package_import() -> None:
- 36: assert hasattr(multimodal, "__name__")
- 45: def test_modality_values() -> None:
- 59: def test_text_data_is_text() -> None:
- 67: def test_binary_data_is_binary() -> None:
- 74: def test_as_text_raises_for_non_utf8_binary() -> None:
- 81: def test_metadata_stored() -> None:
- 93: def test_embedding_stored() -> None:
- 104: def test_add_and_text_items() -> None:
- 113: def test_to_prompt_parts_with_context() -> None:
- 122: def test_to_prompt_parts_binary_placeholder() -> None:
- 130: def test_empty_inputs_no_context() -> None:
- 141: def test_text_processor() -> None:
- 150: def test_image_processor_bytes() -> None:
- 159: def test_image_processor_url_passthrough() -> None:
- 167: def test_audio_processor() -> None:
- 177: def test_multimodal_processor_full_pipeline() -> None:
- 191: def test_multimodal_processor_unsupported_modality() -> None:
- 200: def test_multimodal_processor_register_custom() -> None:
- 203: class UpperTextProcessor:
- 206: def process(self, data: MultiModalData) -> dict:
- 217: def test_validate_returns_true() -> None:

## tests/test_n8n_bridge.py

- 17: from __future__ import annotations
- 19: import io
- 20: from importlib import import_module
- 21: from typing import Any
- 22: from urllib.error import HTTPError
- 24: import pytest
- 27: def _load_symbol(module_name: str, symbol_name: str) -> Any:
- 41: def _base_env() -> dict[str, str]:
- 56: def _new_config() -> Any:
- 62: def _inbound_payload(event_id: str = "evt-1") -> dict[str, Any]:
- 76: def _outbound_event(correlation_id: str = "corr-1") -> dict[str, Any]:
- 90: def test_from_env_loads_required_fields_and_defaults() -> None:
- 98: def test_validate_rejects_invalid_base_url() -> None:
- 110: def test_validate_rejects_nonpositive_timeout_or_negative_retries(
- 126: def test_validate_rejects_negative_backoff_or_nonpositive_ttl(
- 138: def test_to_inbound_event_maps_valid_payload() -> None:
- 147: def test_to_inbound_event_rejects_missing_required_identifiers() -> None:
- 157: def test_to_inbound_event_preserves_correlation_id_from_headers() -> None:
- 165: def test_to_n8n_trigger_payload_maps_outbound_canonical_event() -> None:
- 171: assert isinstance(payload, dict)
- 174: def test_to_n8n_trigger_payload_rejects_missing_required_fields() -> None:
- 184: def test_to_inbound_event_raises_when_correlation_id_cannot_be_derived() -> None:
- 189: class _EmptyStringable:
- 192: def __str__(self) -> str:
- 202: def test_get_header_returns_none_for_falsey_or_non_matching_values() -> None:
- 210: async def test_post_json_includes_api_key_header_when_configured(monkeypatch: pytest.MonkeyPatch) -> None:
- 217: class _Response:
- 222: def read(self) -> bytes:
- 226: def getheaders(self) -> list[tuple[str, str]]:
- 230: def _fake_urlopen(request: Any, timeout: float) -> _Response:
- 245: async def test_post_json_applies_timeout_to_request_execution(monkeypatch: pytest.MonkeyPatch) -> None:
- 253: class _Response:
- 258: def read(self) -> bytes:
- 262: def getheaders(self) -> list[tuple[str, str]]:
- 266: def _fake_urlopen(_: Any, timeout: float) -> _Response:
- 278: async def test_post_json_retries_retryable_failures_up_to_max_attempts(
- 287: class _Response:
- 292: def read(self) -> bytes:
- 296: def getheaders(self) -> list[tuple[str, str]]:
- 300: def _fake_urlopen(_: Any, __: float) -> _Response:
- 304: raise OSError("temporary network issue")
- 314: async def test_post_json_does_not_retry_non_retryable_4xx(monkeypatch: pytest.MonkeyPatch) -> None:
- 321: def _fake_urlopen(_: Any, __: float) -> Any:
- 324: raise HTTPError("http://n8n", 400, "bad request", {}, None)
- 334: async def test_post_json_applies_extra_headers_and_skips_api_key_when_not_configured(
- 346: class _Response:
- 351: def read(self) -> bytes:
- 355: def getheaders(self) -> list[tuple[str, str]]:
- 359: def _fake_urlopen(request: Any, _: float) -> _Response:
- 378: async def test_post_json_raises_after_retryable_http_5xx_exhaustion(
- 391: def _fake_urlopen(_: Any, __: float) -> Any:
- 394: raise HTTPError("http://n8n", 503, "service unavailable", {}, io.BytesIO(b""))
- 404: async def test_post_json_raises_for_oserror_when_base_url_is_not_example_domain(
- 414: def _fake_urlopen(_: Any, __: float) -> Any:
- 416: raise OSError("network unreachable")
- 423: def test_parse_json_bytes_handles_empty_and_non_object_payloads() -> None:
- 431: async def test_sleep_backoff_returns_immediately_for_nonpositive_delay() -> None:
- 437: def test_http_client_module_validate_executes_monotonic_probe() -> None:
- 444: async def test_handle_inbound_event_rejects_duplicate_event_id_inside_ttl() -> None:
- 459: async def test_handle_inbound_event_accepts_same_event_id_after_ttl_expiry(
- 480: async def test_trigger_workflow_returns_success_result_on_2xx() -> None:
- 499: async def test_trigger_workflow_maps_timeout_to_typed_retryable_failure_result(
- 507: class _TimeoutHttpClient(http_client_cls):
- 510: async def post_json(
- 519: raise TimeoutError("timed out")
- 536: async def test_n8n_trigger_delegates_to_core_with_passthrough_args() -> None:
- 540: class _Core:
- 543: def __init__(self) -> None:
- 547: async def trigger_workflow(
- 575: class _Host(mixin_cls):
- 578: def __init__(self, core: _Core) -> None:
- 596: async def test_n8n_handle_callback_delegates_to_core_and_returns_result() -> None:
- 600: class _Core:
- 603: def __init__(self) -> None:
- 607: async def handle_inbound_event(
- 627: class _Host(mixin_cls):
- 630: def __init__(self, core: _Core) -> None:
- 645: async def test_contract_outbound_event_to_normalized_bridge_result(monkeypatch: pytest.MonkeyPatch) -> None:
- 651: class _Response:
- 656: def read(self) -> bytes:
- 660: def getheaders(self) -> list[tuple[str, str]]:
- 664: def _fake_urlopen(_: Any, __: float) -> _Response:
- 678: assert isinstance(result, dict)

## tests/test_pipeline_execution.py

- 19: from __future__ import annotations
- 21: from fastapi.testclient import TestClient
- 23: import backend.auth as _auth
- 24: from backend.app import app
- 29: client = TestClient(app)
- 31: PIPELINE_STAGES = [
- 45: def test_pipeline_run_endpoint_returns_pipeline_id():
- 53: def test_pipeline_status_endpoint_returns_pipeline_data():
- 66: def test_pipeline_status_404_for_unknown_id():
- 71: def test_pipeline_has_10_stages():
- 84: def test_pipeline_stages_have_status_and_log_fields():

## tests/test_plugin_marketplace.py

- 19: from __future__ import annotations
- 21: from fastapi.testclient import TestClient
- 23: from backend.app import app
- 25: client = TestClient(app)
- 28: def _get_plugins(client_ip: str):
- 33: def test_plugins_endpoint_returns_200():
- 39: def test_plugins_response_has_plugins_key():
- 46: def test_plugins_registry_is_non_empty():
- 53: def test_plugin_has_required_fields():
- 63: def test_plugins_without_auth_returns_200():

## tests/test_plugins.py

- 16: from __future__ import annotations
- 18: import pytest
- 20: from plugins.PluginManager import Plugin, PluginManager, PluginMetadata
- 27: class EchoPlugin(Plugin):
- 34: def name(self) -> str:
- 38: def metadata(self) -> PluginMetadata:
- 41: def setup(self) -> None:
- 44: def teardown(self) -> None:
- 47: def execute(self, **kwargs):
- 51: class AddPlugin(Plugin):
- 55: def name(self) -> str:
- 58: def execute(self, a: int = 0, b: int = 0):
- 67: def test_plugin_metadata_defaults() -> None:
- 76: def test_plugin_metadata_custom() -> None:
- 87: def test_plugin_default_metadata() -> None:
- 93: def test_add_plugin_default_metadata() -> None:
- 105: def test_register_and_has() -> None:
- 112: def test_register_calls_setup() -> None:
- 119: def test_register_replaces_plugin_calls_teardown() -> None:
- 127: def test_unregister_calls_teardown() -> None:
- 136: def test_unregister_unknown_raises() -> None:
- 147: def test_list_plugins_sorted() -> None:
- 155: def test_find_by_tag() -> None:
- 164: def test_find_by_tag_no_match() -> None:
- 170: def test_get_unknown_raises() -> None:
- 181: def test_execute_echo() -> None:
- 188: def test_execute_add() -> None:
- 194: def test_execute_unknown_raises() -> None:
- 205: def test_shutdown_calls_teardown_all() -> None:
- 215: def test_repr() -> None:

## tests/test_precommit.py

- 4: import pathlib
- 5: import subprocess
- 6: import sys
- 8: import pytest
- 11: def test_precommit_runs_on_empty_config(tmp_path: pathlib.Path) -> None:
- 26: def test_precommit_yaml_exists() -> None:

## tests/test_prioritization.py

- 5: def test_score_feature() -> None:
- 7: from roadmap import prioritization
- 11: assert isinstance(score, (int, float))

## tests/test_providers_flm.py

- 22: from __future__ import annotations
- 24: import asyncio
- 25: from typing import Any, cast
- 27: import pytest
- 32: from src.core.providers.FlmChatAdapter import FlmChatAdapter, FlmRuntimeError
- 33: from src.core.providers.FlmProviderConfig import FlmProviderConfig
- 38: class _DummyCompletion:
- 41: def __init__(self, content: str, tool_calls: list[object] \| None = None) -> None:
- 58: class ToolCall:
- 61: def __init__(self, id: int) -> None:
- 68: class _DummyModels:
- 71: def __init__(self, available: list[str] \| None = None, raise_exc: bool = False) -> None:
- 76: def list(self) -> object:
- 82: raise RuntimeError("list failed")
- 86: class _DummyChat:
- 89: class Completions:
- 93: def create(*, messages: object, model: str, max_tokens: int) -> object:
- 104: class _DummyClient:
- 107: def __init__(self, models_obj: object, chat_obj: object) -> None:
- 114: def base_config() -> FlmProviderConfig:
- 126: def test_check_endpoint_success(base_config: FlmProviderConfig) -> None:
- 136: def test_check_endpoint_failure(base_config: FlmProviderConfig) -> None:
- 146: def test_ensure_model_missing(base_config: FlmProviderConfig) -> None:
- 156: def test_create_completion_raises(base_config: FlmProviderConfig) -> None:
- 160: class BadChat:
- 163: class Completions:
- 167: def create(**kwargs: object) -> object:
- 169: raise RuntimeError("boom")
- 181: def test_run_until_terminal_tool_executor_missing(base_config: FlmProviderConfig) -> None:
- 188: class ToolCall:
- 191: def __init__(self, id: int) -> None:
- 197: class ChatWithTool:
- 200: class Completions:
- 204: def create(**kwargs: object) -> object:
- 219: def test_run_until_terminal_max_iterations(base_config: FlmProviderConfig) -> None:
- 226: class ChatLoop:
- 229: class Completions:
- 233: def create(**kwargs: object) -> object:
- 249: def noop(tool_call: object) -> str:
- 261: def test_dummy_assertion() -> None:

## tests/test_quality_yaml.py

- 16: import yaml
- 19: def test_ci_yaml_has_test_job() -> None:
- 27: def test_ci_yaml_test_job_has_install_step() -> None:
- 36: def test_ci_yaml_does_not_run_shared_precommit_profile() -> None:
- 47: def test_ci_yaml_triggers_on_push_and_pr() -> None:

## tests/test_rate_limiting.py

- 16: from __future__ import annotations
- 18: import asyncio
- 20: from fastapi.testclient import TestClient
- 23: def test_rate_limiter_module_imports():
- 25: from backend.rate_limiter import RateLimitMiddleware, TokenBucket
- 27: assert callable(RateLimitMiddleware)
- 28: assert callable(TokenBucket)
- 31: def test_probe_paths_exempt_from_rate_limit(monkeypatch):
- 33: import backend.rate_limiter as rl_mod
- 39: from fastapi import FastAPI
- 42: from backend.rate_limiter import RateLimitMiddleware
- 48: async def _health() -> dict[str, str]:
- 52: async def _livez() -> dict[str, str]:
- 56: async def _readyz() -> dict[str, str]:
- 66: def test_allowed_under_limit():
- 68: from fastapi import FastAPI
- 70: from backend.rate_limiter import RateLimitMiddleware
- 76: async def _test() -> dict[str, bool]:
- 84: def test_rate_limit_triggers_429():
- 86: from fastapi import FastAPI
- 88: from backend.rate_limiter import RateLimitMiddleware
- 94: async def _data() -> dict[str, bool]:
- 107: def test_retry_after_header_present():
- 109: from fastapi import FastAPI
- 111: from backend.rate_limiter import RateLimitMiddleware
- 117: async def _limited() -> dict[str, bool]:
- 128: def test_token_bucket_allows_then_blocks():
- 130: from backend.rate_limiter import TokenBucket
- 134: async def _run() -> None:

## tests/test_registry_api.py

- 4: from typing import cast
- 6: import pytest
- 10: from fastapi import FastAPI
- 11: from fastapi.testclient import TestClient
- 15: from src.swarm.agent_registry import AgentRegistry
- 18: app = FastAPI()
- 19: registry = AgentRegistry()
- 23: def register_agent(info: dict[str, object]) -> dict[str, object]:
- 35: def heartbeat(agent_id: str) -> dict[str, str]:
- 46: def get_agent(agent_id: str) -> dict[str, object]:
- 55: def list_agents() -> list[dict[str, object]]:
- 63: client = TestClient(app)
- 66: def test_registry_http_endpoints() -> None:
- 73: assert isinstance(aid, str)
- 90: assert any(agent["agent_id"] == aid for agent in agents)

## tests/test_repo_layout_scaffold.py

- 16: from pathlib import Path
- 18: from scripts.scaffold_new_layout import create_dirs
- 21: def test_new_layout_dirs_exist(tmp_path: Path) -> None:

## tests/test_research_packages.py

- 5: def test_all_research_packages_exist() -> None:

## tests/test_responsive_nebula.py

- 19: from pathlib import Path
- 21: WEB_DIR = Path(__file__).parent.parent / "web"
- 22: STYLES_DIR = WEB_DIR / "styles"
- 25: def _find_responsive_css() -> Path \| None:
- 33: def test_web_contains_css_with_responsive_media_queries():
- 43: def test_responsive_css_has_mobile_max_width_768():
- 52: def test_responsive_css_has_tablet_breakpoint():
- 61: def test_app_tsx_imports_or_references_responsive_styles():
- 79: def test_responsive_css_has_at_least_3_rules_for_window_or_taskbar():

## tests/test_rl_package.py

- 4: from __future__ import annotations
- 6: import importlib
- 9: def test_rl_package_exports_slice1_api() -> None:
- 14: assert hasattr(module, "discounted_return")
- 15: assert hasattr(module, "validate")

## tests/test_roadmap_cli.py

- 4: from pathlib import Path
- 6: from src.roadmap import cli, vision
- 9: def test_roadmap_cli(tmp_path: Path) -> None:
- 18: def test_roadmap_cli_main_generate(tmp_path: Path) -> None:
- 26: def test_roadmap_cli_main_vision(capsys) -> None:
- 34: def test_roadmap_cli_main_milestones(tmp_path: Path) -> None:
- 44: def test_vision_template_contains_pyagent() -> None:

## tests/test_runtime.py

- 17: from __future__ import annotations
- 19: import asyncio
- 22: def test_runtime_validate_and_start() -> None:
- 24: from src.core import runtime
- 31: assert callable(getattr(r, "start", None))

## tests/test_rust_core.py

- 7: import re
- 8: import sys
- 9: import time
- 10: from collections import defaultdict
- 11: from pathlib import Path
- 12: from re import Pattern
- 13: from typing import Any
- 15: import pytest
- 18: import rust_core
- 23: VERBOSE = True
- 24: SHOW_ALL_FUNCTIONS = False  # Set to True to see all functions
- 25: SCAN_SOURCE = True  # Scan rust_core/src/ for function signatures
- 26: TEST_ALL_FUNCTIONS = True  # Attempt to test all discovered functions
- 27: MAX_FUNCTIONS_TO_TEST = 100  # Limit tests for performance
- 30: def print_header(title: str, char: str = "=") -> None:
- 38: def print_section(title: str) -> None:
- 45: def _extract_functions_from_file(filepath: str, fn_pattern: Pattern[str]) -> list[dict[str, Any]]:
- 76: def scan_rust_files(rust_src_path: Path) -> dict[str, list[dict[str, Any]]]:
- 94: def generate_test_args(function_name: str, arg_count: int = 1) -> list[tuple[Any, ...]]:
- 146: def safe_call_function(func_obj: object, args: tuple[Any, ...]) -> tuple[bool, str, object \| None]:
- 205: all_exports = dir(rust_core)
- 206: public_exports = [x for x in all_exports if not x.startswith("_")]
- 207: private_exports = [x for x in all_exports if x.startswith("_")]
- 214: class_exports: list[str] = []
- 215: function_exports: list[str] = []
- 216: special_exports: list[str] = []
- 232: _denom = max(1, len(public_exports))
- 259: prefixes: dict[str, list[str]] = defaultdict(list)
- 273: sorted_prefixes: list[tuple[str, list[str]]] = sorted(prefixes.items(), key=lambda x: len(x[1]), reverse=True)
- 291: test_results: dict[str, Any] = {
- 300: test_functions: list[str] = sorted(function_exports)
- 304: total_to_test = len(test_functions)
- 361: key_classes = [
- 371: class_results = {"found": 0, "missing": 0}
- 391: TOTAL_FUNCTIONS_TESTED = test_results["pass"] + test_results["fail"]
- 392: pass_rate = 100 * test_results["pass"] / max(1, TOTAL_FUNCTIONS_TESTED)
- 427: health_checks = [

## tests/test_rust_crdt_merge.py

- 21: from __future__ import annotations
- 23: import json
- 24: import subprocess
- 25: import sys
- 26: from pathlib import Path
- 29: def test_rust_crdt_merge_binary_merges_json(tmp_path):

## tests/test_rust_p2p_binary.py

- 20: from __future__ import annotations
- 22: import os
- 23: import shutil
- 24: import subprocess
- 25: import sys
- 26: import urllib.request
- 27: import zipfile
- 28: from pathlib import Path
- 30: import pytest
- 36: def _ensure_protoc_available(tmp_path: Path) -> str:
- 75: def test_rust_p2p_binary_runs_and_reports_peer_id(tmp_path):

## tests/test_sandbox.py

- 22: from __future__ import annotations
- 24: import os
- 25: import uuid
- 26: from pathlib import Path
- 28: import pytest
- 36: from src.core.sandbox import (  # type: ignore[import]  # noqa: E402
- 48: def test_sandbox_config_from_strings_valid() -> None:
- 61: def test_sandbox_config_from_strings_auto_uuid() -> None:
- 72: def test_validate_path_in_scope_passes(tmp_path: Path) -> None:
- 83: def test_validate_path_out_of_scope_raises(tmp_path: Path) -> None:
- 98: def test_validate_path_exact_boundary_passes(tmp_path: Path) -> None:
- 109: def test_sandbox_violation_error_attributes() -> None:
- 119: assert isinstance(err, RuntimeError)
- 122: def test_validate_host_allowed_passes(tmp_path: Path) -> None:
- 128: class _Agent(SandboxMixin):
- 131: def __init__(self) -> None:
- 140: def test_validate_host_forbidden_raises(tmp_path: Path) -> None:
- 146: class _Agent(SandboxMixin):
- 149: def __init__(self) -> None:
- 159: def test_validate_host_allow_all_hosts_bypasses(tmp_path: Path) -> None:
- 165: class _Agent(SandboxMixin):
- 168: def __init__(self) -> None:
- 184: async def test_sandbox_tx_write_inside_allowed_path(tmp_path: Path) -> None:
- 199: async def test_sandbox_tx_write_outside_allowed_path_raises(tmp_path: Path) -> None:
- 216: async def test_sandbox_tx_delete_outside_allowed_path_raises(tmp_path: Path) -> None:
- 231: async def test_sandbox_tx_mkdir_outside_allowed_path_raises(tmp_path: Path) -> None:
- 245: def test_sandbox_tx_commit_legacy_forbidden_target_raises(tmp_path: Path) -> None:
- 264: async def test_sandbox_mixin_agent_writes_to_allowed_dir(tmp_path: Path) -> None:
- 270: class _Agent(SandboxMixin):
- 273: def __init__(self, allowed_dir: Path) -> None:
- 287: async def test_sandbox_tx_write_op_not_queued_on_violation(tmp_path: Path) -> None:
- 308: def test_validate_path_symlink_escape_raises(tmp_path: Path) -> None:
- 331: def test_validate_path_traversal_string_raises(tmp_path: Path) -> None:
- 348: async def test_sandbox_config_empty_allowed_paths_rejects_all(tmp_path: Path) -> None:

## tests/test_security_bridge.py

- 17: from __future__ import annotations
- 19: from pathlib import Path
- 21: from src.core import security_bridge
- 24: def test_security_bridge_encrypt_decrypt(tmp_path: Path):
- 37: def test_security_bridge_rotate_key_changes_key(tmp_path: Path):

## tests/test_security_rotation.py

- 17: from __future__ import annotations
- 19: import subprocess
- 20: from pathlib import Path
- 22: import pytest
- 24: SECURITY_BIN = Path("rust_core/security/target/release/security")
- 28: pytestmark = pytest.mark.skipif(
- 34: def _run(args: list[str], **kwargs) -> subprocess.CompletedProcess:
- 38: def test_security_binary_keygen(tmp_path: Path) -> None:
- 46: def test_security_binary_encrypt_decrypt_roundtrip(tmp_path: Path) -> None:
- 60: def test_security_binary_rotate_key_changes_file(tmp_path: Path) -> None:
- 72: def test_security_binary_decrypt_with_rotated_key_fails(tmp_path: Path) -> None:

## tests/test_shadow_replay.py

- 22: from __future__ import annotations
- 24: import hashlib
- 25: import importlib
- 26: import json
- 27: from dataclasses import dataclass
- 28: from typing import Any
- 30: import pytest
- 33: def _require_symbol(module_name: str, symbol_name: str) -> Any:
- 64: def _replay_envelope_payload(
- 103: def _build_envelope(*, sequence_no: int, session_id: str = "s-store", logical_clock: int \| None = None) -> Any:
- 125: class _TxRecorder:
- 137: async def commit(self) -> None:
- 141: async def rollback(self) -> None:
- 146: def _make_shadow_core_and_txs() -> tuple[Any, list[_TxRecorder]]:
- 156: def _factory() -> _TxRecorder:
- 173: async def test_rt_01_envelope_roundtrip_preserves_payload() -> None:
- 183: async def test_rt_02_envelope_rejects_missing_required_fields() -> None:
- 194: async def test_rt_03_envelope_rejects_non_monotonic_logical_clock() -> None:
- 204: async def test_rt_04_envelope_checksum_mismatch_raises_schema_error() -> None:
- 215: async def test_rt_05_store_append_and_load_return_ordered_envelopes(tmp_path: Any) -> None:
- 230: async def test_rt_06_store_rejects_duplicate_sequence(tmp_path: Any) -> None:
- 245: async def test_rt_07_store_load_range_is_deterministic_subset(tmp_path: Any) -> None:
- 258: async def test_rt_08_store_corruption_raises_typed_error(tmp_path: Any) -> None:
- 276: async def test_rt_09_store_delete_session_removes_events(tmp_path: Any) -> None:
- 290: async def test_rt_10_shadow_core_executes_read_only_envelope_safely() -> None:
- 302: async def test_rt_11_shadow_core_blocks_process_side_effects() -> None:
- 317: async def test_rt_12_shadow_core_rolls_back_transactions_on_exception(
- 324: async def _boom(_envelope: Any) -> Any:
- 326: raise RuntimeError("forced-shadow-failure")
- 332: assert any(tx.rolled_back for tx in txs)
- 336: async def test_rt_13_orchestrator_fails_on_sequence_gap() -> None:
- 341: class _Store:
- 344: async def load_session(self, _session_id: str) -> list[Any]:
- 351: class _ShadowCore:
- 354: async def execute_envelope(self, _envelope: Any, *, deterministic_seed: int \| None = None) -> Any:
- 356: raise AssertionError("execute_envelope should not run when sequence validation fails")
- 365: async def test_rt_14_orchestrator_halts_at_first_divergence() -> None:
- 369: class _Store:
- 372: async def load_session(self, _session_id: str) -> list[Any]:
- 380: class _Result:
- 383: def __init__(self, *, success: bool) -> None:
- 387: class _ShadowCore:
- 390: def __init__(self) -> None:
- 394: async def execute_envelope(self, envelope: Any, *, deterministic_seed: int \| None = None) -> _Result:
- 407: async def test_rt_15_orchestrator_collects_all_divergences_when_configured() -> None:
- 411: class _Store:
- 414: async def load_session(self, _session_id: str) -> list[Any]:
- 423: class _Result:
- 426: def __init__(self, *, success: bool, reason: str = "") -> None:
- 431: class _ShadowCore:
- 434: def __init__(self) -> None:
- 438: async def execute_envelope(self, envelope: Any, *, deterministic_seed: int \| None = None) -> _Result:
- 456: async def test_rt_16_mixin_emission_includes_context_lineage_fields() -> None:
- 460: class _Host(replay_mixin_cls):
- 463: def __init__(self) -> None:
- 487: async def test_rt_17_mixin_replay_delegates_to_orchestrator() -> None:
- 491: class _Orchestrator:
- 494: def __init__(self) -> None:
- 498: async def replay_session(
- 509: class _Host(replay_mixin_cls):
- 512: def __init__(self) -> None:
- 525: async def test_rt_18_end_to_end_replay_produces_deterministic_hash() -> None:
- 529: class _Store:
- 532: async def load_session(self, _session_id: str) -> list[Any]:
- 539: class _Orchestrator:
- 542: async def replay_session(
- 562: class _Host(replay_mixin_cls):
- 565: def __init__(self) -> None:
- 573: assert isinstance(result["output_hash"], str)
- 578: async def test_rt_19_envelope_rejects_invalid_schema_and_payload_types() -> None:
- 605: async def test_rt_20_envelope_rejects_non_positive_sequence_and_logical_clock() -> None:
- 620: async def test_rt_21_envelope_allows_sha256_checksum_mismatch_for_side_effect_envelopes() -> None:
- 633: async def test_rt_22_envelope_sha256_shape_helper_rejects_non_hex() -> None:
- 640: async def test_rt_23_store_handles_invalid_bounds_and_missing_delete(tmp_path: Any) -> None:
- 653: async def test_rt_24_store_validate_rejects_file_root(tmp_path: Any) -> None:
- 667: async def test_rt_25_mixin_validate_and_missing_orchestrator_errors() -> None:
- 672: class _BadOrchestrator:
- 675: class _HostBad(replay_mixin_cls):
- 678: def __init__(self) -> None:
- 686: class _HostMissing(replay_mixin_cls):
- 689: def __init__(self) -> None:
- 695: await _HostMissing().replay_session("s-missing-orchestrator")
- 699: async def test_rt_26_mixin_emission_appends_to_store_when_available() -> None:
- 703: class _Store:
- 706: def __init__(self) -> None:
- 710: async def append_envelope(self, envelope: Any) -> None:
- 714: class _Host(replay_mixin_cls):
- 717: def __init__(self) -> None:
- 737: async def test_rt_27_orchestrator_empty_stream_and_dependency_validation() -> None:
- 742: class _NoStoreMethod:
- 745: class _NoShadowMethod:
- 762: class _Store:
- 765: async def load_session(self, _session_id: str) -> list[Any]:
- 769: class _ShadowCore:
- 772: async def execute_envelope(self, _envelope: Any, *, deterministic_seed: int \| None = None) -> Any:
- 783: async def test_rt_28_shadow_core_network_toggle_and_policy_rollback(monkeypatch: pytest.MonkeyPatch) -> None:
- 801: async def _policy_error(_envelope: Any) -> dict[str, Any]:
- 803: raise shadow_policy_violation_cls("blocked")
- 809: assert all(tx.rolled_back for tx in txs_rollback)
- 823: async def test_rt_29_shadow_core_rollback_ignores_transactions_without_rollback() -> None:
- 827: class _NoRollback:

## tests/test_shared_memory_python.py

- 4: import pytest
- 7: import rust_core
- 13: SharedMemory = rust_core.SharedMemory  # type: ignore[attr-defined]
- 16: def test_shared_memory_python_basics() -> None:
- 28: def test_verify_hmac_wrong_tag() -> None:

## tests/test_speculation_package.py

- 4: from __future__ import annotations
- 6: import importlib
- 9: def test_speculation_package_exports_slice1_api() -> None:
- 14: assert hasattr(module, "select_candidate")
- 15: assert hasattr(module, "validate")

## tests/test_structured_logging.py

- 16: from __future__ import annotations
- 18: import logging
- 20: from pythonjsonlogger.json import JsonFormatter
- 23: def test_logging_config_module_imports():
- 25: from backend.logging_config import get_logger, setup_logging  # noqa: F401
- 27: assert callable(setup_logging)
- 28: assert callable(get_logger)
- 31: def test_setup_logging_returns_logger():
- 33: from backend.logging_config import setup_logging
- 36: assert isinstance(result, logging.Logger)
- 39: def test_get_logger_returns_named_logger():
- 41: from backend.logging_config import get_logger
- 44: assert isinstance(lg, logging.Logger)
- 48: def test_logger_has_json_handler():
- 50: from backend.logging_config import setup_logging
- 59: def test_correlation_id_middleware_adds_header():
- 61: from fastapi.testclient import TestClient
- 63: from backend.app import app

## tests/test_swarm_agent_registry.py

- 16: import time
- 18: from swarm.agent_registry import AgentRegistry
- 21: def test_register_returns_id():
- 27: def test_register_multiple_agents():
- 34: def test_get_agent():
- 42: def test_heartbeat_updates_timestamp():
- 52: def test_is_healthy_freshly_registered():
- 58: def test_metrics_output():

## tests/test_swarm_message.py

- 16: import pytest
- 18: from swarm.message_model import Message, validate_message
- 21: def _valid():
- 34: def test_validate_message_accepts_valid():
- 38: def test_validate_message_rejects_missing_field():
- 39: from pydantic import ValidationError
- 47: def test_message_model_fields():

## tests/test_swarm_node.py

- 16: import pytest
- 18: from swarm.memory_store import SwarmMemory
- 19: from swarm.swarm_node import SwarmNode
- 23: async def test_shared_set_get():
- 30: async def test_shared_get_default():
- 36: async def test_local_set_get():
- 43: async def test_local_isolated_per_node():
- 52: async def test_shared_keys():
- 60: def test_memory_metrics():
- 67: async def test_swarm_node_ping():
- 76: async def test_swarm_node_pong_on_ping():
- 86: async def test_swarm_node_process_one():

## tests/test_swarm_task_scheduler.py

- 16: import pytest
- 18: from swarm.task_scheduler import TaskScheduler
- 22: async def test_enqueue_and_dequeue():
- 31: async def test_priority_ordering():
- 40: async def test_dequeue_empty_raises():
- 46: def test_modify_priority():

## tests/test_system_integration.py

- 4: from pathlib import Path
- 6: import pytest
- 10: async def test_system_integration(tmp_path: Path) -> None:
- 12: from context_manager import ContextManager
- 13: from skills_registry import SkillsRegistry

## tests/test_task.py

- 4: import pytest
- 6: from src.core.workflow.task import Task, TaskState
- 10: async def test_task_initial_state_and_metadata() -> None:
- 20: async def test_task_state_transitions() -> None:

## tests/test_task_queue.py

- 4: import pytest
- 6: from src.core.workflow.queue import TaskQueue
- 7: from src.core.workflow.task import Task
- 11: async def test_enqueue_dequeue() -> None:

## tests/test_task_scheduler.py

- 4: import pytest
- 6: from src.swarm.task_scheduler import TaskScheduler
- 10: async def test_enqueue_dequeue_priority() -> None:
- 21: def test_modify_priority() -> None:

## tests/test_task_state.py

- 4: import pytest
- 6: from src.core.workflow.task import TaskState
- 10: async def test_taskstate_contains_expected_states() -> None:

## tests/test_theme_system.py

- 16: from pathlib import Path
- 18: REPO_ROOT = Path(__file__).parent.parent
- 19: THEMES_CSS = REPO_ROOT / "web" / "styles" / "themes.css"
- 20: USE_THEME_HOOK = REPO_ROOT / "web" / "hooks" / "useTheme.ts"
- 21: THEME_SELECTOR = REPO_ROOT / "web" / "components" / "ThemeSelector.tsx"
- 24: def test_themes_css_exists():
- 29: def test_themes_css_has_three_themes():
- 37: def test_themes_css_uses_css_variables():
- 43: def test_use_theme_hook_exists():
- 48: def test_theme_selector_component_exists():

## tests/test_tools_sanity.py

- 21: from __future__ import annotations
- 23: import pkgutil
- 24: import runpy
- 25: import sys
- 26: from pathlib import Path
- 28: import pytest
- 34: def test_tools_main_blocks() -> None:

## tests/test_tracing.py

- 16: from __future__ import annotations
- 18: from opentelemetry.sdk.trace import TracerProvider
- 19: from opentelemetry.sdk.trace.export import SimpleSpanProcessor
- 20: from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
- 22: from backend.tracing import _TRACER_NAME, setup_tracing
- 25: def test_setup_tracing_returns_tracer():
- 31: def test_span_name_recorded():
- 43: def test_tracer_instrumentation_scope():
- 54: def test_tracing_module_singleton_exists():
- 55: from backend import tracing
- 57: assert hasattr(tracing, "tracer")
- 58: assert hasattr(tracing, "setup_tracing")
- 59: assert hasattr(tracing, "_TRACER_NAME")
- 62: def test_tracer_name_constant():

## tests/test_transaction_managers.py

- 17: from __future__ import annotations
- 19: import sys
- 20: from pathlib import Path
- 22: import pytest
- 24: from src.core.ContextTransactionManager import ContextTransaction, RecursionGuardError
- 25: from src.core.ProcessTransactionManager import ProcessTransaction
- 26: from src.core.StorageTransactionManager import StorageTransaction
- 33: class TestStorageTransaction:
- 36: def test_commit_writes_file(self, tmp_path: Path) -> None:
- 44: def test_rollback_on_exception_leaves_target_untouched(self, tmp_path: Path) -> None:
- 51: raise ValueError("abort")
- 54: def test_autocommit_when_no_exception(self, tmp_path: Path) -> None:
- 61: def test_stage_replaces_previous_stage(self, tmp_path: Path) -> None:
- 71: async def test_async_context_manager_commits(self, tmp_path: Path) -> None:
- 85: class TestProcessTransaction:
- 88: def test_start_and_wait_success(self) -> None:
- 97: def test_rollback_terminates_process(self) -> None:
- 108: def test_exception_triggers_rollback(self) -> None:
- 116: raise RuntimeError("forced abort")
- 121: async def test_async_start_and_wait(self) -> None:
- 137: class TestContextTransaction:
- 140: def test_basic_enter_exit(self) -> None:
- 146: def test_recursive_entry_raises(self) -> None:
- 153: def test_different_contexts_nest_fine(self) -> None:
- 161: def test_empty_context_id_raises(self) -> None:
- 167: async def test_async_context_manager(self) -> None:

## tests/test_transport_identity.py

- 16: import importlib.util
- 17: import os
- 18: import sys
- 20: import pytest
- 23: import rust_core as rc  # type: ignore
- 55: def test_generate_node_identity_returns_32_bytes():
- 62: def test_node_id_is_deterministic_for_loaded_identity(tmp_path):
- 72: def test_sign_and_verify_roundtrip():
- 81: def test_verify_fails_for_tampered_message():
- 89: def test_loopback_send_recv():
- 98: def test_loopback_roundtrip_integrity():
- 107: def test_noise_handshake_produces_encrypted_channel():
- 120: def test_noise_handshake_rejects_unknown_peer():

## tests/test_transport_package.py

- 5: def test_transport_package_import() -> None:
- 8: import transport  # noqa: F401
- 10: assert hasattr(transport, "__name__")

## tests/test_transport_t1.py

- 19: import pytest
- 21: _TRANSPORT_AVAILABLE = False
- 23: import rust_core as _rc
- 26: from transport import LoopbackChannel, NodeIdentity
- 32: pytestmark = pytest.mark.skipif(
- 41: def test_node_identity_public_key_is_32_bytes():
- 44: assert isinstance(identity.public_key, bytes)
- 48: def test_node_identity_sign_returns_64_bytes():
- 52: assert isinstance(sig, bytes)
- 56: def test_node_identity_verify_valid_signature():
- 64: def test_node_identity_verify_rejects_tampered_message():
- 71: def test_node_identity_repr():
- 81: def test_loopback_channel_send_recv():
- 89: def test_loopback_channel_binary_payload():
- 98: def test_loopback_channel_bidirectional():
- 106: def test_loopback_channel_empty_payload():
- 114: def test_loopback_channel_multiple_messages():

## tests/test_transport_utm_policy.py

- 16: import pytest
- 19: import rust_core
- 26: from rust_core import (  # noqa: E402
- 37: def test_utm_transport_port_constants():
- 45: def test_utm_transport_policy_constants():

## tests/test_unified_transaction_manager.py

- 17: from __future__ import annotations
- 19: import importlib
- 20: from types import ModuleType
- 23: def _load_unified_module() -> ModuleType:
- 28: def test_unified_manager_class_contract_exists() -> None:
- 39: def test_transaction_envelope_and_result_contracts_exist() -> None:
- 50: def test_rollback_called_in_reverse_order_on_failure() -> None:
- 74: def test_operation_error_metadata_is_exposed() -> None:
- 90: raise AssertionError("execute was expected to raise on failing operation")

## tests/test_universal_shell.py

- 17: from __future__ import annotations
- 19: import asyncio
- 20: import importlib
- 21: from dataclasses import dataclass
- 22: from types import SimpleNamespace
- 23: from typing import Any
- 25: import pytest
- 28: def _import_or_fail(module_name: str) -> Any:
- 50: def test_public_exports_include_stable_symbols() -> None:
- 79: def test_exception_hierarchy_matches_design_contract() -> None:
- 98: def test_task_envelope_and_dispatch_result_have_required_fields() -> None:
- 123: def test_router_classify_rejects_non_envelope() -> None:
- 133: def test_router_allowlist_normalization_and_validate() -> None:
- 152: class _ValidHandler:
- 155: async def execute(self, envelope: Any) -> dict[str, Any]:
- 169: class _MissingExecuteHandler:
- 173: class _SyncExecuteHandler:
- 176: def execute(self, envelope: Any) -> dict[str, Any]:
- 190: def test_registry_validation_and_lifecycle_paths() -> None:
- 211: assert hasattr(handler, "execute")
- 228: class _RouterDouble:
- 235: def classify(self, envelope: Any) -> Any:
- 253: class _RouterBrokenDecision:
- 256: def classify(self, envelope: Any) -> Any:
- 271: class _CoreHandlerDouble:
- 277: async def execute(self, envelope: Any) -> dict[str, Any]:
- 298: raise AssertionError(f"unexpected mode: {self.mode}")
- 302: class _CoreRegistryDouble:
- 308: def resolve(self, intent: str) -> _CoreHandlerDouble:
- 327: def _make_envelope() -> Any:
- 344: async def test_shell_constructor_and_decision_contract_errors() -> None:
- 349: async def _legacy(envelope: Any) -> dict[str, Any]:
- 382: async def test_shell_rejects_invalid_route_and_empty_intent() -> None:
- 387: async def _legacy(envelope: Any) -> dict[str, Any]:
- 422: async def test_shell_core_success_legacy_path_and_fallback_paths() -> None:
- 428: async def _legacy(envelope: Any) -> dict[str, Any]:
- 497: async def test_shell_legacy_error_mapping_and_passthrough() -> None:
- 502: async def _legacy_generic_failure(envelope: Any) -> dict[str, Any]:
- 513: raise RuntimeError("legacy exploded")
- 525: async def _legacy_contract_failure(envelope: Any) -> dict[str, Any]:
- 550: async def test_shell_rejects_invalid_envelope_type() -> None:
- 555: async def _legacy(envelope: Any) -> dict[str, Any]:
- 579: def test_validate_helpers_for_shell_package_and_exceptions() -> None:

## tests/test_vision_template.py

- 4: from pathlib import Path
- 6: from roadmap import vision
- 9: def test_vision_template_exists(tmp_path: Path) -> None:

## tests/test_watchdog.py

- 15: import asyncio
- 17: from fastapi.testclient import TestClient
- 19: from backend.app import app
- 20: from backend.watchdog import AgentWatchdog
- 27: def test_run_success():
- 28: async def good_coro():
- 43: def test_run_timeout_increments_retry():
- 44: async def slow_coro():
- 59: def test_run_dead_letter_after_retries():
- 60: async def slow_coro():
- 66: async def drive():
- 85: def test_status_returns_correct_shape():
- 101: def test_dlq_contains_correct_entry():
- 102: async def slow_coro():
- 107: async def drive():
- 118: assert isinstance(entry["timestamp"], float)
- 126: def test_watchdog_status_endpoint():

## tests/test_workflow_engine.py

- 4: import pytest
- 6: from src.core.workflow.engine import WorkflowEngine
- 7: from src.core.workflow.queue import TaskQueue
- 8: from src.core.workflow.task import Task, TaskState
- 12: async def test_engine_process_changes_state() -> None:

## tests/test_ws_crypto.py

- 16: from __future__ import annotations
- 18: import pytest
- 20: from backend.ws_crypto import (
- 28: def test_generate_keypair_returns_32_byte_keys() -> None:
- 37: def test_ecdh_shared_secret_symmetric() -> None:
- 49: def test_encrypt_decrypt_roundtrip() -> None:
- 62: def test_decrypt_with_wrong_key_raises() -> None:
- 64: from cryptography.exceptions import InvalidTag
- 79: def test_nonce_prepended_to_ciphertext() -> None:
- 91: from cryptography.hazmat.primitives.ciphers.aead import AESGCM

## tests/tools/test_capabilities_modules.py

- 4: import importlib.util
- 5: import sys
- 6: from pathlib import Path
- 8: MODULES = [
- 23: def test_modules_importable(tmp_path: Path) -> None:
- 26: from scripts.setup_structure import create_core_structure
- 38: assert callable(module.detect_misconfig)
- 41: assert callable(module.main)

## tests/tools/test_common_helpers.py

- 4: from pathlib import Path
- 7: def test_common_helpers_importable(tmp_path: Path) -> None:
- 10: from scripts.setup_structure import create_core_structure
- 13: import importlib.util
- 14: import sys
- 21: assert hasattr(module, "load_config")
- 22: assert callable(module.load_config)

## tests/tools/test_dependency_audit.py

- 4: from pathlib import Path
- 7: def test_dependency_audit_returns_list(tmp_path: Path) -> None:
- 10: from scripts.setup_structure import create_core_structure
- 14: import importlib.util
- 15: import sys
- 22: assert hasattr(module, "check_dependencies")
- 24: assert isinstance(result, list)

## tests/tools/test_email.py

- 4: from tools.pm import email
- 7: def test_render_status_email() -> None:
- 10: import asyncio

## tests/tools/test_implementation_helpers.py

- 16: import json
- 17: from pathlib import Path
- 19: import pytest
- 21: from src.tools.common import (
- 30: def test_load_config_json(tmp_path: Path) -> None:
- 38: def test_load_config_toml(tmp_path: Path) -> None:
- 46: import pytest
- 51: def test_ensure_dir_creates_nested(tmp_path: Path) -> None:
- 59: def test_ensure_dir_idempotent(tmp_path: Path) -> None:
- 66: async def test_retry_succeeds_on_first_attempt() -> None:
- 70: def fn():
- 80: async def test_retry_retries_on_failure() -> None:
- 84: def fn():
- 90: raise ValueError("not yet")
- 99: async def test_retry_raises_after_max_attempts() -> None:
- 102: def always_fail():
- 104: raise RuntimeError("boom")
- 107: await retry(always_fail, max_attempts=2, delay=0.0)
- 110: def test_format_table_basic() -> None:
- 119: def test_format_table_alignment() -> None:
- 127: def test_get_logger_returns_logger() -> None:
- 129: import logging
- 132: assert isinstance(logger, logging.Logger)

## tests/tools/test_kpi.py

- 4: from tools.pm import kpi
- 7: def test_compute_throughput_function() -> None:
- 9: assert hasattr(kpi, "compute_throughput")
- 10: assert isinstance(kpi.compute_throughput([], []), int)

## tests/tools/test_metrics_collector.py

- 4: from pathlib import Path
- 7: def test_metrics_collector_api(tmp_path: Path) -> None:
- 10: from scripts.setup_structure import create_core_structure
- 14: import importlib.util
- 15: import sys
- 22: assert hasattr(module, "collect_metrics")
- 23: assert callable(module.collect_metrics)

## tests/tools/test_plugin_loader.py

- 4: import os
- 7: def test_plugin_loader_creates_directory() -> None:
- 10: import tools.agent_plugins  # noqa: F401

## tests/tools/test_pm_email.py

- 16: import pytest
- 18: from tools.pm.email import render
- 22: async def test_render_simple_substitution():
- 28: async def test_render_multiple_keys():
- 36: async def test_render_missing_key_leaves_placeholder():
- 42: async def test_render_empty_template():

## tests/tools/test_pm_kpi.py

- 16: import pytest
- 18: from tools.pm import kpi
- 21: def test_compute_throughput_basic():
- 25: def test_compute_throughput_empty():
- 29: def test_velocity_single_sprint():
- 33: def test_velocity_multiple_sprints():
- 37: def test_velocity_invalid_sprints():
- 42: def test_cycle_time_basic():
- 46: def test_cycle_time_invalid():
- 51: def test_defect_rate_basic():
- 55: def test_defect_rate_zero_bugs():
- 59: def test_defect_rate_invalid():
- 64: def test_sprint_health_green():
- 68: def test_sprint_health_amber():
- 72: def test_sprint_health_red():
- 76: def test_sprint_health_invalid():

## tests/tools/test_pm_risk.py

- 16: import pytest
- 18: from tools.pm.risk import Risk, read_matrix, top_risks
- 21: def test_risk_score_low_low():
- 26: def test_risk_score_high_high():
- 31: def test_risk_level_low():
- 36: def test_risk_level_medium():
- 41: def test_risk_level_high():
- 46: def test_risk_to_dict_keys():
- 53: async def test_read_matrix_pipe_table(tmp_path):
- 69: async def test_read_matrix_empty_file(tmp_path):
- 75: def test_top_risks_returns_top_n():

## tests/tools/test_pm_structure.py

- 4: import importlib.util
- 5: import os
- 8: def test_pm_package_present(tmp_path) -> None:

## tests/tools/test_risk.py

- 4: from pathlib import Path
- 6: import pytest
- 8: from tools.pm import risk
- 12: async def test_risk_matrix_reader_writer(tmp_path: Path) -> None:
- 18: assert isinstance(matrix, list)

## tests/tools/test_self_healing.py

- 4: from pathlib import Path
- 7: def test_self_healing_detects(tmp_path: Path) -> None:
- 9: from scripts.setup_structure import create_core_structure
- 13: import importlib.util
- 14: import sys
- 21: assert hasattr(module, "detect_misconfig")
- 23: assert isinstance(info, dict)

## tests/tools/test_structure_layout.py

- 4: import os
- 7: def test_tools_directories_exist() -> None:

## tests/tools/test_tool_registry.py

- 16: import pytest
- 18: from src.tools.tool_registry import (
- 29: def _clean_registry():
- 37: def test_register_and_retrieve() -> None:
- 38: def my_main(args=None):
- 48: def test_register_duplicate_same_description_is_idempotent() -> None:
- 49: def my_main(args=None):
- 57: def test_register_duplicate_different_description_raises() -> None:
- 58: def my_main(args=None):
- 66: def test_list_tools_sorted() -> None:
- 73: def test_run_tool_int_result() -> None:
- 78: def test_run_tool_unknown_raises() -> None:
- 83: def test_tool_frozen_dataclass() -> None:
- 84: def fn(a=None):
- 89: assert isinstance(t, Tool)
- 94: def test_main_cli_list(capsys) -> None:
- 96: from src.tools.__main__ import main
- 105: def test_main_cli_run() -> None:
- 107: from src.tools.__main__ import main
- 114: def test_main_cli_unknown_tool(capsys) -> None:
- 116: from src.tools.__main__ import main

## tests/tools/test_tools_cli.py

- 1: import subprocess
- 2: import sys
- 5: def test_tools_cli_help_runs_successfully() -> None:
- 17: def test_tools_cli_runs_netcalc_tool() -> None:

## tests/tools/test_tools_docs.py

- 1: def test_tools_document_exist() -> None:
- 3: import os
- 5: from src.tools.tool_registry import list_tools

## tests/tools/test_tools_registry.py

- 1: import subprocess
- 2: import sys
- 4: from src.tools.tool_registry import list_tools
- 7: def test_tools_list_all_registered() -> None:
- 12: def test_tools_cli_help_for_each_tool() -> None:

## tests/unit/test_CortAgent.py

- 21: from __future__ import annotations
- 23: from unittest.mock import AsyncMock
- 25: import pytest
- 27: from src.core.reasoning import (
- 34: from src.core.reasoning.CortAgent import CortMixin
- 35: from src.core.reasoning.CortCore import CortRecursionError
- 43: async def test_cort_agent_run_task_returns_cort_result() -> None:
- 52: assert isinstance(result, CortResult)
- 61: async def test_cort_agent_metadata_has_agent_id() -> None:
- 81: def test_cort_mixin_injects_into_base_agent() -> None:
- 84: class _StubBase:
- 89: class AgentWithCort(_StubBase, CortMixin):
- 101: def test_cort_agent_default_config() -> None:
- 116: async def test_cort_agent_reentrant_raises() -> None:
- 121: async def reentrant_llm(prompt: str, *, temperature: float, max_tokens: int) -> str:
- 151: async def test_cort_agent_run_task_string_input() -> None:
- 163: assert isinstance(result["result"], CortResult)

## tests/unit/test_CortCore.py

- 21: from __future__ import annotations
- 23: from unittest.mock import AsyncMock
- 25: import pytest
- 27: from src.core.reasoning import (
- 34: from src.core.reasoning.CortCore import (
- 47: def test_cort_config_defaults() -> None:
- 58: def test_cort_config_cap_enforcement() -> None:
- 69: def test_cort_config_valid_cap() -> None:
- 81: def test_reasoning_chain_ordering() -> None:
- 107: async def test_cort_result_has_best_chain() -> None:
- 116: assert isinstance(result, CortResult)
- 117: assert isinstance(result.best_chain, ReasoningChain)
- 129: async def test_cort_result_round_count() -> None:
- 147: async def test_cort_core_run_returns_cort_result() -> None:
- 156: assert isinstance(result, CortResult)
- 165: async def test_cort_core_calls_llm_n_times_m_alternatives() -> None:
- 183: async def test_cort_core_temperature_schedule() -> None:
- 187: async def recording_llm(prompt: str, *, temperature: float, max_tokens: int) -> str:
- 211: async def test_cort_recursion_guard() -> None:
- 218: async def reentrant_llm(prompt: str, *, temperature: float, max_tokens: int) -> str:
- 240: def test_cort_limit_exceeded() -> None:
- 251: def test_reasoning_chain_lt_notimplemented() -> None:
- 269: def test_reasoning_chain_gt_notimplemented() -> None:
- 287: def test_reasoning_chain_eq_notimplemented() -> None:
- 306: async def test_cort_core_early_stop_skips_remaining_rounds() -> None:
- 329: async def test_all_alternatives_fail_raises_alternatives_generation_error() -> None:
- 332: async def failing_llm(prompt: str, *, temperature: float, max_tokens: int) -> str:
- 334: raise RuntimeError("API error")

## tests/unit/test_EvaluationEngine.py

- 21: from __future__ import annotations
- 23: import pytest
- 25: from src.core.reasoning import EvaluationEngine
- 26: from src.core.reasoning.CortCore import ReasoningChain
- 27: from src.core.reasoning.EvaluationEngine import RubricScore
- 34: def test_rubric_score_weighted_total() -> None:
- 45: def test_rubric_score_weights() -> None:
- 64: def test_correctness_penalizes_contradictions() -> None:
- 86: def test_completeness_rewards_keyword_recall() -> None:
- 104: def test_reasoning_depth_rewards_connectives() -> None:
- 125: def test_reasoning_depth_rewards_structure() -> None:
- 144: def test_select_best_returns_highest_score() -> None:
- 159: def test_select_best_tie_breaks_by_depth() -> None:
- 178: def test_completeness_empty_prompt_keywords() -> None:
- 194: def test_reasoning_depth_caps_at_one() -> None:
- 212: def test_select_best_raises_value_error_on_empty_list() -> None:

## tests/unit/test_McpClient.py

- 20: from __future__ import annotations
- 22: import asyncio
- 23: import json
- 24: from typing import AsyncGenerator
- 25: from unittest.mock import AsyncMock, MagicMock, call
- 27: import pytest
- 29: from src.mcp.exceptions import McpCallTimeout, McpProtocolError
- 30: from src.mcp.McpClient import McpClient, McpToolDefinition, McpToolResult
- 31: from src.mcp.McpServerConfig import McpServerConfig
- 38: def _make_config(name: str = "test-server", timeout: float = 5.0) -> McpServerConfig:
- 62: def _make_process(stdout_responses: list[bytes]) -> MagicMock:
- 81: async def readline() -> bytes:
- 99: def _jsonrpc_response(req_id: int, result: object) -> bytes:
- 113: def _jsonrpc_error(req_id: int, code: int = -32603, message: str = "Internal error") -> bytes:
- 128: _CAPABILITIES_RESPONSE = _jsonrpc_response(
- 137: _INITIALIZED_NOTIFICATION = (
- 147: async def test_initialize_sends_initialize_request() -> None:
- 177: async def test_initialize_parses_capabilities_response() -> None:
- 202: async def test_list_tools_returns_tool_definitions() -> None:
- 245: async def test_call_tool_round_trip() -> None:
- 276: async def test_call_tool_timeout_raises_McpCallTimeout() -> None:  # noqa: N802
- 297: async def test_call_tool_protocol_error_raises_McpProtocolError() -> None:  # noqa: N802
- 319: async def test_close_cancels_reader_task_first() -> None:
- 333: def recording_stdin_close() -> None:
- 346: def recording_cancel(*args: object) -> bool:
- 368: async def test_correlation_id_matches_response() -> None:
- 382: async def capture_write(data: bytes) -> None:
- 394: async def dynamic_readline() -> bytes:
- 422: assert isinstance(result, McpToolResult)

## tests/unit/test_McpRegistry.py

- 20: from __future__ import annotations
- 22: import asyncio
- 23: from unittest.mock import AsyncMock, MagicMock, call, patch
- 25: import pytest
- 27: from src.mcp.exceptions import McpServerAlreadyEnabled, McpServerNotEnabled, McpServerNotFound
- 28: from src.mcp.McpRegistry import McpRegistry
- 29: from src.mcp.McpServerConfig import McpServerConfig
- 35: _SERVER_DICT = {
- 49: def registry() -> McpRegistry:
- 55: def loaded_registry() -> McpRegistry:
- 59: import asyncio as _asyncio
- 71: async def test_load_config_populates_servers(registry: McpRegistry) -> None:
- 97: async def test_enable_starts_sandbox_and_client(registry: McpRegistry) -> None:
- 134: async def test_disable_drains_inflight_before_terminate(registry: McpRegistry) -> None:
- 147: async def ordered_terminate(_process: object) -> None:
- 158: from src.mcp.McpRegistry import McpServerStatus  # noqa: PLC0415
- 188: async def test_reload_cycles_disable_then_enable(registry: McpRegistry) -> None:
- 199: async def mock_disable(name: str) -> None:
- 203: async def mock_enable(name: str) -> None:
- 222: def test_get_client_raises_when_not_enabled(registry: McpRegistry) -> None:
- 238: async def test_enable_already_enabled_is_idempotent(registry: McpRegistry) -> None:
- 250: async def counting_spawn(_config: object) -> MagicMock:
- 280: async def test_list_servers_returns_snapshot(registry: McpRegistry) -> None:
- 305: async def test_concurrent_enable_disable_safe(registry: McpRegistry) -> None:
- 344: async def test_reload_on_unknown_server_raises(registry: McpRegistry) -> None:

## tests/unit/test_McpSandbox.py

- 20: from __future__ import annotations
- 22: import asyncio
- 23: import hashlib
- 24: import os
- 25: import tempfile
- 26: from pathlib import Path
- 27: from unittest.mock import AsyncMock, MagicMock, patch
- 29: import pytest
- 31: from src.mcp.exceptions import McpPathForbidden, McpPinMismatch, McpSandboxError, McpSecretNotFound
- 32: from src.mcp.McpSandbox import McpSandbox
- 33: from src.mcp.McpServerConfig import McpServerConfig
- 40: def _make_config(
- 79: def test_build_env_inherits_allowed_vars() -> None:
- 102: def test_build_env_strips_disallowed_vars() -> None:
- 129: def test_masked_env_replaces_secrets_with_redacted() -> None:
- 155: def test_validate_path_allows_declared_paths(tmp_path: Path) -> None:
- 179: def test_validate_path_blocks_undeclared_paths(tmp_path: Path) -> None:
- 200: def test_validate_path_blocks_symlink_escape(tmp_path: Path) -> None:
- 225: async def test_spawn_uses_sanitised_env() -> None:
- 242: async def fake_create_subprocess_exec(*args: object, **kwargs: object) -> MagicMock:
- 261: async def test_terminate_sends_sigterm_then_sigkill() -> None:
- 275: def record_terminate() -> None:
- 280: def record_kill() -> None:
- 286: async def wait_that_never_returns() -> int:
- 300: async def fast_wait_for(coro: object, timeout: float) -> int:
- 325: async def test_spawn_raises_on_missing_command() -> None:
- 349: async def test_sha256_pin_validation() -> None:

## tests/unit/test_McpToolAdapter.py

- 20: from __future__ import annotations
- 22: from unittest.mock import AsyncMock, MagicMock
- 24: import pytest
- 26: from src.mcp.exceptions import McpToolNameCollision
- 27: from src.mcp.McpClient import McpClient, McpToolDefinition, McpToolResult
- 28: from src.mcp.McpSandbox import McpSandbox
- 29: from src.mcp.McpServerConfig import McpServerConfig
- 30: from src.mcp.McpToolAdapter import McpToolAdapter
- 37: def _make_tool_def(name: str, description: str = "A tool", schema: dict \| None = None) -> McpToolDefinition:
- 56: def _make_mock_client(tools: list[McpToolDefinition]) -> AsyncMock:
- 72: def _make_config(name: str = "fs") -> McpServerConfig:
- 95: def _make_adapter(existing_registry: dict \| None = None) -> McpToolAdapter:
- 116: async def test_register_server_tools_adds_namespaced_tools() -> None:
- 148: async def test_deregister_server_tools_removes_only_that_server() -> None:
- 181: def test_tool_schema_conversion_maps_types() -> None:
- 208: import asyncio
- 221: async def test_async_run_tool_calls_mcp_client() -> None:
- 244: await tool_main(["--path", "/workspace/notes.txt"])
- 259: async def test_namespace_collision_raises() -> None:
- 286: async def test_deregister_nonexistent_server_is_noop() -> None:

## tests/web/test_a11y_checklist.py

- 18: import pathlib
- 20: _WEB = pathlib.Path("web")
- 23: def _read(path: str) -> str:
- 30: def test_window_minimize_has_aria_label() -> None:
- 35: def test_window_maximize_restore_has_aria_label() -> None:
- 43: def test_window_close_has_aria_label() -> None:
- 48: def test_window_menu_has_aria_label() -> None:
- 53: def test_window_controls_have_focus_visible_ring() -> None:
- 61: def test_paint_pencil_has_aria_label() -> None:
- 66: def test_paint_eraser_has_aria_label() -> None:
- 71: def test_paint_clear_has_aria_label() -> None:
- 76: def test_paint_color_input_has_aria_label() -> None:
- 81: def test_paint_range_input_has_aria_label() -> None:
- 89: def test_editor_textarea_has_focus_ring() -> None:
- 98: def test_app_toggle_has_focus_ring() -> None:
- 108: def test_project_card_has_role_button() -> None:
- 113: def test_project_card_has_tab_index() -> None:
- 118: def test_project_card_has_keyboard_handler() -> None:
- 128: def test_project_card_has_aria_expanded() -> None:
- 136: def test_accent_colour_passes_aa_contrast() -> None:

## tests/zzz/test_yzz_python_function_coverage.py

- 11: from __future__ import annotations
- 13: import ast
- 14: import asyncio
- 15: import inspect
- 16: import sys
- 17: from pathlib import Path
- 18: from typing import Any, Dict, Iterator, List, Tuple
- 20: import pytest
- 22: ROOT = Path(__file__).resolve().parents[2]
- 23: SRC_ROOT = ROOT / "src"
- 27: MAX_FUNCTIONS = 200  # limit to keep runtime reasonable
- 30: def _iter_python_files(root: Path) -> Iterator[Path]:
- 39: def _module_name_from_path(path: Path, root: Path) -> str:
- 46: def _extract_functions_from_ast(source: str) -> List[Tuple[str, int]]:
- 65: def _gen_call_args(func_name: str, required: int) -> List[Tuple[Any, ...]]:
- 112: def _safe_call(func: Any, args: Tuple[Any, ...]) -> Tuple[bool, str]:
- 144: def test_exercise_python_functions(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
- 168: source = py_file.read_text(encoding="utf-8", errors="ignore")
- 203: def _format_map(m: Dict[str, str], limit: int = 10) -> str:
- 223: def main() -> int:
- 234: raise SystemExit(main())

## tests/zzz/test_zza_lint_config.py

- 5: import asyncio
- 6: import sys
- 7: from pathlib import Path
- 9: import pytest
- 13: async def test_ruff_command_intent_is_check_dot_fix(tmp_path: Path) -> None:

## tests/zzz/test_zzb_mypy_config.py

- 4: import os
- 5: import subprocess
- 6: import sys
- 7: from pathlib import Path
- 9: import pytest
- 12: def test_mypy_full_run_detects_problem(tmp_path: Path) -> None:

## tests/zzz/test_zzc_flake8_config.py

- 4: import subprocess
- 5: import sys
- 6: from pathlib import Path
- 8: import pytest
- 11: def test_flake8_repo_config_has_no_repo_issues() -> None:

## tests/zzz/test_zzc_mypy_strict_lane_smoke.py

- 4: import subprocess
- 5: import sys
- 6: from pathlib import Path
- 8: import pytest
- 10: STRICT_CONFIG_PATH = Path("mypy-strict-lane.ini")
- 11: BAD_FIXTURE_PATH = Path("tests/fixtures/mypy_strict_lane/bad_case.py")
- 14: def test_mypy_strict_lane_rejects_known_bad_fixture() -> None:

## tests/zzz/test_zzd_codeql_python.py

- 16: Set CODEQL_SKIP=1 to bypass entirely (e.g. in very fast local loops).
- 17: Set CODEQL_REBUILD=1 to force a database rebuild even when the SARIF is fresh.
- 20: import json
- 21: import os
- 22: import shutil
- 23: import subprocess
- 24: from pathlib import Path
- 26: import pytest
- 28: REPO_ROOT = Path(__file__).resolve().parents[2]
- 31: def _resolve_codeql_exe() -> Path:
- 42: CODEQL_EXE = _resolve_codeql_exe()
- 43: DB_PATH = REPO_ROOT / "databases" / "python-db"
- 44: SARIF_PATH = REPO_ROOT / "results" / "python.sarif"
- 45: SOURCE_ROOT = REPO_ROOT / "src"
- 46: MAX_SARIF_AGE_HOURS = 24
- 49: def _codeql_available() -> bool:
- 53: def _sarif_age_hours() -> float \| None:
- 56: import time
- 61: def _rebuild_db() -> None:
- 78: def _run_analysis() -> None:
- 98: def test_codeql_exe_exists() -> None:
- 106: def test_python_sarif_is_fresh_or_rebuilt() -> None:
- 136: def test_python_sarif_execution_succeeded() -> None:
- 150: def test_python_sarif_scanned_files() -> None:
- 162: def test_python_no_new_security_findings() -> None:

## tests/zzz/test_zze_codeql_javascript.py

- 16: Set CODEQL_SKIP=1 to bypass entirely.
- 17: Set CODEQL_REBUILD=1 to force a database rebuild even when the SARIF is fresh.
- 20: import json
- 21: import os
- 22: import shutil
- 23: import subprocess
- 24: from pathlib import Path
- 26: import pytest
- 28: REPO_ROOT = Path(__file__).resolve().parents[2]
- 31: def _resolve_codeql_exe() -> Path:
- 42: CODEQL_EXE = _resolve_codeql_exe()
- 43: DB_PATH = REPO_ROOT / "databases" / "javascript-db"
- 44: SARIF_PATH = REPO_ROOT / "results" / "javascript.sarif"
- 45: SOURCE_ROOT = REPO_ROOT / "web"
- 46: MAX_SARIF_AGE_HOURS = 24
- 49: def _codeql_available() -> bool:
- 53: def _sarif_age_hours() -> float \| None:
- 56: import time
- 61: def _rebuild_db() -> None:
- 78: def _run_analysis() -> None:
- 98: def test_javascript_sarif_is_fresh_or_rebuilt() -> None:
- 128: def test_javascript_sarif_execution_succeeded() -> None:
- 142: def test_javascript_sarif_scanned_files() -> None:
- 154: def test_javascript_no_new_security_findings() -> None:

## tests/zzz/test_zzf_codeql_rust.py

- 16: Set CODEQL_SKIP=1 to bypass entirely.
- 17: Set CODEQL_REBUILD=1 to force a database rebuild even when the SARIF is fresh.
- 20: import json
- 21: import os
- 22: import shutil
- 23: import subprocess
- 24: from pathlib import Path
- 26: import pytest
- 28: REPO_ROOT = Path(__file__).resolve().parents[2]
- 31: def _resolve_codeql_exe() -> Path:
- 42: CODEQL_EXE = _resolve_codeql_exe()
- 43: DB_PATH = REPO_ROOT / "databases" / "rust-db"
- 44: SARIF_PATH = REPO_ROOT / "results" / "rust.sarif"
- 45: SOURCE_ROOT = REPO_ROOT / "rust_core"
- 46: MAX_SARIF_AGE_HOURS = 24
- 49: def _codeql_available() -> bool:
- 53: def _sarif_age_hours() -> float \| None:
- 56: import time
- 61: def _rebuild_db() -> None:
- 78: def _run_analysis() -> None:
- 99: def test_rust_sarif_is_fresh_or_rebuilt() -> None:
- 129: def test_rust_sarif_execution_succeeded() -> None:
- 143: def test_rust_sarif_scanned_files() -> None:
- 155: def test_rust_no_security_findings() -> None:

## tests/zzz/test_zzg_codeql_sarif_gate.py

- 21: Set CODEQL_SKIP=1 to bypass entirely.
- 24: import json
- 25: import os
- 26: import shutil
- 27: import time
- 28: from pathlib import Path
- 29: from typing import NamedTuple
- 31: import pytest
- 33: REPO_ROOT = Path(__file__).resolve().parents[2]
- 34: RESULTS_DIR = REPO_ROOT / "results"
- 35: MAX_SARIF_AGE_HOURS = 24
- 38: class _SarifSpec(NamedTuple):
- 46: _SARIF_SPECS: list[_SarifSpec] = [
- 54: _hard_fail_rule_prefixes = (
- 93: def _codeql_available() -> bool:
- 103: def test_all_sarif_files_exist() -> None:
- 114: def test_all_sarif_files_are_fresh() -> None:
- 135: def test_all_analyses_completed_successfully() -> None:
- 152: def test_no_hard_fail_security_findings() -> None:
- 173: def test_finding_count_within_baseline() -> None:

## tests/zzz/ztest_zzz_tests_quality.py

- 17: import ast
- 18: from pathlib import Path
- 20: import pytest
- 23: def _has_pytest_raises(tree: ast.AST) -> bool:
- 36: def test_all_test_files_meet_quality(pytestconfig: pytest.Config) -> None:

## tests/docs/test_agent_workflow_policy_docs.py

- 15: from pathlib import Path
- 17: REPO_ROOT = Path(__file__).resolve().parents[2]
- 20: def _read(relative_path: str) -> str:
- 25: def _normalize(text: str) -> str:
- 30: def test_0master_documents_project_numbering_ownership_and_continuity() -> None:
- 47: def test_1project_requires_assigned_identifier_and_template_sections() -> None:
- 62: def test_1project_enforces_branch_gate_before_handoff() -> None:
- 74: def test_0master_enforces_delegation_preflight_branch_gate() -> None:
- 86: def test_9git_enforces_branch_scope_and_failure_rules() -> None:
- 114: def test_downstream_agents_require_branch_gate_before_work() -> None:
- 251: def test_all_workflow_agents_carry_exact_branch_governance_contract() -> None:
- 268: def test_legacy_git_summaries_document_branch_exception_and_corrective_ownership() -> None:
- 320: def test_git_summaries_use_modern_branch_plan_format_or_carry_legacy_exception() -> None:
- 374: def test_every_project_folder_has_a_project_overview() -> None:
- 419: def test_project_folder_numbers_are_unique_or_documented_legacy_duplicates() -> None:
- 429: import re
- 430: from collections import defaultdict
- 531: def test_project_overviews_use_modern_template_or_carry_legacy_exception() -> None:

## tests/docs/test_codestructure_governance.py

- 15: from pathlib import Path
- 16: import re
- 18: REPO_ROOT = Path(__file__).resolve().parents[2]
- 19: CODESTRUCTURE_PATH = REPO_ROOT / ".github" / "agents" / "data" / "codestructure.md"
- 20: CODESTRUCTURE_DATA_DIR = REPO_ROOT / ".github" / "agents" / "data"
- 21: REQUIRED_SPLIT_FILES = (
- 30: ROW_PATTERN = re.compile(r"^-\s*(\d+)\s*:\s*(.+)\s*$")
- 33: def _read_codestructure_text() -> str:
- 43: def _parse_data_rows(text: str) -> list[tuple[str, int, str]]:
- 76: def _all_codestructure_paths() -> list[Path]:
- 86: def test_codestructure_file_exists_at_canonical_path() -> None:
- 91: def test_required_codestructure_split_files_exist() -> None:
- 97: def test_codestructure_rows_across_manifest_and_splits_are_valid() -> None:

## tests/test_orchestration_graph.py

- 19: from __future__ import annotations
- 21: import uuid
- 23: import pytest
- 24: from fastapi.testclient import TestClient
- 26: from backend.app import _log_path, app
- 38: def _restore_agent_log():
- 50: def test_agent_log_endpoint_returns_200() -> None:
- 56: def test_agent_log_response_has_correct_fields() -> None:
- 65: def test_agent_log_accepts_put_request() -> None:
- 74: def test_agent_log_put_stores_data() -> None:
- 85: def test_agent_log_roundtrip() -> None:
