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

"""Generate the committed backend OpenAPI artifact from backend.app only."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPO_ROOT / "docs" / "api" / "openapi" / "backend_openapi.json"


def _canonicalize_openapi_payload(payload: Any) -> str:
    """Return deterministic JSON text for the committed artifact.

    Args:
        payload: JSON-serializable OpenAPI payload.

    Returns:
        str: Canonical JSON text with stable ordering and trailing newline.

    """
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def _load_backend_openapi_payload() -> dict[str, Any]:
    """Load the backend-only OpenAPI payload from the FastAPI app.

    Returns:
        dict[str, Any]: OpenAPI payload produced by ``backend.app``.

    Raises:
        AssertionError: If the imported app does not expose the expected backend schema.

    """
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

    from backend.app import app

    payload = app.openapi()
    assert isinstance(payload, dict), "backend.app.openapi() must return a JSON object payload."
    assert payload.get("info", {}).get("title") == "PyAgent Backend Worker", (
        "backend.app must remain the phase-one OpenAPI authority for the backend worker."
    )
    return payload


def main() -> int:
    """Generate and persist the canonical backend OpenAPI artifact.

    Returns:
        int: Process exit code.

    """
    payload = _load_backend_openapi_payload()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(_canonicalize_openapi_payload(payload), encoding="utf-8")
    print(f"Wrote backend OpenAPI artifact to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
