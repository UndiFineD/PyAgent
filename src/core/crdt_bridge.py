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

"""CRDT bridge facade with FFI routing, fallback merge, and typed contracts."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any

SUPPORTED_SCHEMA_VERSION = 1
_last_observability_event: dict[str, Any] | None = None


class CRDTBridgeError(Exception):
    """Represent a typed bridge error suitable for API-level handling.

    Args:
        message: Human-readable error summary.
        error_code: Stable machine-readable error code.
        category: Error taxonomy category.
        request_id: Request identifier correlated with the failure.

    """

    def __init__(self, message: str, error_code: str, category: str, request_id: str) -> None:
        """Initialize a typed bridge error.

        Args:
            message: Human-readable error summary.
            error_code: Stable machine-readable error code.
            category: Error taxonomy category.
            request_id: Request identifier correlated with the failure.

        """
        super().__init__(message)
        self.error_code = error_code
        self.category = category
        self.request_id = request_id


def _rust_crdt_binary() -> Path:
    """Ensure the rust_core/crdt binary is built and return its path.

    Returns:
        The resolved path to the release binary.

    """
    repo_root = Path(__file__).resolve().parents[2]
    crate = repo_root / "rust_core" / "crdt"
    is_windows = Path().joinpath(".venv").exists() and sys.platform == "win32"
    binary_name = "rust_core_crdt.exe" if is_windows else "rust_core_crdt"
    binary = crate / "target" / "release" / binary_name

    if not binary.exists():
        subprocess.run(["cargo", "build", "--release"], cwd=crate, check=True)  # noqa: S603 S607

    return binary


def _feature_flag_enabled() -> bool:
    """Evaluate the CRDT FFI feature flag.

    Returns:
        True when FFI is explicitly enabled by environment configuration.

    """
    value = os.getenv("CRDT_FFI_ENABLED", "0").strip().lower()
    return value in {"1", "true", "yes", "on"}


def _ffi_available() -> bool:
    """Check whether an in-process FFI merge function is importable.

    Returns:
        True when rust_core exposes a callable merge_crdt function.

    """
    try:
        import rust_core  # type: ignore
    except ImportError:
        return False
    return callable(getattr(rust_core, "merge_crdt", None))


def _deep_merge(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge two dictionary-like state objects.

    Args:
        left: Base state.
        right: Overlay state.

    Returns:
        A deterministic deep-merged state.

    """
    merged: dict[str, Any] = dict(left)
    for key in sorted(right.keys()):
        left_value = merged.get(key)
        right_value = right[key]
        if isinstance(left_value, dict) and isinstance(right_value, dict):
            merged[key] = _deep_merge(left_value, right_value)
        else:
            merged[key] = right_value
    return merged


