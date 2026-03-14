#!/usr/bin/env python3
"""Transport module for PyAgent.

This module is a thin Python wrapper around the Rust `rust_core` extension.

During development we prefer the locally built `rust_core` extension in
`rust_core/target/debug` so tests and local scripts use the same compiled
Rust code even if a different `rust_core` package is installed in the
active Python environment.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _locate_local_rust_core() -> Path | None:
    """Locate a local rust_core build output directory (target/debug).

    The repository layout is:
        <repo>/rust_core/target/debug

    This is where `cargo build` writes the Python extension (`rust_core.pyd`).
    """

    repo_root = Path(__file__).resolve().parents[2]
    candidate = repo_root / "rust_core" / "target" / "debug"
    return candidate if candidate.exists() else None


def _apply_local_rust_core_path() -> None:
    """Add local rust_core build output to sys.path (if present).

    This ensures the repo's local `rust_core/target/debug` build is imported
    over any installed `rust_core` package.
    """

    local_dir = _locate_local_rust_core()
    if local_dir is None:
        return

    build_dir = str(local_dir)
    if build_dir not in sys.path:
        sys.path.insert(0, build_dir)

    # On Windows, the Rust build emits rust_core.dll; Python expects .pyd
    if sys.platform.startswith("win"):
        dll = os.path.join(build_dir, "rust_core.dll")
        pyd = os.path.join(build_dir, "rust_core.pyd")
        if os.path.exists(dll) and not os.path.exists(pyd):
            try:
                os.remove(pyd)
            except FileNotFoundError:
                pass
            os.rename(dll, pyd)


_apply_local_rust_core_path()

try:
    import rust_core  # type: ignore
except ImportError:  # pragma: no cover
    rust_core = None  # type: ignore


def _ensure_rust_core() -> None:
    if rust_core is None:
        raise ImportError(
            "rust_core extension is not available. Ensure the Rust extension is built."
        )


def generate_node_identity() -> bytes:
    """Generate a fresh node identity (32-byte Ed25519 public key)."""
    _ensure_rust_core()
    return rust_core.generate_node_identity()


def get_node_id() -> bytes:
    """Return the current node identity (32-byte public key)."""
    _ensure_rust_core()
    return rust_core.get_node_id()


def save_node_identity(path: str) -> None:
    """Save the current node identity to disk."""
    _ensure_rust_core()
    return rust_core.save_node_identity(path)


def load_node_identity(path: str) -> None:
    """Load a node identity from disk."""
    _ensure_rust_core()
    return rust_core.load_node_identity(path)


def transport_loopback_pair() -> tuple[int, int]:
    """Create a pair of connected transport handles for testing."""
    _ensure_rust_core()
    return rust_core.transport_loopback_pair()


def transport_send(handle: int, payload: bytes) -> None:
    """Send a payload over the transport handle."""
    _ensure_rust_core()
    return rust_core.transport_send(handle, payload)


def transport_recv(handle: int) -> bytes:
    """Receive a payload from the transport handle."""
    _ensure_rust_core()
    return rust_core.transport_recv(handle)


def transport_handshake_initiator(handle: int) -> None:
    """Perform the initiator side of the transport handshake."""
    _ensure_rust_core()
    return rust_core.transport_handshake_initiator(handle)


def transport_handshake_responder(handle: int) -> None:
    """Perform the responder side of the transport handshake."""
    _ensure_rust_core()
    return rust_core.transport_handshake_responder(handle)


def transport_handshake_finalize(a: int, b: int) -> None:
    """Finalize the transport handshake between two handles."""
    _ensure_rust_core()
    return rust_core.transport_handshake_finalize(a, b)


def placeholder() -> bool:
    """A no-op placeholder to validate that the transport package is importable."""
    return True


__all__ = [
    "generate_node_identity",
    "get_node_id",
    "save_node_identity",
    "load_node_identity",
    "transport_loopback_pair",
    "transport_send",
    "transport_recv",
    "transport_handshake_initiator",
    "transport_handshake_responder",
    "transport_handshake_finalize",
    "placeholder",
]
