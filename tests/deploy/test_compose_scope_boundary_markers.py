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

"""Scope-boundary marker tests for deploy compose files in prj0000109."""

from __future__ import annotations

from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    """Load YAML file as dictionary mapping.

    Args:
        path: Absolute path to YAML file.

    Returns:
        Parsed YAML mapping.

    """
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError as error:
        raise AssertionError("PyYAML is required for compose scope-boundary tests") from error

    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict), f"YAML file must parse to mapping: {path}"
    return loaded


def _service_build_dockerfiles(path: Path) -> dict[str, str]:
    """Extract service-to-dockerfile mapping for a compose manifest.

    Args:
        path: Compose manifest path.

    Returns:
        Mapping of service name to Dockerfile value.

    """
    compose_obj = _load_yaml_mapping(path)
    services = compose_obj.get("services")
    assert isinstance(services, dict), f"services mapping missing in {path}"

    result: dict[str, str] = {}
    for service_name, service_obj in services.items():
        assert isinstance(service_name, str), "service name must be string"
        assert isinstance(service_obj, dict), f"service '{service_name}' must be mapping"

        build = service_obj.get("build")
        if not isinstance(build, dict):
            continue

        dockerfile_value = build.get("dockerfile")
        if isinstance(dockerfile_value, str):
            result[service_name] = dockerfile_value

    return result


def test_canonical_compose_pyagent_dockerfile_marker_is_project_specific() -> None:
    """Canonical compose must keep the pyagent-specific Dockerfile marker."""
    marker_map = _service_build_dockerfiles(REPO_ROOT / "deploy" / "compose.yaml")

    assert marker_map.get("pyagent") == "deploy/Dockerfile.pyagent", (
        "Scope marker regression: compose.yaml pyagent service no longer points to deploy/Dockerfile.pyagent."
    )


def test_fleet_compose_nodes_share_fleet_dockerfile_marker() -> None:
    """Fleet compose nodes must keep shared fleet Dockerfile marker."""
    marker_map = _service_build_dockerfiles(REPO_ROOT / "deploy" / "docker-compose.yaml")

    assert marker_map.get("fleet_master") == "deploy/Dockerfile.fleet"
    assert marker_map.get("agent_node_0") == "deploy/Dockerfile.fleet"
    assert marker_map.get("agent_node_1") == "deploy/Dockerfile.fleet"
