#!/usr/bin/env python3
"""Tests for the Rust-based encryption and decryption functions in rust_core."""
import os
import sys
import pytest
from pathlib import Path

# Ensure the build directory is first on path so the compiled extension
# is loaded instead of the plain python namespace package that lives in
# the workspace root.
_build_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "target", "debug")
)
if _build_dir not in sys.path:
    sys.path.insert(0, _build_dir)

# On Windows the crate outputs rust_core.dll; Python expects .pyd
# Always refresh the .pyd so reruns after rebuilding pick up the latest
# library version.
if sys.platform.startswith("win"):
    dll = os.path.join(_build_dir, "rust_core.dll")
    pyd = os.path.join(_build_dir, "rust_core.pyd")
    if os.path.exists(dll):
        try:
            os.remove(pyd)
        except FileNotFoundError:
            pass
        os.rename(dll, pyd)

import rust_core  # noqa: E402


def test_encrypt_decrypt_roundtrip(tmp_path: Path) -> None:
    """Test that encrypting and then decrypting returns the original plaintext.

    The API should first allow loading a public/private key pair from disk; if
    the keys are present they are used in the XOR operation.  The unit test
    therefore writes two tiny key files in the temporary directory and
    exercises `load_keys` before performing the round trip.
    """
    # create key files with one-byte values for simplicity
    pub_file = tmp_path / "key.pub"
    priv_file = tmp_path / "key.priv"
    pub_file.write_bytes(b"\x01")
    priv_file.write_bytes(b"\x02")

    assert hasattr(rust_core, "load_keys"), "load_keys missing"
    rust_core.load_keys(str(pub_file), str(priv_file))

    plaintext = b"sensitive data"
    assert hasattr(rust_core, "encrypt_data"), "encrypt_data missing"
    assert hasattr(rust_core, "decrypt_data"), "decrypt_data missing"

    encrypted = getattr(rust_core, "encrypt_data")(plaintext)  # noqa: F821
    assert isinstance(encrypted, (bytes, bytearray))
    # nonce prefix should be present
    assert len(encrypted) >= len(plaintext) + 24
    # ciphertext must differ
    assert encrypted[24:] != plaintext, "ciphertext body should differ"
    # encrypt again to exercise randomness/nonce generation
    encrypted2 = rust_core.encrypt_data(plaintext)
    assert encrypted2 != encrypted, "nonce should make each output unique"

    decrypted = getattr(rust_core, "decrypt_data")(encrypted)  # noqa: F821
    assert decrypted == plaintext
    with pytest.raises(RuntimeError):
        rust_core.decrypt_data(encrypted + b"x")


def test_metrics_counter():
    # call a couple of operations and ensure counters appear in output
    rust_core.encrypt_data(b"foo")
    rust_core.decrypt_data(rust_core.encrypt_data(b"bar"))
    metrics = rust_core.gather_metrics()
    assert "encrypt_data_calls" in metrics
    assert "decrypt_data_calls" in metrics


def test_export_keys(tmp_path: Path):
    # if no keys loaded the call should fail
    with pytest.raises(RuntimeError):
        rust_core.export_keys(str(tmp_path / "a"), str(tmp_path / "b"))
    # load keys and then export
    pub_file = tmp_path / "key.pub"
    priv_file = tmp_path / "key.priv"
    pub_file.write_bytes(b"p")
    priv_file.write_bytes(b"q")
    rust_core.load_keys(str(pub_file), str(priv_file))
    out_pub = tmp_path / "out.pub"
    out_priv = tmp_path / "out.priv"
    rust_core.export_keys(str(out_pub), str(out_priv))
    assert out_pub.read_bytes() == b"p"
    assert out_priv.read_bytes() == b"q"


def test_transaction_rollback(tmp_path: Path) -> None:
    """Verify that transaction operations exist and rollback behaves as expected.

    The functions are not implemented yet, so this test will initially fail
    either because the attributes are missing or because the rollback logic is
    a no-op.  We'll exercise file creation inside the transaction in later
    steps.

    This test does not depend on the encryption algorithm; it simply ensures
    the metadata APIs work and that rollback removes any created files.
    """
    # API surface should exist first
    assert hasattr(rust_core, "begin_transaction"), "begin_transaction missing"
    assert hasattr(rust_core, "commit_transaction"), "commit_transaction missing"
    assert hasattr(rust_core, "rollback_transaction"), "rollback_transaction missing"

    # start a transaction and create a file that should disappear on rollback
    rust_core.begin_transaction(str(tmp_path))
    f = open(tmp_path / "foo.txt", "w", encoding="utf-8")
    f.write("hello")
    f.close()

    # simulate failure and rollback
    with pytest.raises(RuntimeError):
        raise RuntimeError("oops")
    rust_core.rollback_transaction()
    assert not (tmp_path / "foo.txt").exists(), "transaction should have rolled back"


def test_key_rotation() -> None:
    """Verify the key rotation API increments version and decrypts old data.

    The encryption primitive is stateful only via a 64-bit counter; rotating
    keys today simply bumps the counter.  We check that ciphertext produced
    before a rotation can still be decrypted afterward.
    """
    assert hasattr(rust_core, "current_key_version"), "current_key_version missing"
    assert hasattr(rust_core, "rotate_keys"), "rotate_keys missing"

    v1 = rust_core.current_key_version()
    rust_core.rotate_keys()
    v2 = rust_core.current_key_version()
    assert v2 != v1

    # ensure data encrypted under old key can still be decrypted after another rotation
    data = b"abc"
    encrypted = rust_core.encrypt_data(data)
    rust_core.rotate_keys()
    decrypted = rust_core.decrypt_data(encrypted)
    assert decrypted == data
