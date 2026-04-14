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
"""Unit tests for backend/ws_crypto.py — X25519 ECDH + AES-256-GCM primitives."""

from __future__ import annotations

import pytest

from backend.ws_crypto import (
    decrypt_message,
    derive_shared_secret,
    encrypt_message,
    generate_keypair,
)


def test_generate_keypair_returns_32_byte_keys() -> None:
    """Both private and public key bytes must be exactly 32 bytes."""
    priv, pub = generate_keypair()
    assert isinstance(priv, bytes), "private key must be bytes"
    assert isinstance(pub, bytes), "public key must be bytes"
    assert len(priv) == 32, f"private key must be 32 bytes, got {len(priv)}"
    assert len(pub) == 32, f"public key must be 32 bytes, got {len(pub)}"


def test_ecdh_shared_secret_symmetric() -> None:
    """Alice and Bob must derive the same shared secret from each other's public keys."""
    alice_priv, alice_pub = generate_keypair()
    bob_priv, bob_pub = generate_keypair()

    alice_secret = derive_shared_secret(alice_priv, bob_pub)
    bob_secret = derive_shared_secret(bob_priv, alice_pub)

    assert alice_secret == bob_secret, "ECDH shared secrets must be symmetric"
    assert len(alice_secret) == 32, "shared secret must be 32 bytes"


def test_encrypt_decrypt_roundtrip() -> None:
    """decrypt_message(key, encrypt_message(key, msg)) must equal original msg."""
    priv_a, pub_a = generate_keypair()
    priv_b, pub_b = generate_keypair()
    key = derive_shared_secret(priv_a, pub_b)

    plaintext = b"Hello, encrypted WebSocket world!"
    ciphertext = encrypt_message(key, plaintext)
    recovered = decrypt_message(key, ciphertext)

    assert recovered == plaintext


def test_decrypt_with_wrong_key_raises() -> None:
    """Decrypting with a different key must raise an exception."""
    from cryptography.exceptions import InvalidTag

    priv_a, pub_a = generate_keypair()
    priv_b, pub_b = generate_keypair()
    priv_c, pub_c = generate_keypair()

    key_correct = derive_shared_secret(priv_a, pub_b)
    key_wrong = derive_shared_secret(priv_a, pub_c)  # different peer → different secret

    ciphertext = encrypt_message(key_correct, b"secret payload")

    with pytest.raises(InvalidTag):
        decrypt_message(key_wrong, ciphertext)


def test_nonce_prepended_to_ciphertext() -> None:
    """The first 12 bytes of the encrypt_message output must be the random nonce."""
    key = b"\x00" * 32  # zero key — valid for testing nonce structure
    plaintext = b"nonce structure test"

    result = encrypt_message(key, plaintext)

    # Result must be at least 12 (nonce) + len(plaintext) + 16 (GCM tag) bytes
    assert len(result) >= 12 + len(plaintext) + 16

    # Verify we can decrypt using the first 12 bytes as the nonce manually
    nonce = result[:12]
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    aesgcm = AESGCM(key)
    recovered = aesgcm.decrypt(nonce, result[12:], None)
    assert recovered == plaintext, "Manually extracted nonce must allow correct decryption"
