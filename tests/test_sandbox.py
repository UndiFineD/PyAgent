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

"""Tests for src.core.sandbox — agent-execution-sandbox (TDD red phase).

All 19 tests in this module are expected to FAIL before implementation.
The failure mode in the red phase is ModuleNotFoundError / ImportError arising
from the top-level import block below — src.core.sandbox does not yet exist.
"""

from __future__ import annotations

import os
import uuid
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Module under test — NOT YET IMPLEMENTED.  This import is intentionally left
# at module level so that pytest's collection phase emits ModuleNotFoundError,
# confirming all 19 tests are in the red phase before @6code implements the
# sandbox package.
# ---------------------------------------------------------------------------
from src.core.sandbox import (  # type: ignore[import]  # noqa: E402
    SandboxConfig,
    SandboxedStorageTransaction,
    SandboxMixin,
    SandboxViolationError,
)

# ===========================================================================
# Unit tests — U1 through U9
# ===========================================================================


def test_sandbox_config_from_strings_valid() -> None:
    """SandboxConfig.from_strings() converts string paths and stores an explicit agent_id.

    Verifies that allowed_paths contains Path objects (not raw strings) and that an
    explicitly supplied agent_id is preserved unchanged.
    """
    config = SandboxConfig.from_strings(["/tmp/a"], ["api.example.com"], agent_id="my-id")
    assert config.allowed_paths == [Path("/tmp/a")]
    assert config.allowed_hosts == ["api.example.com"]
    assert config.agent_id == "my-id"
    assert config.allow_all_hosts is False


def test_sandbox_config_from_strings_auto_uuid() -> None:
    """SandboxConfig.from_strings() auto-generates a valid UUID v4 when agent_id is omitted.

    Verifies the field is non-empty and round-trips through uuid.UUID without error.
    """
    config = SandboxConfig.from_strings(["/tmp/b"], [])
    assert config.agent_id  # non-empty string
    parsed = uuid.UUID(config.agent_id)  # must not raise ValueError
    assert str(parsed) == config.agent_id


def test_validate_path_in_scope_passes(tmp_path: Path) -> None:
    """SandboxedStorageTransaction._validate_path() does not raise for a path inside allowed_paths.

    A path that is a descendant of the single allowed root must pass validation silently.
    """
    config = SandboxConfig.from_strings([str(tmp_path)], [])
    tx = SandboxedStorageTransaction(sandbox=config)
    # Should not raise — nested path is inside tmp_path
    tx._validate_path(tmp_path / "subdir" / "file.txt")


def test_validate_path_out_of_scope_raises(tmp_path: Path) -> None:
    """SandboxedStorageTransaction._validate_path() raises SandboxViolationError for a path outside allowed_paths.

    The err.resource attribute must contain the resolved form of the rejected path string.
    """
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    config = SandboxConfig.from_strings([str(allowed)], [])
    tx = SandboxedStorageTransaction(sandbox=config)
    outside = tmp_path / "outside" / "file.txt"
    with pytest.raises(SandboxViolationError) as exc_info:
        tx._validate_path(outside)
    assert str(outside.resolve()) in exc_info.value.resource


def test_validate_path_exact_boundary_passes(tmp_path: Path) -> None:
    """SandboxedStorageTransaction._validate_path() does not raise when path equals allowed_paths[0] exactly.

    The allowed root directory itself must be accepted as a valid target (inclusive boundary).
    """
    config = SandboxConfig.from_strings([str(tmp_path)], [])
    tx = SandboxedStorageTransaction(sandbox=config)
    # Exact boundary — the allowed root itself is valid
    tx._validate_path(tmp_path)


def test_sandbox_violation_error_attributes() -> None:
    """SandboxViolationError stores resource and reason and formats the message correctly.

    Verifies that .resource and .reason attributes are set, the string representation
    contains the expected prefix, and the class is a RuntimeError subclass.
    """
    err = SandboxViolationError(resource="/bad/path", reason="test reason")
    assert err.resource == "/bad/path"
    assert err.reason == "test reason"
    assert "Sandbox violation [/bad/path]" in str(err)
    assert isinstance(err, RuntimeError)


def test_validate_host_allowed_passes(tmp_path: Path) -> None:
    """SandboxMixin._validate_host() does not raise when the host is listed in allowed_hosts.

    Uses a minimal concrete class that provides _sandbox_config via __init__.
    """

    class _Agent(SandboxMixin):
        """Minimal agent for testing SandboxMixin host validation."""

        def __init__(self) -> None:
            """Initialize with a config that whitelists trusted.example.com."""
            self._sandbox_config = SandboxConfig.from_strings([str(tmp_path)], ["trusted.example.com"])

    agent = _Agent()
    # Should not raise — host is in the allowlist
    agent._validate_host("trusted.example.com")


