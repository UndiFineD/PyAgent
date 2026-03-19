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

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


def _rust_security_binary() -> Path:
    """Get the path to the Rust security binary, building it if necessary."""
    repo_root = Path(__file__).resolve().parents[2]
    crate = repo_root / "rust_core" / "security"
    binary_name = "rust_core_security.exe" if __import__("sys").platform == "win32" else "rust_core_security"
    binary = crate / "target" / "release" / binary_name

    if not binary.exists():
        subprocess.run(["cargo", "build", "--release"], cwd=crate, check=True)

    return binary


def generate_key(path: Path) -> None:
    """Generate a new encryption key and save it to the specified file."""
    bin_path = _rust_security_binary()
    subprocess.run([str(bin_path), "keygen", "--key-file", str(path)], check=True)


def rotate_keys(path: Path) -> None:
    """Rotate the encryption keys and update the specified key file."""
    bin_path = _rust_security_binary()
    subprocess.run([str(bin_path), "rotate", "--key-file", str(path)], check=True)


def encrypt(key_file: Path, plaintext: str) -> str:
    """Encrypt the given plaintext using the specified key file."""
    bin_path = _rust_security_binary()
    result = subprocess.run(
        [
            str(bin_path),
            "encrypt",
            "--key-file",
            str(key_file),
            "--plaintext",
            plaintext,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def decrypt(key_file: Path, ciphertext: str) -> str:
    """Decrypt the given ciphertext using the specified key file."""
    bin_path = _rust_security_binary()


def validate() -> None:
    """Validate this bridge module is loadable.

    This is used by repository-level quality checks.
    """
    return
    result = subprocess.run(
        [
            str(bin_path),
            "decrypt",
            "--key-file",
            str(key_file),
            "--ciphertext",
            ciphertext,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()
