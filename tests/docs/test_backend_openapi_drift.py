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

"""Red-phase drift contracts for the backend-only OpenAPI artifact lane."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMITTED_BACKEND_OPENAPI_PATH = REPO_ROOT / "docs" / "api" / "openapi" / "backend_openapi.json"
FORBIDDEN_PHASE_ONE_IMPORTS = ("src.github_app", "src.chat.api")


def _canonicalize_openapi_payload(payload: Any) -> str:
    """Return deterministic JSON for semantic drift comparison.

    Args:
        payload: JSON-serializable OpenAPI payload.

    Returns:
        str: Canonical JSON text with stable ordering and trailing newline.

    """
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def _load_committed_backend_openapi() -> dict[str, Any]:
    """Load the committed backend OpenAPI artifact.

    Returns:
        dict[str, Any]: Parsed committed OpenAPI payload.

    Raises:
        AssertionError: If the committed artifact is missing or lacks semantic shape.
        json.JSONDecodeError: If the committed artifact is not valid JSON.

    """
    assert COMMITTED_BACKEND_OPENAPI_PATH.exists(), (
        "Missing committed backend OpenAPI artifact at "
        f"{COMMITTED_BACKEND_OPENAPI_PATH}. @6code must add the generator and commit "
        "the backend-only schema before drift checks can pass."
    )

    payload = json.loads(COMMITTED_BACKEND_OPENAPI_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict), "Committed backend OpenAPI artifact must decode to a JSON object."
    assert payload.get("openapi"), "Committed backend OpenAPI artifact must include the 'openapi' version field."
    assert isinstance(payload.get("paths"), dict) and payload["paths"], (
        "Committed backend OpenAPI artifact must include at least one documented path."
    )
    return payload


def _load_generated_backend_openapi() -> dict[str, Any]:
    """Generate the backend OpenAPI payload in memory from the only allowed app.

    Returns:
        dict[str, Any]: OpenAPI payload produced by ``backend.app``.

    Raises:
        AssertionError: If the generated payload is not the backend worker schema.

    """
    backend_app_module = importlib.import_module("backend.app")
    payload = backend_app_module.app.openapi()

    assert isinstance(payload, dict), "backend.app.openapi() must return a JSON-like dictionary payload."
    assert payload.get("info", {}).get("title") == "PyAgent Backend Worker", (
        "backend.app must remain the phase-one OpenAPI authority for the backend worker."
    )
    return payload


def _fail_on_write(*_args: Any, **_kwargs: Any) -> None:
    """Fail the test if the drift lane attempts to write during read-only verification.

    Returns:
        None.

    Raises:
        AssertionError: Always, because drift verification must stay read-only.

    """
    raise AssertionError("Drift verification must stay read-only and must not write generated artifacts.")


def _assert_backend_openapi_is_in_sync() -> None:
    """Assert that committed and generated backend schemas are semantically identical.

    Returns:
        None.

    Raises:
        AssertionError: If the committed artifact is missing or semantically drifted.

    """
    committed_payload = _load_committed_backend_openapi()
    generated_payload = _load_generated_backend_openapi()

    assert _canonicalize_openapi_payload(committed_payload) == _canonicalize_openapi_payload(generated_payload), (
        "Committed backend OpenAPI artifact drifted from backend.app.openapi(). Regenerate "
        "docs/api/openapi/backend_openapi.json via scripts/generate_backend_openapi.py."
    )


def test_ac_oas_003_committed_backend_artifact_exists_with_semantic_shape() -> None:
    """Verify the committed backend artifact exists with real OpenAPI content.

    Returns:
        None.

    """
    committed_payload = _load_committed_backend_openapi()

    assert committed_payload.get("info", {}).get("title") == "PyAgent Backend Worker"


def test_ac_oas_003_drift_check_is_read_only_and_semantic(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify drift checking remains read-only while comparing semantic schema output.

    Args:
        monkeypatch: Pytest monkeypatch fixture for blocking write paths.

    Returns:
        None.

    """
    monkeypatch.setattr(Path, "write_text", _fail_on_write)
    monkeypatch.setattr(Path, "write_bytes", _fail_on_write)
    monkeypatch.setattr(json, "dump", _fail_on_write)

    _assert_backend_openapi_is_in_sync()


def test_ac_oas_006_drift_lane_imports_backend_app_only() -> None:
    """Verify the drift lane stays scoped to ``backend.app`` in phase one.

    Returns:
        None.

    """
    generated_payload = _load_generated_backend_openapi()

    assert "backend.app" in sys.modules
    for forbidden_module in FORBIDDEN_PHASE_ONE_IMPORTS:
        assert forbidden_module not in sys.modules, (
            f"Phase-one drift lane must not import excluded FastAPI surface: {forbidden_module}"
        )
    assert generated_payload.get("paths"), "backend.app.openapi() must expose backend paths for drift comparison."