def test_validate_host_forbidden_raises(tmp_path: Path) -> None:
    """SandboxMixin._validate_host() raises SandboxViolationError for a host not in allowed_hosts.

    Verifies that err.resource equals the forbidden hostname string exactly.
    """

    class _Agent(SandboxMixin):
        """Minimal agent for testing SandboxMixin forbidden host rejection."""

        def __init__(self) -> None:
            """Initialize with a config that only allows trusted.example.com."""
            self._sandbox_config = SandboxConfig.from_strings([str(tmp_path)], ["trusted.example.com"])

    agent = _Agent()
    with pytest.raises(SandboxViolationError) as exc_info:
        agent._validate_host("evil.com")
    assert exc_info.value.resource == "evil.com"


def test_validate_host_allow_all_hosts_bypasses(tmp_path: Path) -> None:
    """SandboxMixin._validate_host() never raises when allow_all_hosts=True regardless of input.

    Verifies the bypass flag short-circuits the allowlist check entirely.
    """

    class _Agent(SandboxMixin):
        """Minimal agent for testing global host bypass via allow_all_hosts=True."""

        def __init__(self) -> None:
            """Initialize with allow_all_hosts=True (empty allowlist)."""
            self._sandbox_config = SandboxConfig.from_strings([str(tmp_path)], [], allow_all_hosts=True)

    agent = _Agent()
    # Neither of these should raise when allow_all_hosts is True
    agent._validate_host("evil.com")
    agent._validate_host("another-evil.net")


# ===========================================================================
# Integration tests — I1 through I7
# ===========================================================================


@pytest.mark.asyncio
async def test_sandbox_tx_write_inside_allowed_path(tmp_path: Path) -> None:
    """SandboxedStorageTransaction.write() + acommit() writes a file to an allowed path.

    Verifies that the file exists on disk and its content matches after acommit().
    """
    config = SandboxConfig.from_strings([str(tmp_path)], [])
    tx = SandboxedStorageTransaction(sandbox=config)
    target = tmp_path / "output.bin"
    await tx.write(target, b"hello")
    await tx.acommit()
    assert target.exists()
    assert target.read_bytes() == b"hello"


@pytest.mark.asyncio
async def test_sandbox_tx_write_outside_allowed_path_raises(tmp_path: Path) -> None:
    """SandboxedStorageTransaction.write() raises SandboxViolationError for a path outside allowed_paths.

    Verifies that the violation is raised before any operation is queued (tx._ops stays empty).
    """
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    config = SandboxConfig.from_strings([str(allowed)], [])
    tx = SandboxedStorageTransaction(sandbox=config)
    outside = tmp_path / "forbidden" / "file.txt"
    with pytest.raises(SandboxViolationError):
        await tx.write(outside, b"bad")
    # Nothing must be queued after a violation
    assert tx._ops == []


@pytest.mark.asyncio
async def test_sandbox_tx_delete_outside_allowed_path_raises(tmp_path: Path) -> None:
    """SandboxedStorageTransaction.delete() raises SandboxViolationError for a path outside allowed_paths.

    Verifies that delete() enforces the path allowlist before queuing the operation.
    """
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    config = SandboxConfig.from_strings([str(allowed)], [])
    tx = SandboxedStorageTransaction(sandbox=config)
    outside = tmp_path / "forbidden" / "file.txt"
    with pytest.raises(SandboxViolationError):
        await tx.delete(outside)


@pytest.mark.asyncio
async def test_sandbox_tx_mkdir_outside_allowed_path_raises(tmp_path: Path) -> None:
    """SandboxedStorageTransaction.mkdir() raises SandboxViolationError for a path outside allowed_paths.

    Verifies that mkdir() enforces the path allowlist before queuing the operation.
    """
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    config = SandboxConfig.from_strings([str(allowed)], [])
    tx = SandboxedStorageTransaction(sandbox=config)
    outside = tmp_path / "forbidden" / "subdir"
    with pytest.raises(SandboxViolationError):
        await tx.mkdir(outside)


