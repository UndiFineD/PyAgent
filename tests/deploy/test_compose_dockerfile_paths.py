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

"""RED-phase contract tests for compose Dockerfile path references.

These tests intentionally codify expected post-fix behavior. They should fail
against the current broken compose path state and pass after @6code applies the
path correction and Dockerfile addition.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPOSE_FILE = REPO_ROOT / "deploy" / "compose.yaml"
EXPECTED_DOCKERFILE = "deploy/Dockerfile.pyagent"


def _load_compose_contract() -> dict[str, Any]:
    """Load minimal compose contract data needed for these tests.

    Returns:
        dict[str, Any]: Parsed compose object with at least
            services.pyagent.build.context and
            services.pyagent.build.dockerfile.

    """
    assert COMPOSE_FILE.exists(), f"Missing compose file: {COMPOSE_FILE}"

    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError:
        return _fallback_parse_compose_contract(COMPOSE_FILE.read_text(encoding="utf-8"))

    loaded = yaml.safe_load(COMPOSE_FILE.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict), "Compose file must parse into a mapping"
    return loaded


def _fallback_parse_compose_contract(compose_text: str) -> dict[str, Any]:
    """Parse required compose values without external YAML dependency.

    Args:
        compose_text: Raw compose YAML file content.

    Returns:
        dict[str, Any]: Minimal compose-like mapping with pyagent build fields.

    """
    context: str | None = None
    dockerfile: str | None = None
    in_services = False
    in_pyagent = False
    in_build = False

    for raw_line in compose_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        if line.startswith("services:"):
            in_services = True
            in_pyagent = False
            in_build = False
            continue

        if in_services and line.startswith("  pyagent:"):
            in_pyagent = True
            in_build = False
            continue

        if in_pyagent and line.startswith("    build:"):
            in_build = True
            continue

        if in_build and line.startswith("      context:"):
            context = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            continue

        if in_build and line.startswith("      dockerfile:"):
            dockerfile = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            continue

        # Leave the build block when indentation falls back to pyagent scope.
        if in_build and line.startswith("    ") and not line.startswith("      "):
            in_build = False

    assert context is not None, "Unable to parse services.pyagent.build.context"
    assert dockerfile is not None, "Unable to parse services.pyagent.build.dockerfile"

    return {
        "services": {
            "pyagent": {
                "build": {
                    "context": context,
                    "dockerfile": dockerfile,
                }
            }
        }
    }


def _resolve_pyagent_dockerfile_path(compose_obj: dict[str, Any]) -> Path:
    """Resolve the compose pyagent Dockerfile path to an absolute repository path.

    Args:
        compose_obj: Parsed compose object.

    Returns:
        Path: Absolute path of the referenced Dockerfile.

    """
    services = compose_obj.get("services")
    assert isinstance(services, dict), "Compose file must include 'services' mapping"
    assert "pyagent" in services, "Compose file must define services.pyagent"

    pyagent = services["pyagent"]
    assert isinstance(pyagent, dict), "services.pyagent must be a mapping"
    build = pyagent.get("build")
    assert isinstance(build, dict), "services.pyagent.build must be a mapping"

    context_value = build.get("context")
    dockerfile_value = build.get("dockerfile")
    assert isinstance(context_value, str), "services.pyagent.build.context must be a string"
    assert isinstance(dockerfile_value, str), "services.pyagent.build.dockerfile must be a string"

    context_dir = (COMPOSE_FILE.parent / context_value).resolve()
    return (context_dir / dockerfile_value).resolve()


def test_compose_reference_contract_uses_expected_pyagent_dockerfile_path() -> None:
    """Assert compose pyagent service uses the expected Dockerfile path contract.

    This must fail in red phase until `deploy/compose.yaml` points to
    `deploy/Dockerfile.pyagent`.
    """
    compose_obj = _load_compose_contract()

    services = compose_obj.get("services", {})
    pyagent = services.get("pyagent", {}) if isinstance(services, dict) else {}
    build = pyagent.get("build", {}) if isinstance(pyagent, dict) else {}
    actual_dockerfile = build.get("dockerfile") if isinstance(build, dict) else None

    assert actual_dockerfile == EXPECTED_DOCKERFILE, (
        "Compose contract violation for services.pyagent.build.dockerfile: "
        f"expected '{EXPECTED_DOCKERFILE}', got '{actual_dockerfile}'."
    )


def test_compose_referenced_dockerfile_path_exists_in_repository() -> None:
    """Assert the Dockerfile referenced by compose exists on disk.

    This verifies real filesystem behavior and must fail when compose points to
    a missing Dockerfile path.
    """
    compose_obj = _load_compose_contract()
    resolved_path = _resolve_pyagent_dockerfile_path(compose_obj)

    assert resolved_path.exists(), (
        "Compose path contract violation: referenced Dockerfile does not exist. "
        f"compose_file='{COMPOSE_FILE}', resolved_dockerfile='{resolved_path}'."
    )
