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

"""Non-goal guardrail tests for compose topology consolidation drift."""

from __future__ import annotations

from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    """Load a YAML file into a mapping.

    Args:
        path: Absolute YAML path.

    Returns:
        Parsed YAML mapping.

    """
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError as error:
        raise AssertionError("PyYAML is required for compose guardrail tests") from error

    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict), f"YAML file must parse to mapping: {path}"
    return loaded


def test_fleet_compose_service_set_remains_three_node_topology() -> None:
    """Fleet compose must keep current 3-node topology in this non-goal lane."""
    manifest = REPO_ROOT / "deploy" / "docker-compose.yaml"
    compose_obj = _load_yaml_mapping(manifest)

    services = compose_obj.get("services")
    assert isinstance(services, dict), "docker-compose.yaml must contain services mapping"

    service_names = set(services)
    expected = {"fleet_master", "agent_node_0", "agent_node_1"}
    assert service_names == expected, (
        "Non-goal guardrail failure: fleet topology changed in missing-compose-dockerfile lane; "
        f"expected {sorted(expected)}, got {sorted(service_names)}."
    )


def test_canonical_compose_service_set_remains_runtime_focused() -> None:
    """Canonical compose must stay runtime-focused with pyagent and ollama only."""
    manifest = REPO_ROOT / "deploy" / "compose.yaml"
    compose_obj = _load_yaml_mapping(manifest)

    services = compose_obj.get("services")
    assert isinstance(services, dict), "compose.yaml must contain services mapping"

    service_names = set(services)
    expected = {"pyagent", "ollama"}
    assert service_names == expected, (
        "Non-goal guardrail failure: compose.yaml service topology drifted; "
        f"expected {sorted(expected)}, got {sorted(service_names)}."
    )
