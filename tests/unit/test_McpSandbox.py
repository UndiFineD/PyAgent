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
r"""Unit tests for McpSandbox: env sanitisation, path validation, subprocess lifecycle.

All 10 tests are RED-phase: collection fails with ``ModuleNotFoundError``
because ``src.mcp`` does not yet exist.  That is the expected failure.
"""

from __future__ import annotations

import asyncio
import hashlib
import os
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.mcp.exceptions import McpPathForbidden, McpPinMismatch, McpSandboxError, McpSecretNotFound
from src.mcp.McpSandbox import McpSandbox
from src.mcp.McpServerConfig import McpServerConfig

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_config(
    *,
    command: list[str] | None = None,
    env_vars: dict[str, str] | None = None,
    secret_refs: list[str] | None = None,
    allowed_paths: list[str] | None = None,
    sha256_pin: str | None = None,
) -> McpServerConfig:
    """Build a McpServerConfig suitable for McpSandbox unit tests.

    Args:
        command: Server command list; defaults to a safe sentinel path.
        env_vars: Literal env vars to inject; defaults to empty.
        secret_refs: Names of secrets to copy from os.environ; defaults to empty.
        allowed_paths: Filesystem paths the server may access; defaults to ["/workspace"].
        sha256_pin: Optional expected SHA-256 hex of the binary; defaults to None.

    Returns:
        A McpServerConfig with test-safe defaults.

    """
    return McpServerConfig(
        name="sandbox-test",
        command=command or ["/usr/bin/node", "server.js"],
        env_vars=env_vars or {},
        secret_refs=secret_refs or [],
        allowed_paths=allowed_paths or ["/workspace"],
        allowed_hosts=[],
        timeout_seconds=5.0,
        restart_policy="on-failure",
        sha256_pin=sha256_pin,
    )


# ---------------------------------------------------------------------------
# TC-SBX-01  build_env includes PATH and LANG (safe system vars)
# ---------------------------------------------------------------------------


def test_build_env_inherits_allowed_vars() -> None:
    """build_env() includes PATH in the sanitised environment.

    PATH must always be present (set to the binary directory) so that the
    child process can locate its own dependencies.  LANG is an example of a
    safe locale var that implementations may optionally inherit.
    """
    sandbox = McpSandbox()
    config = _make_config(command=["/usr/bin/node", "server.js"])

    env, _masked = sandbox.build_env(config)

    assert "PATH" in env, f"Sanitised env is missing PATH; got keys: {list(env.keys())}"
    # PATH must point to (or include) the binary's directory.
    binary_dir = str(Path("/usr/bin/node").parent)
    assert binary_dir in env["PATH"], f"Expected binary dir '{binary_dir}' in PATH '{env['PATH']}'"


# ---------------------------------------------------------------------------
# TC-SBX-02  build_env strips dangerous host vars (HOME, AWS credentials)
# ---------------------------------------------------------------------------


def test_build_env_strips_disallowed_vars() -> None:
    """build_env() must NOT include HOME or AWS_SECRET_ACCESS_KEY in the sanitised env.

    These represent host-filesystem leak and credential-leak risks respectively.
    The sandbox must start from an empty base and never blindly copy os.environ.
    """
    sandbox = McpSandbox()
    config = _make_config(env_vars={})

    injected_secrets = {
        "HOME": "/root",
        "AWS_SECRET_ACCESS_KEY": "s3cr3t",
        "AWS_ACCESS_KEY_ID": "AKIAIOSFODNN7EXAMPLE",
    }
    with patch.dict(os.environ, injected_secrets, clear=False):
        env, _masked = sandbox.build_env(config)

    assert "HOME" not in env, f"HOME must be stripped from sandbox env; found: {env.get('HOME')}"
    assert "AWS_SECRET_ACCESS_KEY" not in env, "AWS_SECRET_ACCESS_KEY must be stripped from sandbox env"
    assert "AWS_ACCESS_KEY_ID" not in env, "AWS_ACCESS_KEY_ID must be stripped from sandbox env"


# ---------------------------------------------------------------------------
# TC-SBX-03  masked_env replaces secret values with [REDACTED]
# ---------------------------------------------------------------------------


