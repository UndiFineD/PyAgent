#!/usr/bin/env python3
"""Transport module for PyAgent.

This module is a thin Python wrapper around the Rust `rust_core` extension.
"""

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
    _ensure_rust_core()
    return rust_core.transport_loopback_pair()


def transport_send(handle: int, payload: bytes) -> None:
    _ensure_rust_core()
    return rust_core.transport_send(handle, payload)


def transport_recv(handle: int) -> bytes:
    _ensure_rust_core()
    return rust_core.transport_recv(handle)


def transport_handshake_initiator(handle: int) -> None:
    _ensure_rust_core()
    return rust_core.transport_handshake_initiator(handle)


def transport_handshake_responder(handle: int) -> None:
    _ensure_rust_core()
    return rust_core.transport_handshake_responder(handle)


def transport_handshake_finalize(a: int, b: int) -> None:
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
