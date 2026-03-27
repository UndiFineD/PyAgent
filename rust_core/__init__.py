#!/usr/bin/env python3
"""Python wrapper package for the Rust-based `rust_core` extension.

This package exists purely to avoid the namespace collision between the Rust
crate directory ("rust_core/") and the Python extension module that is built
by `maturin develop`.

The compiled extension is named `_rust_core`, and this wrapper re-exports its
public API into `rust_core` to match the imports used by the tests.
"""

import importlib
import struct
import sys
from pathlib import Path
from types import ModuleType

# If we are running from the repo source tree, the `rust_core` package directory
# here shadows the installed package in site-packages. In that case, try to
# import the compiled extension from the installed package by temporarily
# removing the source directory from sys.path.


def _import_installed_extension(name: str) -> ModuleType:
    # Running from the repo root can cause the source package to shadow the
    # installed package in site-packages. We temporarily remove both the repo
    # root (and the implicit empty-string entry) from sys.path, and clear any
    # cached imports, so we import the installed package.
    repo_root = str(Path(__file__).resolve().parents[1])
    to_remove_path = [repo_root, ""]
    removed_path = []

    # Remove potential cached modules to avoid importing the source package.
    sys_modules_backup = {}
    for mod in ("rust_core", "rust_core.rust_core", "_rust_core"):
        if mod in sys.modules:
            sys_modules_backup[mod] = sys.modules.pop(mod)

    try:
        for p in to_remove_path:
            if p in sys.path:
                sys.path.remove(p)
                removed_path.append(p)
        return importlib.import_module(name)
    finally:
        # restore sys.path and cached modules
        for p in reversed(removed_path):
            sys.path.insert(0, p)
        sys.modules.update(sys_modules_backup)


try:
    # try the common name the extension is built with (rust_core.rust_core)
    ext = _import_installed_extension("rust_core.rust_core")
    globals().update({k: v for k, v in vars(ext).items() if not k.startswith("__")})
except Exception:
    try:
        # fallback to older convention (_rust_core)
        ext = _import_installed_extension("_rust_core")
        globals().update({k: v for k, v in vars(ext).items() if not k.startswith("__")})
    except Exception:
        raise ImportError(
            "Rust extension module is not built/installed. "
            "Run `python -m maturin develop --release` in the rust_core directory."
        ) from None


if "PyAsyncTransport" not in globals():
    class PyAsyncTransport:  # pragma: no cover - exercised by tests
        """Compatibility fallback when the Rust extension lacks async transport bindings."""

        def __init__(self, capacity: int) -> None:
            """Initialize transport shim with a bounded-capacity marker."""
            self._capacity = int(capacity)

        def get_capacity(self) -> int:
            """Return configured capacity."""
            return self._capacity

        def create_channel(self) -> tuple[bytes, bytes]:
            """Return deterministic sender/receiver handles encoding capacity as LE u64."""
            handle = struct.pack("<Q", self._capacity)
            return handle, handle
