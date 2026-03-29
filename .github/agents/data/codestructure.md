# Code Structure Index

Agents must keep this file updated whenever introducing or changing imports, globals, classes, or functions. Add or update rows for affected anchors.

| file | line | code |
|---|---:|---|
| rust_core/src/base/auth.rs | 1 | use pyo3::prelude::*; |
| rust_core/src/base/auth.rs | 15 | pub fn generate_challenge(agent_id: &str, timestamp: f64) -> PyResult<String> { |
| scripts/ci/run_checks.py | 13 | from __future__ import annotations |
| scripts/ci/run_checks.py | 94 | CODEQL_TEST_FILES = [ |
| tests/docs/test_allowed_websites_governance.py | 15 | from pathlib import Path |
| tests/docs/test_allowed_websites_governance.py | 17 | REPO_ROOT = Path(__file__).resolve().parents[2] |
| tests/docs/test_allowed_websites_governance.py | 51 | def test_canonical_allowlist_location_and_root_absence() -> None: |
| tests/docs/test_codestructure_governance.py | 15 | from pathlib import Path |
| tests/docs/test_codestructure_governance.py | 17 | REPO_ROOT = Path(__file__).resolve().parents[2] |
| tests/docs/test_codestructure_governance.py | 61 | def test_codestructure_has_required_table_schema_and_integer_line_values() -> None: |
| tests/docs/test_copilot_instructions_governance.py | 15 | from pathlib import Path |
| tests/docs/test_copilot_instructions_governance.py | 17 | REPO_ROOT = Path(__file__).resolve().parents[2] |
| tests/docs/test_copilot_instructions_governance.py | 39 | def test_copilot_instructions_reference_canonical_allowlist_path() -> None: |