def test_masked_env_replaces_secrets_with_redacted() -> None:
    """build_env() returns a masked env where secret_refs values are [REDACTED].

    The live env returned in tuple position 0 must contain the real value while
    the masked env in position 1 must show '[REDACTED]' for the same key.
    """
    real_api_key = "sk-real-key-do-not-log"
    sandbox = McpSandbox()
    config = _make_config(secret_refs=["API_KEY"])

    with patch.dict(os.environ, {"API_KEY": real_api_key}, clear=False):
        env, masked_env = sandbox.build_env(config)

    assert env.get("API_KEY") == real_api_key, (
        f"Live env should contain the real API_KEY value; got: {env.get('API_KEY')}"
    )
    assert masked_env.get("API_KEY") == "[REDACTED]", (
        f"Masked env must show '[REDACTED]' for API_KEY; got: {masked_env.get('API_KEY')}"
    )


# ---------------------------------------------------------------------------
# TC-SBX-04  validate_path allows declared paths
# ---------------------------------------------------------------------------


def test_validate_path_allows_declared_paths(tmp_path: Path) -> None:
    """validate_path() returns True (or does not raise) for paths under allowed_paths.

    Creates a real temporary file so symlink resolution produces a valid
    absolute path, then asserts the sandbox permits access to it.
    """
    allowed_dir = tmp_path / "workspace"
    allowed_dir.mkdir()
    test_file = allowed_dir / "file.txt"
    test_file.write_text("content")

    sandbox = McpSandbox()
    config = _make_config(allowed_paths=[str(allowed_dir)])

    # Must not raise and must return a truthy value.
    result = sandbox.validate_path(str(test_file), config)
    assert result is not False, f"validate_path should allow '{test_file}' under allowed dir '{allowed_dir}'"


# ---------------------------------------------------------------------------
# TC-SBX-05  validate_path blocks undeclared paths
# ---------------------------------------------------------------------------


def test_validate_path_blocks_undeclared_paths(tmp_path: Path) -> None:
    """validate_path() raises McpPathForbidden for paths outside allowed_paths.

    /etc/passwd is a canonical example of a sensitive path that should be
    blocked when allowed_paths is set to a workspace directory only.
    """
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    sandbox = McpSandbox()
    config = _make_config(allowed_paths=[str(workspace)])

    with pytest.raises(McpPathForbidden):
        sandbox.validate_path("/etc/passwd", config)


# ---------------------------------------------------------------------------
# TC-SBX-06  validate_path blocks symlink escape
# ---------------------------------------------------------------------------


def test_validate_path_blocks_symlink_escape(tmp_path: Path) -> None:
    """validate_path() blocks path-traversal attacks using .. and symlinks.

    A path like /workspace/../etc/passwd must be resolved to its canonical
    form (/etc/passwd) before the allowlist check, blocking the escape.
    """
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    # Path traversal attempt: start inside workspace then escape via ..
    traversal = str(workspace) + "/../etc/passwd"

    sandbox = McpSandbox()
    config = _make_config(allowed_paths=[str(workspace)])

    with pytest.raises(McpPathForbidden):
        sandbox.validate_path(traversal, config)


# ---------------------------------------------------------------------------
# TC-SBX-07  spawn passes sanitised env to subprocess (not os.environ)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_spawn_uses_sanitised_env() -> None:
    """spawn() passes env=build_env(config) to asyncio.create_subprocess_exec, not os.environ.

    A secret injected into os.environ but NOT listed in secret_refs or env_vars
    must not appear in the env dict passed to the subprocess.
    """
    sandbox = McpSandbox()
    config = _make_config(
        command=["/usr/bin/node", "server.js"],
        env_vars={"DECLARED_VAR": "hello"},
        secret_refs=[],
    )

    captured_env: dict[str, str] = {}
    mock_process = MagicMock()
    mock_process.returncode = None

    async def fake_create_subprocess_exec(*args: object, **kwargs: object) -> MagicMock:
        """Capture subprocess env arg and return a fake process."""
        captured_env.update(kwargs.get("env", {}))
        return mock_process

    with patch.dict(os.environ, {"SECRET_NOT_DECLARED": "should-not-appear"}, clear=False):
        with patch("asyncio.create_subprocess_exec", side_effect=fake_create_subprocess_exec):
            await sandbox.spawn(config)

    assert "SECRET_NOT_DECLARED" not in captured_env, "Undeclared host env var must not be forwarded to subprocess"
    assert "DECLARED_VAR" in captured_env, "Declared env_var must be present in subprocess env"


