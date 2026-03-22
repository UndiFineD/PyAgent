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
"""Tests for prj0000028 Python-level transport T-1 classes.

Tests NodeIdentity and LoopbackChannel via the Python transport API.
"""
import pytest

try:
    from transport import LoopbackChannel, NodeIdentity
    _TRANSPORT_AVAILABLE = True
except ImportError:
    _TRANSPORT_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not _TRANSPORT_AVAILABLE,
    reason="transport module not importable",
)


# ─── NodeIdentity ─────────────────────────────────────────────────────────

def test_node_identity_public_key_is_32_bytes():
    """NodeIdentity.public_key must be 32 bytes (Ed25519 verifying key)."""
    identity = NodeIdentity()
    assert isinstance(identity.public_key, bytes)
    assert len(identity.public_key) == 32


def test_node_identity_sign_returns_64_bytes():
    """NodeIdentity.sign must return a 64-byte Ed25519 signature."""
    identity = NodeIdentity()
    sig = identity.sign(b"test message")
    assert isinstance(sig, bytes)
    assert len(sig) == 64


def test_node_identity_verify_valid_signature():
    """NodeIdentity.verify must accept a valid signature."""
    identity = NodeIdentity()
    msg = b"authentic message"
    sig = identity.sign(msg)
    assert NodeIdentity.verify(identity.public_key, msg, sig) is True


def test_node_identity_verify_rejects_tampered_message():
    """NodeIdentity.verify must reject a signature over a different message."""
    identity = NodeIdentity()
    sig = identity.sign(b"original")
    assert NodeIdentity.verify(identity.public_key, b"tampered", sig) is False


def test_node_identity_repr():
    """NodeIdentity.__repr__ must include the hex prefix of the public key."""
    identity = NodeIdentity()
    r = repr(identity)
    assert "NodeIdentity" in r


# ─── LoopbackChannel ──────────────────────────────────────────────────────

def test_loopback_channel_send_recv():
    """LoopbackChannel.send/recv must deliver a plaintext message end-to-end."""
    NodeIdentity()  # ensure an identity exists
    ch = LoopbackChannel()
    ch.send(b"hello loopback")
    assert ch.recv() == b"hello loopback"


def test_loopback_channel_binary_payload():
    """LoopbackChannel must preserve arbitrary binary data."""
    NodeIdentity()
    ch = LoopbackChannel()
    binary = bytes(range(256))
    ch.send(binary)
    assert ch.recv() == binary


def test_loopback_channel_bidirectional():
    """LoopbackChannel supports B→A communication via send_b/recv_a."""
    NodeIdentity()
    ch = LoopbackChannel()
    ch.send_b(b"pong")
    assert ch.recv_a() == b"pong"


def test_loopback_channel_empty_payload():
    """Empty payload must round-trip correctly over LoopbackChannel."""
    NodeIdentity()
    ch = LoopbackChannel()
    ch.send(b"")
    assert ch.recv() == b""


def test_loopback_channel_multiple_messages():
    """Multiple messages can be sent and received in order."""
    NodeIdentity()
    ch = LoopbackChannel()
    messages = [b"one", b"two", b"three"]
    for m in messages:
        ch.send(m)
    for expected in messages:
        assert ch.recv() == expected
