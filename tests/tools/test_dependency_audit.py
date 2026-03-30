#!/usr/bin/env python3
"""Tests for canonical dependency sync and policy checks."""

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

from pathlib import Path

from src.tools import dependency_audit


def _write_pyproject(path: Path, dependencies: list[str], optional: list[str] | None = None) -> None:
    """Write a minimal pyproject file for dependency tests.

    Args:
        path: Target pyproject path.
        dependencies: Runtime dependencies for [project.dependencies].
        optional: Optional dependencies to prove they are non-canonical.

    """
    optional_entries = optional or []
    optional_block = "\n".join(f'    "{dep}",' for dep in optional_entries)
    optional_section = f"\n[project.optional-dependencies]\ndev = [\n{optional_block}\n]\n" if optional_entries else ""

    dep_block = "\n".join(f'    "{dep}",' for dep in dependencies)
    content = f'[project]\nname = "tmp"\nversion = "0.1.0"\ndependencies = [\n{dep_block}\n]\n{optional_section}'
    path.write_text(content, encoding="utf-8")


def test_dependency_canonical_pyproject_uses_project_dependencies_only(tmp_path: Path) -> None:
    """Canonical dependency reader ignores optional dependency sections."""
    project_root = tmp_path
    _write_pyproject(
        project_root / "pyproject.toml",
        dependencies=["requests>=2.32", "fastapi>=0.128.0"],
        optional=["pytest>=8.0"],
    )

    generated_issues = dependency_audit.generate_requirements(str(project_root))
    assert generated_issues == []

    content = (project_root / "requirements.txt").read_text(encoding="utf-8")
    assert "requests>=2.32" in content
    assert "fastapi>=0.128.0" in content
    assert "pytest>=8.0" not in content


def test_requirements_deterministic_output_is_byte_equivalent() -> None:
    """Deterministic renderer emits identical output from reordered equal inputs."""
    deps_a = ["HTTPX>=0.28.1", "fastapi>=0.128.0", "requests>=2.32.0"]
    deps_b = ["requests>=2.32.0", "fastapi>=0.128.0", "httpx>=0.28.1"]

    output_a = dependency_audit.render_requirements_content(deps_a)
    output_b = dependency_audit.render_requirements_content(deps_b)

    assert output_a == output_b
    assert output_a == "fastapi>=0.128.0\nhttpx>=0.28.1\nrequests>=2.32.0\n"


def test_dependency_drift_detected_when_requirements_do_not_match_generated(tmp_path: Path) -> None:
    """Parity check reports drift when committed requirements diverge."""
    project_root = tmp_path
    _write_pyproject(project_root / "pyproject.toml", ["requests>=2.32.0", "fastapi>=0.128.0"])
    (project_root / "requirements.txt").write_text("requests==1.0.0\n", encoding="utf-8")

    issues = dependency_audit.check_dependencies(str(project_root))

    assert issues
    assert any("drift detected" in issue for issue in issues)


def test_dependency_policy_rejects_duplicates_malformed_and_critical_specs() -> None:
    """Policy validation catches duplicate names, malformed specs, and critical-package violations."""
    dependencies = [
        "requests>=2.32.0",
        "Requests>=2.33.0",
        "fastapi<0.128.0",
        "not a valid requirement",
    ]

    issues = dependency_audit._validate_dependency_policy(dependencies)

    assert any("Duplicate dependency 'requests'" in issue for issue in issues)
    assert any("Critical package 'fastapi'" in issue for issue in issues)
    assert any("Malformed dependency" in issue for issue in issues)


def test_dependency_policy_passes_for_valid_critical_specifiers() -> None:
    """Critical package policy allows pinned or lower-bound specifiers."""
    issues = dependency_audit._validate_dependency_policy(
        ["fastapi>=0.128.0", "pydantic==2.10.0", "requests>=2.32.0"],
    )
    assert issues == []


def test_dependency_and_drift_and_ci_run_checks_invokes_dependency_gate() -> None:
    """Shared CI checks module wires dependency gate into both profiles."""
    run_checks_text = Path("scripts/ci/run_checks.py").read_text(encoding="utf-8")
    assert "run_dependency_sync_gate()" in run_checks_text
    assert "src.tools.dependency_audit" in run_checks_text
