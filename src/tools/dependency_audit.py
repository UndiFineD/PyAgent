#!/usr/bin/env python3
"""Dependency synchronization and policy audit utility.

This module treats ``pyproject.toml`` ``[project.dependencies]`` as the only
runtime dependency authority, emits deterministic ``requirements.txt`` output,
and validates drift/policy constraints.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path

from packaging.requirements import InvalidRequirement, Requirement
from packaging.utils import canonicalize_name

try:
    import tomllib  # type: ignore
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


CRITICAL_PACKAGE_POLICY: dict[str, tuple[str, ...]] = {
    "cryptography": (">=", "=="),
    "fastapi": (">=", "=="),
    "openai": (">=", "=="),
    "pydantic": (">=", "=="),
}


def _load_pyproject_dependencies(pyproject_path: Path) -> list[str]:
    """Load runtime dependencies from ``[project.dependencies]``.

    Args:
        pyproject_path: Path to ``pyproject.toml``.

    Returns:
        Dependencies from ``[project.dependencies]``.

    Raises:
        FileNotFoundError: When the pyproject file does not exist.
        ValueError: When the dependency section is missing or malformed.

    """
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found")

    with pyproject_path.open("rb") as file_obj:
        data = tomllib.load(file_obj)

    raw_dependencies = data.get("project", {}).get("dependencies")
    if raw_dependencies is None:
        raise ValueError("[project.dependencies] is missing")
    if not isinstance(raw_dependencies, list):
        raise ValueError("[project.dependencies] must be a list")
    if not all(isinstance(item, str) for item in raw_dependencies):
        raise ValueError("[project.dependencies] entries must be strings")

    return [item.strip() for item in raw_dependencies]


def _normalize_dependency(dep: str) -> str:
    """Normalize one dependency specifier to deterministic text.

    Args:
        dep: Raw dependency string.

    Returns:
        A deterministic dependency string.

    Raises:
        InvalidRequirement: When ``dep`` is malformed.

    """
    requirement = Requirement(dep)
    normalized_name = canonicalize_name(requirement.name)
    normalized = normalized_name

    if requirement.extras:
        extras = ",".join(sorted(requirement.extras))
        normalized += f"[{extras}]"
    if str(requirement.specifier):
        normalized += str(requirement.specifier)
    if requirement.marker:
        normalized += f"; {requirement.marker}"

    return normalized


def render_requirements_content(dependencies: list[str]) -> str:
    """Render deterministic requirements.txt content.

    Args:
        dependencies: Canonical dependency strings.

    Returns:
        Stable requirements content ending with a trailing newline.

    Raises:
        ValueError: When duplicate package names are detected.
        InvalidRequirement: When any dependency string is malformed.

    """
    normalized_items = [
        (canonicalize_name(Requirement(dep).name), _normalize_dependency(dep), dep) for dep in dependencies
    ]
    package_names = [item[0] for item in normalized_items]
    duplicate_name = next(
        (name for index, name in enumerate(package_names) if name in package_names[:index]),
        None,
    )
    if duplicate_name is not None:
        first_index = package_names.index(duplicate_name)
        second_index = next(
            index for index, name in enumerate(package_names) if name == duplicate_name and index != first_index
        )
        previous_dep = normalized_items[first_index][2]
        duplicate_dep = normalized_items[second_index][2]
        raise ValueError(
            f"Duplicate dependency '{duplicate_name}' found: '{previous_dep}' and '{duplicate_dep}'",
        )

    sorted_normalized = sorted(
        ((item[0], item[1]) for item in normalized_items),
        key=lambda item: (item[0], item[1]),
    )
    lines = [pair[1] for pair in sorted_normalized]
    return "\n".join(lines) + "\n"


def _validate_dependency_policy(dependencies: list[str]) -> list[str]:
    """Validate dependency policy constraints.

    Args:
        dependencies: Canonical dependency strings.

    Returns:
        A list of policy violation messages.

    """
    seen_names: set[str] = set()

    def _validate_single_dependency(dep: str) -> list[str]:
        try:
            requirement = Requirement(dep)
        except InvalidRequirement as exc:
            return [f"Malformed dependency '{dep}': {exc}"]

        package_name = canonicalize_name(requirement.name)
        if package_name in seen_names:
            return [f"Duplicate dependency '{package_name}'"]
        seen_names.add(package_name)

        if package_name in CRITICAL_PACKAGE_POLICY:
            allowed_ops = CRITICAL_PACKAGE_POLICY[package_name]
            if not requirement.specifier:
                return [
                    f"Critical package '{package_name}' must have a version specifier",
                ]

            disallowed_operators = [spec.operator for spec in requirement.specifier if spec.operator not in allowed_ops]
            if disallowed_operators:
                allowed = ", ".join(allowed_ops)
                return [
                    (f"Critical package '{package_name}' has disallowed operator '{operator}' (allowed: {allowed})")
                    for operator in disallowed_operators
                ]

        return []

    violation_groups = [_validate_single_dependency(dep) for dep in dependencies]
    return [violation for group in violation_groups for violation in group]


def _requirements_drift_issues(project_root: Path, expected_content: str) -> list[str]:
    """Build drift issues by comparing generated and committed requirements.

    Args:
        project_root: Repository root path.
        expected_content: Deterministic requirements content.

    Returns:
        Drift issues and optional unified diff lines.

    """
    req_path = project_root / "requirements.txt"
    if not req_path.exists():
        return ["requirements.txt not found"]

    current = req_path.read_text(encoding="utf-8")
    if current == expected_content:
        return []

    diff_lines = list(
        difflib.unified_diff(
            current.splitlines(),
            expected_content.splitlines(),
            fromfile="requirements.txt",
            tofile="generated:requirements.txt",
            lineterm="",
        ),
    )
    issues = ["requirements.txt drift detected"]
    issues.extend(diff_lines)
    return issues


def check_dependencies(project_root: str = ".") -> list[str]:
    """Run canonical dependency parity and policy checks.

    Args:
        project_root: Repository root directory.

    Returns:
        A list of issues. Empty means parity and policy checks passed.

    """
    root_path = Path(project_root)
    pyproject_path = root_path / "pyproject.toml"

    try:
        dependencies = _load_pyproject_dependencies(pyproject_path)
    except (FileNotFoundError, ValueError, tomllib.TOMLDecodeError) as exc:
        return [str(exc)]

    policy_issues = _validate_dependency_policy(dependencies)

    try:
        expected_requirements = render_requirements_content(dependencies)
    except (InvalidRequirement, ValueError) as exc:
        return [str(exc)] + policy_issues

    drift_issues = _requirements_drift_issues(root_path, expected_requirements)
    return policy_issues + drift_issues


def generate_requirements(project_root: str = ".") -> list[str]:
    """Generate deterministic requirements.txt from canonical dependencies.

    Args:
        project_root: Repository root directory.

    Returns:
        A list of issues encountered during generation.

    """
    root_path = Path(project_root)
    pyproject_path = root_path / "pyproject.toml"
    req_path = root_path / "requirements.txt"

    try:
        dependencies = _load_pyproject_dependencies(pyproject_path)
        policy_issues = _validate_dependency_policy(dependencies)
        if policy_issues:
            return policy_issues
        content = render_requirements_content(dependencies)
    except (FileNotFoundError, ValueError, InvalidRequirement, tomllib.TOMLDecodeError) as exc:
        return [str(exc)]

    req_path.write_text(content, encoding="utf-8")
    return []


def main(args: list[str] | None = None) -> int:
    """Main entry point for the dependency audit tool.

    Args:
        args: Optional command-line arguments.

    Returns:
        Process exit code.

    """
    parser = argparse.ArgumentParser(prog="dependency_audit")
    parser.add_argument("--root", default=".", help="Project root directory")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate requirements.txt from canonical pyproject dependencies",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail with exit code 1 when dependency drift or policy violations exist",
    )

    parsed = parser.parse_args(args=args)
    if parsed.generate:
        issues = generate_requirements(parsed.root)
    else:
        issues = check_dependencies(parsed.root)

    if parsed.json:
        print(json.dumps({"issues": issues}, indent=2))
    else:
        if issues:
            print("\n".join(issues))
        else:
            print("Dependency parity and policy checks passed")

    if parsed.check and issues:
        return 1
    return 0


register_tool("dependency_audit", main, "Audit dependency manifests (pyproject/requirements)")


if __name__ == "__main__":
    raise SystemExit(main())
