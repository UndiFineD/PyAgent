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

"""Tests for the Rust security binary — encrypt/decrypt roundtrip and key rotation."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

SECURITY_BIN = Path("rust_core/security/target/release/security")
if not SECURITY_BIN.exists():
    SECURITY_BIN = Path("rust_core/security/target/debug/security")

pytestmark = pytest.mark.skipif(
    not SECURITY_BIN.exists(),
    reason="Rust security binary not built — run 'cargo build' in rust_core/security/",
)


def _run(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run([str(SECURITY_BIN), *args], capture_output=True, text=True, check=True, **kwargs)


def test_security_binary_keygen(tmp_path: Path) -> None:
    """Keygen creates a non-empty key file."""
    key_file = tmp_path / "key.b64"
    _run(["keygen", "--key-file", str(key_file)])
    assert key_file.exists()
    assert len(key_file.read_text().strip()) > 0


def test_security_binary_encrypt_decrypt_roundtrip(tmp_path: Path) -> None:
    """Encrypt then decrypt returns the original plaintext."""
    key_file = tmp_path / "key.b64"
    _run(["keygen", "--key-file", str(key_file)])

    plaintext = "PyAgent swarm security test"
    result = _run(["encrypt", "--key-file", str(key_file), "--plaintext", plaintext])
    ciphertext = result.stdout.strip()
    assert ciphertext != plaintext

    result = _run(["decrypt", "--key-file", str(key_file), "--ciphertext", ciphertext])
    assert result.stdout.strip() == plaintext


def test_security_binary_rotate_key_changes_file(tmp_path: Path) -> None:
    """Key rotation writes a different key to the file."""
    key_file = tmp_path / "key.b64"
    _run(["keygen", "--key-file", str(key_file)])
    original_key = key_file.read_text().strip()

    _run(["rotate", "--key-file", str(key_file)])
    rotated_key = key_file.read_text().strip()

    assert rotated_key != original_key


def test_security_binary_decrypt_with_rotated_key_fails(tmp_path: Path) -> None:
    """Ciphertext encrypted with original key cannot be decrypted after rotation."""
    key_file = tmp_path / "key.b64"
    _run(["keygen", "--key-file", str(key_file)])

    plaintext = "sensitive payload"
    result = _run(["encrypt", "--key-file", str(key_file), "--plaintext", plaintext])
    ciphertext = result.stdout.strip()

    _run(["rotate", "--key-file", str(key_file)])

    with pytest.raises(subprocess.CalledProcessError):
        _run(["decrypt", "--key-file", str(key_file), "--ciphertext", ciphertext])
