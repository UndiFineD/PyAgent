#!/usr/bin/env python3
"""Tests for the Rust-based encryption and decryption functions in rust_core."""
import importlib.util
import os
import sys
from pathlib import Path

import pytest

# rust_core extension will be loaded manually after adjusting sys.path

# Ensure the build directory is first on path so the compiled extension
# is loaded instead of the plain python namespace package that lives in
# the workspace root.  Remove the root entry entirely to avoid shadowing.
_build_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "target", "debug")
)
# insert build dir at front
if _build_dir not in sys.path:
    sys.path.insert(0, _build_dir)
# remove workspace root ('' entry) which otherwise creates a namespace package
root = os.path.abspath(os.getcwd())
sys.path = [p for p in sys.path if os.path.abspath(p) != root and p != '']

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

# now import the compiled extension explicitly to avoid namespace collision
_ext_path = os.path.join(_build_dir, "rust_core.pyd")
spec = importlib.util.spec_from_file_location("rust_core", _ext_path)
assert spec is not None, "failed to load spec for rust_core extension"
rust_core = importlib.util.module_from_spec(spec)
# spec.loader is typed as Optional[Loader], but we know it exists when spec is not None
loader = spec.loader
assert loader is not None, "loader missing for rust_core extension"
loader.exec_module(rust_core)
sys.modules["rust_core"] = rust_core

# diagnostic info in case incorrect module is imported
print(f"[test init] rust_core module path={getattr(rust_core, '__file__', '<none>')}")
print(f"[test init] exports={[x for x in dir(rust_core) if not x.startswith('_')]}")


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

    # diagnostic: show which file was imported and what it exports
    print("[diag] rust_core file", getattr(rust_core, '__file__', None))
    print("[diag] exports contains load_keys?", 'load_keys' in dir(rust_core))
    print("[diag] exports sample", [x for x in dir(rust_core) if x.startswith('load')][:10])

    assert hasattr(rust_core, "load_keys"), "load_keys missing"
    rust_core.load_keys(str(pub_file), str(priv_file))

    plaintext = b"sensitive data"
    assert hasattr(rust_core, "encrypt_data"), "encrypt_data missing"
    assert hasattr(rust_core, "decrypt_data"), "decrypt_data missing"

    encrypted = rust_core.encrypt_data(plaintext)  # noqa: F821
    assert isinstance(encrypted, (bytes, bytearray))
    # nonce prefix should be present
    assert len(encrypted) >= len(plaintext) + 24
    # ciphertext must differ
    assert encrypted[24:] != plaintext, "ciphertext body should differ"
    # encrypt again to exercise randomness/nonce generation
    encrypted2 = rust_core.encrypt_data(plaintext)
    assert encrypted2 != encrypted, "nonce should make each output unique"

    decrypted = rust_core.decrypt_data(encrypted)  # noqa: F821
    assert decrypted == plaintext
    with pytest.raises(RuntimeError):
        rust_core.decrypt_data(encrypted + b"x")


def test_metrics_counter() -> None:
    """Test that the gather_metrics function returns expected counters after operations."""
    # call a couple of operations and ensure counters appear in output
    rust_core.encrypt_data(b"foo")
    decrypted = rust_core.decrypt_data(rust_core.encrypt_data(b"bar"))
    print("DECRYPTED in metrics test:", decrypted)
    metrics = rust_core.gather_metrics()
    # debug output to see what metrics returned
    print("METRICS:\n", metrics)
    assert "encrypt_data_calls" in metrics
    assert "decrypt_data_calls" in metrics


def test_rotation_and_gc_metrics(tmp_path: Path) -> None:
    """Test that key rotation and transaction GC operations update metrics."""
    # verify metrics for rotation backup and garbage collection
    if hasattr(rust_core, "clear_keys"):
        rust_core.clear_keys()
    pub_file = tmp_path / "k.pub"
    priv_file = tmp_path / "k.priv"
    pub_file.write_bytes(b"1")
    priv_file.write_bytes(b"2")
    rust_core.load_keys(str(pub_file), str(priv_file))
    rust_core.rotate_keys()
    # remove backup files produced by the rotation so we don't pollute workspace
    import datetime
    import os
    # use timezone-aware UTC now to avoid deprecation warning
    date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    for ext in ("pub", "priv"):
        try:
            os.remove(f"{date}-keys.{ext}")
        except FileNotFoundError:
            pass
    metrics = rust_core.gather_metrics()
    assert "key_backup_calls" in metrics
    assert "rotate_key_calls" in metrics
    # cleanup on empty directory
    gc_dir = tmp_path / "gc"
    gc_dir.mkdir()
    rust_core.cleanup_transactions(str(gc_dir))
    metrics = rust_core.gather_metrics()
    assert "transaction_gc_calls" in metrics


def test_export_keys(tmp_path: Path) -> None:
    """Test that export_keys raises without loaded keys and exports correctly after loading."""
    # ensure a clean slate; previous tests may have loaded keys
    if hasattr(rust_core, "clear_keys"):
        rust_core.clear_keys()

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


def test_key_rotation_backups(tmp_path: Path) -> None:
    """Test that rotating keys creates backup files with the expected naming convention."""
    # start fresh
    if hasattr(rust_core, "clear_keys"):
        rust_core.clear_keys()
    # load keys then rotate, expect backup files
    pub_file = tmp_path / "k.pub"
    priv_file = tmp_path / "k.priv"
    pub_file.write_bytes(b"x")
    priv_file.write_bytes(b"y")
    rust_core.load_keys(str(pub_file), str(priv_file))
    rust_core.rotate_keys()
    import datetime
    import os
    # match updated usage above; avoid deprecation warning
    date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    assert os.path.exists(f"{date}-keys.pub")
    assert os.path.exists(f"{date}-keys.priv")
    # cleanup the created backups so tests don't pollute repo
    os.remove(f"{date}-keys.pub")
    os.remove(f"{date}-keys.priv")


def test_cleanup_transactions(tmp_path: Path) -> None:
    """Test that cleanup_transactions removes old transaction directories."""
    import os
    import time
    base = tmp_path / "transactions"
    base.mkdir()
    old = base / "old"
    old.mkdir()
    (old / "file.txt").write_text("x")
    old_mtime = time.time() - 31 * 24 * 3600
    os.utime(old, (old_mtime, old_mtime))
    rust_core.cleanup_transactions(str(base))
    assert not old.exists(), "old transaction directory should be removed"


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