# ---------------------------------------------------------------------------
# TC-SBX-08  terminate sends SIGTERM then SIGKILL after timeout
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_terminate_sends_sigterm_then_sigkill() -> None:
    """terminate() sends SIGTERM first; if process does not exit within 5 s, sends SIGKILL.

    Uses a mock process that never exits so the timeout fires and SIGKILL
    (process.kill()) is subsequently called.
    """
    sandbox = McpSandbox()

    mock_process = MagicMock()
    mock_process.returncode = None

    sigterm_sent = False
    sigkill_sent = False

    def record_terminate() -> None:
        """Record SIGTERM delivery."""
        nonlocal sigterm_sent
        sigterm_sent = True

    def record_kill() -> None:
        """Record SIGKILL delivery."""
        nonlocal sigkill_sent
        sigkill_sent = True
        mock_process.returncode = -9  # simulate process exit after kill

    async def wait_that_never_returns() -> int:
        """Simulate process that ignores SIGTERM and never exits."""
        await asyncio.sleep(60)  # longer than any test timeout
        return 0

    mock_process.terminate = record_terminate
    mock_process.kill = record_kill
    mock_process.wait = AsyncMock(side_effect=asyncio.TimeoutError)  # first wait times out

    # Patch asyncio.wait_for to trigger the timeout quickly.
    original_wait_for = asyncio.wait_for

    call_count = 0

    async def fast_wait_for(coro: object, timeout: float) -> int:
        """Replace wait_for: first call times out (SIGTERM wait); second returns 0."""
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # Cancel the coroutine to avoid resource leaks.
            if hasattr(coro, "close"):
                coro.close()  # type: ignore[union-attr]
            raise asyncio.TimeoutError
        return await original_wait_for(coro, timeout=timeout)

    with patch("asyncio.wait_for", side_effect=fast_wait_for):
        mock_process.wait = AsyncMock(return_value=0)  # second wait returns immediately
        await sandbox.terminate(mock_process)

    assert sigterm_sent, "SIGTERM (process.terminate()) was never called"
    assert sigkill_sent, "SIGKILL (process.kill()) was never sent after SIGTERM timeout"


# ---------------------------------------------------------------------------
# TC-SBX-09  spawn raises McpSandboxError when command is not found
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_spawn_raises_on_missing_command() -> None:
    """spawn() raises McpSandboxError when the first command element does not exist.

    When asyncio.create_subprocess_exec raises FileNotFoundError (e.g. binary
    not on PATH), McpSandbox must translate this into McpSandboxError so
    callers get a domain-specific exception.
    """
    sandbox = McpSandbox()
    config = _make_config(command=["nonexistent-binary-xyz-abc", "arg"])

    with patch(
        "asyncio.create_subprocess_exec",
        side_effect=FileNotFoundError("No such file: nonexistent-binary-xyz-abc"),
    ):
        with pytest.raises(McpSandboxError):
            await sandbox.spawn(config)


# ---------------------------------------------------------------------------
# TC-SBX-10  sha256 pin mismatch raises McpPinMismatch
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_sha256_pin_validation() -> None:
    """spawn() raises McpPinMismatch when the binary SHA-256 does not match sha256_pin.

    Creates a temporary file, computes its real SHA-256, then asserts that
    providing a *different* pin (all-zeros) causes spawn() to raise McpPinMismatch
    BEFORE launching any subprocess.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".js") as tmp:
        tmp.write(b"console.log('hello')")
        tmp_path_str = tmp.name

    real_hash = hashlib.sha256(Path(tmp_path_str).read_bytes()).hexdigest()
    wrong_pin = "0" * 64  # definitely not the real hash

    assert wrong_pin != real_hash, "Test setup error: wrong_pin accidentally matched real hash"

    sandbox = McpSandbox()
    config = _make_config(command=[tmp_path_str, "arg"], sha256_pin=wrong_pin)

    # spawn() should raise McpPinMismatch before calling asyncio.create_subprocess_exec.
    with patch("asyncio.create_subprocess_exec") as mock_exec:
        with pytest.raises(McpPinMismatch):
            await sandbox.spawn(config)

    mock_exec.assert_not_called()
