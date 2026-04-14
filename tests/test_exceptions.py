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

"""Coverage tests for core exception modules."""

from src.core.audit.exceptions import AuditTrailError
from src.core.audit.exceptions import validate as audit_validate
from src.core.fuzzing.exceptions import FuzzingError
from src.core.n8nbridge.exceptions import N8nBridgeError
from src.core.replay.exceptions import ReplayError
from src.core.resilience.CircuitBreakerState import CircuitState
from src.core.resilience.exceptions import CircuitOpenError
from src.core.resilience.exceptions import validate as resilience_validate
from src.core.universal.exceptions import UniversalShellError
from src.core.universal.exceptions import validate as universal_validate


def test_exception_modules_are_importable() -> None:
    """Core exception modules should expose base error types."""
    assert issubclass(AuditTrailError, Exception)
    assert issubclass(FuzzingError, Exception)
    assert issubclass(N8nBridgeError, Exception)
    assert issubclass(ReplayError, Exception)
    assert issubclass(UniversalShellError, Exception)


def test_exception_module_validate_hooks() -> None:
    """Modules with explicit validate hooks should return True."""
    assert audit_validate() is True
    assert resilience_validate() is True
    assert universal_validate() is True


def test_circuit_open_error_carries_provider_and_state() -> None:
    """CircuitOpenError should retain provider context and state."""
    err = CircuitOpenError(provider_key="provider-a", state=CircuitState.OPEN)
    assert err.provider_key == "provider-a"
    assert err.state is CircuitState.OPEN
