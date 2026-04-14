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

"""Check parity between generated and committed requirements.txt files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import cast

try:
    import tomllib
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


REMEDIATION_COMMAND = "python scripts/deps/generate_requirements.py --output requirements.txt"
_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*")


def _canonical_key(name: str) -> str:
    """Build a canonical package key for case-insensitive matching.

    Args:
        name: Raw package name token.

    Returns:
        Canonicalized package key using PEP 503 style normalization.

    """
    return re.sub(r"[-_.]+", "-", name).lower()


def _split_requirement(requirement: str) -> tuple[str, str] | None:
    """Split requirement into leading package token and trailing specifier text.

    Args:
        requirement: Requirement line from pyproject or requirements.txt.

    Returns:
        Tuple of package token and remainder, or ``None`` when no package token is present.

    """
    match = _NAME_PATTERN.match(requirement)
    if match is None:
        return None

    name = match.group(0)
    return name, requirement[len(name) :]


def _existing_name_map(requirements_path: Path) -> dict[str, str]:
    """Load existing package-name casing preferences from requirements.txt.

    Args:
        requirements_path: Path to requirements file that may already exist.

    Returns:
        Mapping of canonical package key to previously committed package token.

    """
    if not requirements_path.exists():
        return {}

    mapping: dict[str, str] = {}
    for raw_line in requirements_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        split = _split_requirement(line)
        if split is None:
            continue
        name, _ = split
        mapping[_canonical_key(name)] = name

    return mapping


def _normalize_dependency_name_case(dependencies: list[str], existing_names: dict[str, str]) -> list[str]:
    """Normalize dependency package token casing using existing requirements when possible.

    Args:
        dependencies: Dependency strings from pyproject.
        existing_names: Existing casing preferences keyed by canonical package name.

    Returns:
        Dependency lines with stable package token casing.

    """
    normalized_lines: list[str] = []
    for dependency in dependencies:
        split = _split_requirement(dependency)
        if split is None:
            normalized_lines.append(dependency)
            continue

        name, remainder = split
        preferred = existing_names.get(_canonical_key(name), name)
        normalized_lines.append(f"{preferred}{remainder}")

    return normalized_lines


def _read_project_dependencies(pyproject_path: Path) -> list[str]:
    """Read dependency entries from ``[project.dependencies]``.

    Args:
        pyproject_path: Path to the workspace pyproject.toml file.

    Returns:
        Parsed dependency strings from ``[project.dependencies]``.

    Raises:
        ValueError: When parsing fails or dependency shape is invalid.

    """
    try:
        data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError("failed to parse pyproject.toml: file not found") from exc
    except tomllib.TOMLDecodeError as exc:
        raise ValueError("failed to parse pyproject.toml") from exc

    dependencies = data.get("project", {}).get("dependencies")
    if not isinstance(dependencies, list):
        raise ValueError("failed to parse pyproject.toml: [project.dependencies] must be a list of strings")

    normalized: list[str] = []
    for item in cast(list[object], dependencies):
        if not isinstance(item, str):
            raise ValueError("failed to parse pyproject.toml: [project.dependencies] must be a list of strings")
        stripped = item.strip()
        if stripped:
            normalized.append(stripped)

    return sorted(normalized, key=str.lower)


def _render_requirements(dependencies: list[str]) -> str:
    """Render requirements content with a stable trailing newline.

    Args:
        dependencies: Normalized dependency lines.

    Returns:
        Deterministic requirements content.

    """
    return "\n".join(dependencies) + "\n"


def _run_check(workspace: Path) -> int:
    """Perform dependency parity check and print actionable output.

    Args:
        workspace: Directory containing pyproject.toml and requirements.txt.

    Returns:
        Process exit code where ``0`` indicates parity.

    """
    pyproject_path = workspace / "pyproject.toml"
    requirements_path = workspace / "requirements.txt"

    existing_names = _existing_name_map(requirements_path)

    try:
        dependencies = _read_project_dependencies(pyproject_path)
        normalized_dependencies = _normalize_dependency_name_case(dependencies, existing_names)
        expected = _render_requirements(normalized_dependencies)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if not requirements_path.exists():
        print("dependency parity check failed: requirements.txt is missing", file=sys.stderr)
        print(f"run: {REMEDIATION_COMMAND}", file=sys.stderr)
        return 1

    current = requirements_path.read_text(encoding="utf-8")
    if current == expected:
        print("Parity check passed")
        return 0

    print("Dependency parity check failed: manual edit detected in requirements.txt", file=sys.stderr)
    print(f"Run: {REMEDIATION_COMMAND}", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    """Run the dependency parity CLI command.

    Args:
        argv: Optional command-line arguments.

    Returns:
        Process exit code where ``0`` indicates success.

    """
    parser = argparse.ArgumentParser(description="Check generated requirements parity")
    parser.add_argument("--check", action="store_true", help="Validate parity and return non-zero on drift")
    args = parser.parse_args(argv)

    if not args.check:
        parser.print_help()
        return 0

    return _run_check(Path.cwd())


if __name__ == "__main__":
    raise SystemExit(main())
