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

"""Compose context contract tests for clean-checkout path semantics."""

from __future__ import annotations

from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPOSE_FILE = REPO_ROOT / "deploy" / "compose.yaml"


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    """Load a YAML mapping from disk.

    Args:
        path: Absolute path to the YAML file.

    Returns:
        Parsed YAML object as a dictionary mapping.

    """
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError as error:
        raise AssertionError("PyYAML is required for deploy contract tests") from error

    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict), f"YAML file must parse to mapping: {path}"
    return loaded


def _pyagent_build_contract(compose_file: Path) -> tuple[str, str]:
    """Extract the pyagent build context and Dockerfile contract.

    Args:
        compose_file: Compose manifest path.

    Returns:
        Tuple containing build context and Dockerfile values.

    """
    compose_obj = _load_yaml_mapping(compose_file)

    services = compose_obj.get("services")
    assert isinstance(services, dict), "compose must contain services mapping"

    pyagent = services.get("pyagent")
    assert isinstance(pyagent, dict), "compose must define services.pyagent"

    build = pyagent.get("build")
    assert isinstance(build, dict), "services.pyagent.build must be a mapping"

    context_value = build.get("context")
    dockerfile_value = build.get("dockerfile")

    assert isinstance(context_value, str), "services.pyagent.build.context must be string"
    assert isinstance(dockerfile_value, str), "services.pyagent.build.dockerfile must be string"
    return context_value, dockerfile_value


def test_pyagent_build_context_resolves_inside_repository_root() -> None:
    """Compose build context must resolve to an existing in-repo directory."""
    context_value, _ = _pyagent_build_contract(COMPOSE_FILE)
    resolved_context = (COMPOSE_FILE.parent / context_value).resolve()

    assert resolved_context.exists(), f"Resolved context does not exist: {resolved_context}"
    assert resolved_context.is_dir(), f"Resolved context is not a directory: {resolved_context}"
    assert REPO_ROOT == resolved_context, (
        "Clean-checkout contract regression: expected context to resolve to repository root "
        f"'{REPO_ROOT}', got '{resolved_context}'."
    )


def test_pyagent_dockerfile_path_is_relative_and_repo_local() -> None:
    """Compose Dockerfile path must be repo-relative for deterministic checkout behavior."""
    _, dockerfile_value = _pyagent_build_contract(COMPOSE_FILE)

    dockerfile_path = Path(dockerfile_value)
    assert not dockerfile_path.is_absolute(), (
        "Dockerfile contract regression: absolute path is not allowed for compose build.dockerfile "
        f"('{dockerfile_value}')."
    )

    resolved_dockerfile = (REPO_ROOT / dockerfile_path).resolve()
    assert resolved_dockerfile.exists(), f"Referenced Dockerfile does not exist: {resolved_dockerfile}"
    assert resolved_dockerfile.is_file(), f"Referenced Dockerfile is not a file: {resolved_dockerfile}"
