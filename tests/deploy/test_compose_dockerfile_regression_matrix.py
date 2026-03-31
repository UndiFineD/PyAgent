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

"""Regression matrix for compose Dockerfile path contracts across manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

_CONTRACT_MATRIX = [
    ("deploy/compose.yaml", "pyagent", "deploy/Dockerfile.pyagent"),
    ("deploy/docker-compose.yaml", "fleet_master", "deploy/Dockerfile.fleet"),
    ("deploy/docker-compose.yaml", "agent_node_0", "deploy/Dockerfile.fleet"),
    ("deploy/docker-compose.yaml", "agent_node_1", "deploy/Dockerfile.fleet"),
]


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    """Load YAML file as a mapping.

    Args:
        path: Absolute file path.

    Returns:
        Parsed YAML mapping.

    """
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError as error:
        raise AssertionError("PyYAML is required for compose regression matrix tests") from error

    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict), f"Compose file must parse to mapping: {path}"
    return loaded


@pytest.mark.parametrize(
    ("manifest_relative", "service_name", "expected_dockerfile"),
    _CONTRACT_MATRIX,
)
def test_compose_service_uses_expected_dockerfile_contract(
    manifest_relative: str,
    service_name: str,
    expected_dockerfile: str,
) -> None:
    """Each compose service in the matrix must keep its expected Dockerfile path."""
    manifest_path = REPO_ROOT / manifest_relative
    compose_obj = _load_yaml_mapping(manifest_path)

    services = compose_obj.get("services")
    assert isinstance(services, dict), f"services must be mapping in {manifest_relative}"

    service = services.get(service_name)
    assert isinstance(service, dict), f"service '{service_name}' missing in {manifest_relative}"

    build = service.get("build")
    assert isinstance(build, dict), f"service '{service_name}' build mapping missing in {manifest_relative}"

    dockerfile_value = build.get("dockerfile")
    assert dockerfile_value == expected_dockerfile, (
        f"Dockerfile regression in {manifest_relative}:{service_name}; "
        f"expected '{expected_dockerfile}', got '{dockerfile_value}'."
    )


@pytest.mark.parametrize(("manifest_relative", "_service_name", "expected_dockerfile"), _CONTRACT_MATRIX)
def test_compose_referenced_dockerfiles_exist(
    manifest_relative: str,
    _service_name: str,
    expected_dockerfile: str,
) -> None:
    """Every expected Dockerfile from the matrix must exist in the repository."""
    dockerfile_path = (REPO_ROOT / expected_dockerfile).resolve()
    assert dockerfile_path.exists(), (
        f"Missing Dockerfile for compose regression matrix '{manifest_relative}': {dockerfile_path}"
    )
    assert dockerfile_path.is_file(), f"Expected file path, got non-file: {dockerfile_path}"
