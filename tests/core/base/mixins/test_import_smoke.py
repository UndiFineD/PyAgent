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

"""Import smoke tests for canonical and legacy mixin paths."""

from __future__ import annotations

import subprocess
import sys


def _run_import_smoke(script_body: str) -> subprocess.CompletedProcess[str]:
    """Run a clean-interpreter import smoke script.

    Args:
        script_body: Python script snippet executed with python -c.

    Returns:
        Completed process containing stdout and stderr.

    """
    return subprocess.run(
        [sys.executable, "-c", script_body],
        check=False,
        capture_output=True,
        text=True,
    )


def test_import_smoke_canonical_mixins() -> None:
    """Require canonical mixin package import to succeed in a clean process."""
    script = (
        "from src.core.base.mixins import AuditMixin, SandboxMixin, ReplayMixin;"
        "print(AuditMixin.__name__, SandboxMixin.__name__, ReplayMixin.__name__)"
    )
    result = _run_import_smoke(script)
    assert result.returncode == 0, result.stderr
    assert "AuditMixin SandboxMixin ReplayMixin" in result.stdout


def test_import_smoke_legacy_shims() -> None:
    """Require legacy shim import paths to remain importable."""
    script = (
        "from src.core.audit.AuditTrailMixin import AuditTrailMixin;"
        "from src.core.sandbox.SandboxMixin import SandboxMixin;"
        "from src.core.replay.ReplayMixin import ReplayMixin;"
        "print(AuditTrailMixin.__name__, SandboxMixin.__name__, ReplayMixin.__name__)"
    )
    result = _run_import_smoke(script)
    assert result.returncode == 0, result.stderr
    assert "AuditMixin SandboxMixin ReplayMixin" in result.stdout
