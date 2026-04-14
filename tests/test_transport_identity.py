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
"""T-1 transport identity tests — run against compiled rust_core extension."""

import importlib.util
import os
import sys

import pytest

try:
    import rust_core as rc  # type: ignore

    if not hasattr(rc, "generate_node_identity"):
        # Fallback: load locally built extension from target/debug
        _build = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "rust_core", "target", "debug"))
        if _build not in sys.path:
            sys.path.insert(0, _build)

        if sys.platform.startswith("win"):
            dll = os.path.join(_build, "rust_core.dll")
            pyd = os.path.join(_build, "rust_core.pyd")
            if os.path.exists(dll) and not os.path.exists(pyd):
                try:
                    os.remove(pyd)
                except FileNotFoundError:
                    pass
                os.rename(dll, pyd)

        _ext = "rust_core.pyd" if sys.platform.startswith("win") else "rust_core.so"
        _ext_path = os.path.join(_build, _ext)
        if os.path.exists(_ext_path):
            spec = importlib.util.spec_from_file_location("rust_core", _ext_path)
            rc = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
            spec.loader.exec_module(rc)  # type: ignore[union-attr]
            sys.modules["rust_core"] = rc

        if not hasattr(rc, "generate_node_identity"):
            pytest.skip("rust_core compiled extension not available", allow_module_level=True)
except ImportError:
    pytest.skip("rust_core not importable", allow_module_level=True)


def test_generate_node_identity_returns_32_bytes():
    """Generating a node identity should produce a 32-byte public key."""
    node_id = rc.generate_node_identity()
    assert isinstance(node_id, bytes), "node_id must be bytes"
    assert len(node_id) == 32, f"expected 32 bytes, got {len(node_id)}"


def test_node_id_is_deterministic_for_loaded_identity(tmp_path):
    """Saving and loading an identity should yield the same node ID."""
    rc.generate_node_identity()
    rc.save_node_identity(str(tmp_path / "identity.bin"))
    node_id_a = rc.get_node_id()
    rc.load_node_identity(str(tmp_path / "identity.bin"))
    node_id_b = rc.get_node_id()
    assert node_id_a == node_id_b


def test_sign_and_verify_roundtrip():
    """Signing a message and verifying it should succeed with the correct node ID."""
    rc.generate_node_identity()
    msg = b"hello transport"
    sig = rc.transport_sign(msg)
    assert isinstance(sig, bytes) and len(sig) == 64
    assert rc.transport_verify(rc.get_node_id(), msg, sig) is True


def test_verify_fails_for_tampered_message():
    """Verifying a tampered message should fail."""
    rc.generate_node_identity()
    msg = b"original"
    sig = rc.transport_sign(msg)
    assert rc.transport_verify(rc.get_node_id(), b"tampered", sig) is False


def test_loopback_send_recv():
    """Two virtual peers exchange a message over an in-memory loopback channel."""
    pair = rc.transport_loopback_pair()
    handle_a, handle_b = pair
    rc.transport_send(handle_a, b"ping from A")
    received = rc.transport_recv(handle_b)
    assert received == b"ping from A"


def test_loopback_roundtrip_integrity():
    """Sending and receiving a larger payload over loopback should preserve integrity."""
    pair = rc.transport_loopback_pair()
    handle_a, handle_b = pair
    payload = b"\x00\xff" * 512  # 1 KiB of alternating bytes
    rc.transport_send(handle_a, payload)
    assert rc.transport_recv(handle_b) == payload


def test_noise_handshake_produces_encrypted_channel():
    """After Noise_XX handshake, send/recv transparently encrypts/decrypts."""
    rc.generate_node_identity()
    pair = rc.transport_loopback_pair()
    handle_a, handle_b = pair
    rc.transport_handshake_initiator(handle_a)
    rc.transport_handshake_responder(handle_b)
    rc.transport_handshake_finalize(handle_a, handle_b)
    rc.transport_send(handle_a, b"secret")
    plain = rc.transport_recv(handle_b)
    assert plain == b"secret"


def test_noise_handshake_rejects_unknown_peer():
    """Connecting with an untrusted static key must fail during handshake."""
    pair = rc.transport_loopback_pair()
    ha, hb = pair
    rc.transport_handshake_initiator(ha)
    # Switch to a brand-new identity before responding — simulates unknown peer
    rc.generate_node_identity()
    with pytest.raises(Exception, match="handshake"):
        rc.transport_handshake_responder(hb)
        rc.transport_handshake_finalize(ha, hb)
