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

"""Tests for the security bridge between Python and the Rust security crate."""

from __future__ import annotations

from pathlib import Path

from src.core import security_bridge


def test_security_bridge_encrypt_decrypt(tmp_path: Path):
    """Test that the security bridge can encrypt and decrypt data correctly."""
    key_file = tmp_path / "key.txt"
    security_bridge.generate_key(key_file)

    plaintext = "hello world"
    ciphertext = security_bridge.encrypt(key_file, plaintext)
    assert ciphertext

    decrypted = security_bridge.decrypt(key_file, ciphertext)
    assert decrypted == plaintext


def test_security_bridge_rotate_key_changes_key(tmp_path: Path):
    """Test that rotating the key changes the key file."""
    key_file = tmp_path / "key.txt"
    security_bridge.generate_key(key_file)
    before = key_file.read_text()

    security_bridge.rotate_keys(key_file)
    after = key_file.read_text()

    assert before != after
