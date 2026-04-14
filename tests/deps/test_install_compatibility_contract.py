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

"""Red-phase tests for install compatibility and requirements chain contracts."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_requirements_install_contract_remains_supported() -> None:
    """Install script should keep requirements install and parity preflight contracts."""
    install_text = (REPO_ROOT / "install.ps1").read_text(encoding="utf-8")

    assert "pip install --prefer-binary -r requirements.txt" in install_text
    assert "pip install --prefer-binary -r requirements-ci.txt" in install_text
    assert "python scripts/deps/check_dependency_parity.py --check" in install_text


def test_requirements_ci_chain_still_includes_requirements_txt() -> None:
    """CI requirements chain should include runtime requirements and generation guidance."""
    requirements_ci = (REPO_ROOT / "requirements-ci.txt").read_text(encoding="utf-8")

    assert "-r requirements.txt" in requirements_ci
    assert "generated from pyproject.toml" in requirements_ci.lower()
