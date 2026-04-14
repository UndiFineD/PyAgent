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

"""Compose manifest selection and role-separation contract tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPOSE_CANONICAL = REPO_ROOT / "deploy" / "compose.yaml"
COMPOSE_FLEET = REPO_ROOT / "deploy" / "docker-compose.yaml"


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    """Load YAML file as mapping.

    Args:
        path: Absolute path to YAML file.

    Returns:
        Parsed dictionary mapping.

    """
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError as error:
        raise AssertionError("PyYAML is required for compose file selection tests") from error

    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict), f"YAML file must parse to mapping: {path}"
    return loaded


def _service_names(path: Path) -> set[str]:
    """Return service names for a compose manifest.

    Args:
        path: Compose file path.

    Returns:
        Set of service names.

    """
    compose_obj = _load_yaml_mapping(path)
    services = compose_obj.get("services")
    assert isinstance(services, dict), f"services mapping missing in {path}"
    return set(services)


def test_deploy_directory_keeps_expected_compose_file_set() -> None:
    """Deploy folder must keep both canonical compose manifests for this lane."""
    compose_files = sorted(path.name for path in (REPO_ROOT / "deploy").glob("*compose*.yaml"))
    assert compose_files == ["compose.yaml", "docker-compose.yaml"], (
        "Compose selection contract regression: expected only compose.yaml and docker-compose.yaml, "
        f"got {compose_files}."
    )


def test_canonical_compose_hosts_pyagent_service_and_not_fleet_nodes() -> None:
    """Canonical compose must be dedicated to pyagent runtime, not fleet topology."""
    canonical_services = _service_names(COMPOSE_CANONICAL)

    assert "pyagent" in canonical_services, "compose.yaml must include pyagent service"
    assert "fleet_master" not in canonical_services, "compose.yaml must not include fleet_master service"
    assert "agent_node_0" not in canonical_services, "compose.yaml must not include worker topology"


def test_fleet_compose_hosts_fleet_nodes_and_not_pyagent_service() -> None:
    """Fleet compose must retain fleet services and avoid pyagent runtime service."""
    fleet_services = _service_names(COMPOSE_FLEET)

    assert "fleet_master" in fleet_services, "docker-compose.yaml must include fleet_master"
    assert "agent_node_0" in fleet_services, "docker-compose.yaml must include agent_node_0"
    assert "agent_node_1" in fleet_services, "docker-compose.yaml must include agent_node_1"
    assert "pyagent" not in fleet_services, "docker-compose.yaml must not include pyagent"
