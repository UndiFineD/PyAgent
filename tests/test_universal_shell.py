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

"""Core contract tests for the Universal Shell facade public surface."""

from __future__ import annotations

import importlib
from typing import Any

import pytest


def _import_or_fail(module_name: str) -> Any:
    """Import a module or fail with a red-phase behavioral message.

    Args:
        module_name: Fully-qualified module path to import.

    Returns:
        Imported module object.

    """
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        pytest.fail(
            (
                f"Missing implementation for facade behavior contract: {module_name}. "
                "This red-phase failure is expected before @6code implementation."
            ),
            pytrace=False,
        )


def test_public_exports_include_stable_symbols() -> None:
    """Verify the facade exports the stable contract symbols.

    The contract is defined in the design artifact and must be available from
    the package root once implemented.
    """
    facade = _import_or_fail("src.core.universal")

    required = {
        "TaskEnvelope",
        "RoutingDecision",
        "DispatchResult",
        "UniversalIntentRouter",
        "UniversalCoreRegistry",
        "UniversalAgentShell",
        "UniversalShellError",
        "EnvelopeValidationError",
        "RoutingContractError",
        "CoreRegistrationError",
        "CoreNotRegisteredError",
        "CoreExecutionError",
        "CoreTimeoutError",
        "LegacyDispatchError",
    }

    missing = sorted(symbol for symbol in required if not hasattr(facade, symbol))
    assert not missing, f"Facade exports are incomplete: {missing}"


def test_exception_hierarchy_matches_design_contract() -> None:
    """Verify exception hierarchy follows the defined universal shell contract."""
    exc_mod = _import_or_fail("src.core.universal.exceptions")

    root_error = exc_mod.UniversalShellError
    leaf_errors = [
        exc_mod.EnvelopeValidationError,
        exc_mod.RoutingContractError,
        exc_mod.CoreRegistrationError,
        exc_mod.CoreNotRegisteredError,
        exc_mod.CoreExecutionError,
        exc_mod.CoreTimeoutError,
        exc_mod.LegacyDispatchError,
    ]

    for error_type in leaf_errors:
        assert issubclass(error_type, root_error), (
            f"{error_type.__name__} must inherit UniversalShellError"
        )


def test_task_envelope_and_dispatch_result_have_required_fields() -> None:
    """Verify dataclass-like contract fields exist on key facade value objects."""
    router_mod = _import_or_fail("src.core.universal.UniversalIntentRouter")
    shell_mod = _import_or_fail("src.core.universal.UniversalAgentShell")

    envelope = router_mod.TaskEnvelope(
        task_id="task-1",
        intent="summarize",
        payload={"message": "hello"},
        metadata={"source": "unit-test"},
    )
    result = shell_mod.DispatchResult(
        route="legacy",
        intent="unknown",
        payload={"ok": False},
        fallback_reason="core_missing",
    )

    for field_name in ("task_id", "intent", "payload", "metadata"):
        assert hasattr(envelope, field_name), f"TaskEnvelope missing field: {field_name}"

    for field_name in ("route", "intent", "payload", "fallback_reason"):
        assert hasattr(result, field_name), f"DispatchResult missing field: {field_name}"