def test_sandbox_tx_commit_legacy_forbidden_target_raises(tmp_path: Path) -> None:
    """SandboxedStorageTransaction.commit() raises SandboxViolationError when legacy target is outside allowed_paths.

    Verifies that commit() validates self._target before writing and that no partial file is
    created on disk.
    """
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    outside_target = tmp_path / "forbidden.txt"
    config = SandboxConfig.from_strings([str(allowed)], [])
    tx = SandboxedStorageTransaction(sandbox=config, target=outside_target)
    tx.stage(b"should not be written")
    with pytest.raises(SandboxViolationError):
        tx.commit()
    # The file must not have been created despite staged content
    assert not outside_target.exists()


@pytest.mark.asyncio
async def test_sandbox_mixin_agent_writes_to_allowed_dir(tmp_path: Path) -> None:
    """A class with SandboxMixin can write to an allowed directory via sandbox_tx().

    Verifies the full path: SandboxMixin.sandbox_tx() -> write() -> acommit() -> file on disk.
    """

    class _Agent(SandboxMixin):
        """Minimal concrete agent that uses SandboxMixin for sandboxed I/O."""

        def __init__(self, allowed_dir: Path) -> None:
            """Initialize with a SandboxConfig that permits allowed_dir."""
            self._sandbox_config = SandboxConfig.from_strings([str(allowed_dir)], [])

    agent = _Agent(allowed_dir=tmp_path)
    target = tmp_path / "agent_output.txt"
    tx = agent.sandbox_tx()
    await tx.write(target, b"from agent")
    await tx.acommit()
    assert target.exists()
    assert target.read_bytes() == b"from agent"


@pytest.mark.asyncio
async def test_sandbox_tx_write_op_not_queued_on_violation(tmp_path: Path) -> None:
    """SandboxedStorageTransaction._ops remains empty after a write() that raises SandboxViolationError.

    Confirms the invariant that a violation prevents the operation from being queued,
    making implicit rollback trivial (nothing to roll back).
    """
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    config = SandboxConfig.from_strings([str(allowed)], [])
    tx = SandboxedStorageTransaction(sandbox=config)
    outside = tmp_path / "outside" / "file.txt"
    with pytest.raises(SandboxViolationError):
        await tx.write(outside, b"bad data")
    assert len(tx._ops) == 0


# ===========================================================================
# Negative / escape tests — N1 through N3
# ===========================================================================


def test_validate_path_symlink_escape_raises(tmp_path: Path) -> None:
    """SandboxedStorageTransaction._validate_path() raises for a symlink that resolves outside allowed_paths.

    Creates a symlink inside allowed_paths[0] that points to a directory outside it, then
    verifies that resolve()-based validation catches the escape.
    Skips on platforms that do not support symlink creation.
    """
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    escape_target = tmp_path / "escape"
    escape_target.mkdir()
    link_inside_allowed = allowed / "link_to_escape"
    try:
        os.symlink(str(escape_target), str(link_inside_allowed))
    except (OSError, NotImplementedError):
        pytest.skip("Symlink creation not supported on this platform/privilege level")
    config = SandboxConfig.from_strings([str(allowed)], [])
    tx = SandboxedStorageTransaction(sandbox=config)
    # The symlink resolves to escape_target which is outside allowed
    with pytest.raises(SandboxViolationError):
        tx._validate_path(link_inside_allowed / "file.txt")


def test_validate_path_traversal_string_raises(tmp_path: Path) -> None:
    """SandboxedStorageTransaction._validate_path() raises for a path that traverses above allowed_paths.

    A path of the form allowed/../sibling must be resolved to its real location and
    rejected because it escapes the allowed root directory.
    """
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    config = SandboxConfig.from_strings([str(allowed)], [])
    tx = SandboxedStorageTransaction(sandbox=config)
    # Path traversal: allowed/../escape attempts to leave the allowed dir
    traversal_path = allowed / ".." / "escape" / "passwd"
    with pytest.raises(SandboxViolationError):
        tx._validate_path(traversal_path)


@pytest.mark.asyncio
async def test_sandbox_config_empty_allowed_paths_rejects_all(tmp_path: Path) -> None:
    """SandboxedStorageTransaction raises SandboxViolationError for any path when allowed_paths is empty.

    An empty allowlist is a deny-all policy; even tmp_path itself must be rejected.
    """
    config = SandboxConfig.from_strings([], [])
    tx = SandboxedStorageTransaction(sandbox=config)
    # Even a path that would normally be fine must be rejected with no allowlist
    with pytest.raises(SandboxViolationError):
        await tx.write(tmp_path / "file.txt", b"data")
