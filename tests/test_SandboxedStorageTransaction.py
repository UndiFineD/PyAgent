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

"""Per-module tests for src/core/sandbox/SandboxedStorageTransaction.py.

Comprehensive sandbox integration tests live in tests/test_sandbox.py.
This file satisfies the test_each_core_has_test_file convention.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.core.sandbox.SandboxConfig import SandboxConfig
from src.core.sandbox.SandboxedStorageTransaction import SandboxedStorageTransaction, validate


def test_sandboxed_storage_transaction_validate() -> None:
    """Ensure the SandboxedStorageTransaction validate() helper returns True."""
    assert validate() is True


def test_sandboxed_storage_transaction_is_importable() -> None:
    """SandboxedStorageTransaction must be importable as a class."""
    assert SandboxedStorageTransaction is not None
    assert issubclass(SandboxedStorageTransaction, object)


@pytest.mark.asyncio
async def test_sandboxed_storage_transaction_delete_inside_allowed_path(tmp_path: Path) -> None:
    """delete() queues the delete operation when path is inside allowed_paths."""
    config = SandboxConfig.from_strings([str(tmp_path)], [])
    tx = SandboxedStorageTransaction(sandbox=config)
    target = tmp_path / "file_to_delete.txt"
    await tx.delete(target)
    assert len(tx._ops) == 1
    assert tx._ops[0][0] == "delete"


@pytest.mark.asyncio
async def test_sandboxed_storage_transaction_mkdir_inside_allowed_path(tmp_path: Path) -> None:
    """mkdir() queues the mkdir operation when path is inside allowed_paths."""
    config = SandboxConfig.from_strings([str(tmp_path)], [])
    tx = SandboxedStorageTransaction(sandbox=config)
    new_dir = tmp_path / "new_subdir"
    await tx.mkdir(new_dir)
    assert len(tx._ops) == 1
    assert tx._ops[0][0] == "mkdir"


def test_sandboxed_storage_transaction_commit_none_target_is_noop(tmp_path: Path) -> None:
    """commit() with no target and nothing staged must not raise (safe no-op path)."""
    config = SandboxConfig.from_strings([str(tmp_path)], [])
    tx = SandboxedStorageTransaction(sandbox=config)
    tx.commit()  # _target is None, _staged is None — must be a complete no-op