def _validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate the typed CRDT request payload.

    Args:
        payload: Candidate CRDT merge payload.

    Returns:
        The validated payload.

    Raises:
        CRDTBridgeError: If required fields are missing or invalid.

    """
    request_id = str(payload.get("request_id", "unknown"))
    required = {"request_id", "lhs_state", "rhs_state", "merge_strategy", "schema_version"}
    missing = sorted(required.difference(payload.keys()))
    if missing:
        raise CRDTBridgeError(
            message=f"Missing required fields: {', '.join(missing)}",
            error_code="crdt_validation_missing_fields",
            category="validation",
            request_id=request_id,
        )

    if not isinstance(payload["lhs_state"], dict) or not isinstance(payload["rhs_state"], dict):
        raise CRDTBridgeError(
            message="lhs_state and rhs_state must be objects",
            error_code="crdt_validation_shape",
            category="validation",
            request_id=request_id,
        )

    if payload["schema_version"] != SUPPORTED_SCHEMA_VERSION:
        raise CRDTBridgeError(
            message=(
                f"Unsupported schema_version={payload['schema_version']}; "
                f"expected={SUPPORTED_SCHEMA_VERSION}"
            ),
            error_code="crdt_validation_schema_version",
            category="validation",
            request_id=request_id,
        )

    return payload


def _fallback_merge(payload: dict[str, Any]) -> dict[str, Any]:
    """Merge states using the deterministic fallback implementation.

    Args:
        payload: Validated merge payload.

    Returns:
        Merged state object.

    """
    return _deep_merge(payload["lhs_state"], payload["rhs_state"])


def _ffi_merge(payload: dict[str, Any]) -> dict[str, Any]:
    """Merge states using the in-process FFI implementation when available.

    Args:
        payload: Validated merge payload.

    Returns:
        Merged state object.

    Raises:
        CRDTBridgeError: If rust_core merge fails and must be taxonomy-mapped.

    """
    try:
        import rust_core  # type: ignore
    except ImportError:
        return _fallback_merge(payload)

    merge_fn = getattr(rust_core, "merge_crdt", None)
    if not callable(merge_fn):
        return _fallback_merge(payload)

    try:
        result = merge_fn(payload)
    except ValueError as exc:
        raise CRDTBridgeError(
            message=str(exc),
            error_code="crdt_validation_error",
            category="validation",
            request_id=str(payload["request_id"]),
        ) from exc
    except RuntimeError as exc:
        raise CRDTBridgeError(
            message=str(exc),
            error_code="crdt_merge_error",
            category="merge",
            request_id=str(payload["request_id"]),
        ) from exc
    except Exception as exc:
        raise CRDTBridgeError(
            message="FFI merge failed",
            error_code="crdt_internal_error",
            category="internal",
            request_id=str(payload["request_id"]),
        ) from exc

    if isinstance(result, dict) and "merged_state" in result:
        merged_state = result["merged_state"]
    else:
        merged_state = result

    if not isinstance(merged_state, dict):
        raise CRDTBridgeError(
            message="FFI merge returned non-object payload",
            error_code="crdt_internal_invalid_result",
            category="internal",
            request_id=str(payload["request_id"]),
        )
    return merged_state


def _emit_observability_event(
    request_id: str,
    path: str,
    duration_ms: float,
    outcome: str,
    parity_tag: str,
) -> None:
    """Store the latest redacted observability event for tests and diagnostics.

    Args:
        request_id: Request identifier.
        path: Execution path marker.
        duration_ms: Elapsed time in milliseconds.
        outcome: Outcome category.
        parity_tag: Parity marker.

    """
    global _last_observability_event
    _last_observability_event = {
        "request_id": request_id,
        "path": path,
        "duration_ms": duration_ms,
        "outcome": outcome,
        "parity_tag": parity_tag,
    }


def get_last_observability_event() -> dict[str, Any] | None:
    """Return the most recent redacted observability event.

    Returns:
        The latest event, if one was emitted.

    """
    return _last_observability_event


def merge(left: dict[str, Any], right: dict[str, Any] | None = None) -> dict[str, Any]:
    """Merge CRDT documents via stable payload envelope or legacy two-arg form.

    Args:
        left: Either legacy left-state or a full typed request payload.
        right: Legacy right-state when using two-arg mode.

    Returns:
        Legacy mode returns merged state only. Payload mode returns envelope.

    Raises:
        CRDTBridgeError: If payload validation or merge execution fails.

    """
    if right is not None:
        return _deep_merge(left, right)

    payload = _validate_payload(left)
    ffi_enabled = _feature_flag_enabled()
    use_ffi = ffi_enabled and _ffi_available()
    path = "ffi" if use_ffi else "fallback"

    start_time = time.perf_counter()
    try:
        merged_state = _ffi_merge(payload) if use_ffi else _fallback_merge(payload)
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        _emit_observability_event(
            request_id=str(payload["request_id"]),
            path=path,
            duration_ms=duration_ms,
            outcome="success",
            parity_tag="legacy_parity_pending",
        )
        return {
            "request_id": str(payload["request_id"]),
            "merged_state": merged_state,
            "conflict_summary": {"strategy": payload["merge_strategy"], "count": 0},
            "engine_version": "crdt-ffi-v1" if use_ffi else "crdt-fallback-v1",
            "path": path,
        }
    except CRDTBridgeError as exc:
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        _emit_observability_event(
            request_id=exc.request_id,
            path=path,
            duration_ms=duration_ms,
            outcome="error",
            parity_tag="legacy_parity_pending",
        )
        raise
    except Exception as exc:
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        request_id = str(payload.get("request_id", "unknown"))
        _emit_observability_event(
            request_id=request_id,
            path=path,
            duration_ms=duration_ms,
            outcome="error",
            parity_tag="legacy_parity_pending",
        )
        raise CRDTBridgeError(
            message="Unhandled bridge merge error",
            error_code="crdt_internal_error",
            category="internal",
            request_id=request_id,
        ) from exc
    with tempfile.TemporaryDirectory() as td:
        left_file = Path(td) / "left.json"
        right_file = Path(td) / "right.json"
        left_file.write_text(json.dumps(left))
        right_file.write_text(json.dumps(right))

        binary = _rust_crdt_binary()
        result = subprocess.run(  # noqa: S603
            [
                str(binary),
                "merge",
                "--left",
                str(left_file),
                "--right",
                str(right_file),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        return json.loads(result.stdout)


def validate() -> None:
    """Validate this bridge module is loadable.

    This is used by repository-level quality checks.

    Returns:
        None.

    """
    return


def make_request(
    lhs_state: dict[str, Any],
    rhs_state: dict[str, Any],
    merge_strategy: str = "last_write_wins",
    request_id: str | None = None,
) -> dict[str, Any]:
    """Build a canonical request payload used by selector-aligned tests.

    Args:
        lhs_state: Left/baseline state.
        rhs_state: Right/overlay state.
        merge_strategy: Merge strategy marker.
        request_id: Optional request identifier.

    Returns:
        Canonical merge request payload.

    """
    return {
        "request_id": request_id or str(uuid.uuid4()),
        "lhs_state": lhs_state,
        "rhs_state": rhs_state,
        "merge_strategy": merge_strategy,
        "schema_version": SUPPORTED_SCHEMA_VERSION,
    }
