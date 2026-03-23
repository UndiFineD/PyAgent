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
"""Static/structural tests for install.ps1 (prj0000050).

Reads install.ps1 as text and asserts required elements are present.
Does NOT execute the script.
"""

import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
_SCRIPT_PATH = REPO_ROOT / "install.ps1"

# Read file once at module level; guard so content-dependent tests can skip
# gracefully when the file does not yet exist.
try:
    content = _SCRIPT_PATH.read_text(encoding="utf-8")
except FileNotFoundError:
    content = ""

_FILE_MISSING = content == ""


# ---------------------------------------------------------------------------
# 1. File existence
# ---------------------------------------------------------------------------

def test_install_script_exists() -> None:
    """install.ps1 must exist at the repository root."""
    assert _SCRIPT_PATH.exists()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _require_file(func):
    """Decorator: skip the test when install.ps1 does not yet exist."""
    return pytest.mark.skipif(_FILE_MISSING, reason="install.ps1 not yet created")(func)


# ---------------------------------------------------------------------------
# 2. Param block — CmdletBinding + param keyword
# ---------------------------------------------------------------------------

@_require_file
def test_has_cmdletbinding() -> None:
    """Script must declare [CmdletBinding()]."""
    assert "[CmdletBinding()]" in content


@_require_file
def test_has_param_block() -> None:
    """Script must have a param( or param ( block."""
    assert "param(" in content or "param (" in content


@_require_file
def test_has_skiprrust_param() -> None:
    """Script must declare the -SkipRust switch parameter."""
    assert "SkipRust" in content


@_require_file
def test_has_skipweb_param() -> None:
    """Script must declare the -SkipWeb switch parameter."""
    assert "SkipWeb" in content


@_require_file
def test_has_skipdev_param() -> None:
    """Script must declare the -SkipDev switch parameter."""
    assert "SkipDev" in content


@_require_file
def test_has_ci_param() -> None:
    """Script must declare the -CI switch parameter."""
    assert "[switch]$CI" in content or "switch]$CI" in content or "-CI" in content


@_require_file
def test_has_force_param() -> None:
    """Script must declare the -Force switch parameter."""
    assert "Force" in content


# ---------------------------------------------------------------------------
# 3. Get-Help comment block (.SYNOPSIS / .DESCRIPTION)
# ---------------------------------------------------------------------------

@_require_file
def test_has_synopsis() -> None:
    """Script must contain a .SYNOPSIS comment for Get-Help."""
    assert ".SYNOPSIS" in content


@_require_file
def test_has_description() -> None:
    """Script must contain a .DESCRIPTION comment for Get-Help."""
    assert ".DESCRIPTION" in content


# ---------------------------------------------------------------------------
# 4. Required functions
# ---------------------------------------------------------------------------

@_require_file
def test_has_write_status_function() -> None:
    """Script must define a Write-Status helper function."""
    assert "function Write-Status" in content


@_require_file
def test_has_test_prerequisites_function() -> None:
    """Script must define function Test-Prerequisites."""
    assert "function Test-Prerequisites" in content


@_require_file
def test_has_initialize_venv_function() -> None:
    """Script must define function Initialize-Venv."""
    assert "function Initialize-Venv" in content


@_require_file
def test_has_install_python_function() -> None:
    """Script must define function Install-Python."""
    assert "function Install-Python" in content


@_require_file
def test_has_build_rust_function() -> None:
    """Script must define or call Build-Rust."""
    assert "function Build-Rust" in content or "Build-Rust" in content


@_require_file
def test_has_install_scaffold_function() -> None:
    """Script must define function Install-Scaffold."""
    assert "function Install-Scaffold" in content or "Install-Scaffold" in content


@_require_file
def test_has_install_node_function() -> None:
    """Script must define function Install-Node."""
    assert "function Install-Node" in content


@_require_file
def test_has_show_summary_function() -> None:
    """Script must define function Show-Summary."""
    assert "function Show-Summary" in content


# ---------------------------------------------------------------------------
# 5. References to all three requirements files
# ---------------------------------------------------------------------------

@_require_file
def test_references_requirements_txt() -> None:
    """Script must reference requirements.txt."""
    assert "requirements.txt" in content


@_require_file
def test_references_backend_requirements() -> None:
    """Script must reference backend/requirements.txt (forward or backslash)."""
    assert "backend/requirements.txt" in content or "backend\\requirements.txt" in content


@_require_file
def test_references_requirements_ci() -> None:
    """Script must reference requirements-ci.txt (dev/CI tooling tier)."""
    assert "requirements-ci.txt" in content


# ---------------------------------------------------------------------------
# 6. Venv creation and activation
# ---------------------------------------------------------------------------

@_require_file
def test_has_venv_creation() -> None:
    """Script must contain 'python -m venv' to create the virtual environment."""
    assert "python -m venv" in content


@_require_file
def test_has_venv_activate() -> None:
    """Script must reference Activate.ps1 to activate the virtual environment."""
    assert "Activate.ps1" in content


# ---------------------------------------------------------------------------
# 7. Rust build via maturin
# ---------------------------------------------------------------------------

@_require_file
def test_has_maturin() -> None:
    """Script must reference maturin for the Rust PyO3 build step."""
    assert "maturin" in content


@_require_file
def test_has_maturin_develop() -> None:
    """Script must call 'maturin develop' to build the extension."""
    assert "maturin develop" in content


@_require_file
def test_has_rust_core_manifest() -> None:
    """Script must reference rust_core/Cargo.toml for maturin."""
    assert "rust_core/Cargo.toml" in content or "rust_core\\Cargo.toml" in content


# ---------------------------------------------------------------------------
# 8. Frontend npm install
# ---------------------------------------------------------------------------

@_require_file
def test_has_npm_install() -> None:
    """Script must contain 'npm install' for frontend dependency installation."""
    assert "npm install" in content


# ---------------------------------------------------------------------------
# 9. Summary output
# ---------------------------------------------------------------------------

@_require_file
def test_has_summary_complete_message() -> None:
    """Script must output a summary string containing 'PyAgent Install'."""
    assert "PyAgent Install" in content


# ---------------------------------------------------------------------------
# 10. Python version check ≥ 3.12
# ---------------------------------------------------------------------------

@_require_file
def test_has_python_version_check() -> None:
    """Script must enforce Python ≥ 3.12 (hardcoded or via variable)."""
    assert "3.12" in content or "MinPythonVersion" in content or "MinVersion" in content


# ---------------------------------------------------------------------------
# 11. OS guard (Windows-only)
# ---------------------------------------------------------------------------

@_require_file
def test_has_os_guard() -> None:
    """Script must abort on Linux/macOS."""
    assert "$IsLinux" in content or "$IsMacOS" in content


# ---------------------------------------------------------------------------
# 12. ErrorActionPreference
# ---------------------------------------------------------------------------

@_require_file
def test_has_error_action_preference() -> None:
    """Script must set $ErrorActionPreference = 'Stop' for strict error handling."""
    assert "$ErrorActionPreference" in content and "Stop" in content


# ---------------------------------------------------------------------------
# 13. Requires directive
# ---------------------------------------------------------------------------

@_require_file
def test_has_requires_version() -> None:
    """Script must declare #Requires -Version 5.1 or higher."""
    assert "#Requires -Version" in content
