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
"""WebSocket E2E encryption primitives — X25519 ECDH + AES-256-GCM."""
from __future__ import annotations

import os

from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
    PrivateFormat,
    NoEncryption,
)


def generate_keypair() -> tuple[bytes, bytes]:
    """Generate an ephemeral X25519 key pair.

    Returns:
        (private_key_bytes, public_key_bytes) — each 32 bytes.
    """
    private_key = X25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=Encoding.Raw,
        format=PrivateFormat.Raw,
        encryption_algorithm=NoEncryption(),
    )
    public_bytes = private_key.public_key().public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw,
    )
    return private_bytes, public_bytes


def derive_shared_secret(private_key_bytes: bytes, peer_public_key_bytes: bytes) -> bytes:
    """Perform X25519 ECDH and return the 32-byte shared secret.

    Args:
        private_key_bytes: Raw 32-byte private key.
        peer_public_key_bytes: Raw 32-byte public key from the peer.

    Returns:
        32-byte shared secret suitable for AES-256 key material.
    """
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey

    private_key = X25519PrivateKey.from_private_bytes(private_key_bytes)
    peer_public_key = X25519PublicKey.from_public_bytes(peer_public_key_bytes)
    return private_key.exchange(peer_public_key)


def encrypt_message(key: bytes, plaintext: bytes) -> bytes:
    """Encrypt *plaintext* with AES-256-GCM using *key*.

    A fresh 12-byte random nonce is generated for each call.

    Args:
        key: 32-byte AES-256 key.
        plaintext: Arbitrary byte payload.

    Returns:
        ``nonce[12] + ciphertext + gcm_tag[16]`` — the nonce is prepended.
    """
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return nonce + ciphertext


def decrypt_message(key: bytes, ciphertext: bytes) -> bytes:
    """Decrypt *ciphertext* with AES-256-GCM using *key*.

    Args:
        key: 32-byte AES-256 key.
        ciphertext: ``nonce[12] + ciphertext + gcm_tag[16]`` as returned by
            :func:`encrypt_message`.

    Returns:
        Original plaintext bytes.

    Raises:
        cryptography.exceptions.InvalidTag: If the GCM authentication tag is invalid.
        ValueError: If *ciphertext* is shorter than the 12-byte nonce.
    """
    if len(ciphertext) < 12:
        raise ValueError("Ciphertext too short — nonce missing")
    nonce = ciphertext[:12]
    data = ciphertext[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, data, None)
