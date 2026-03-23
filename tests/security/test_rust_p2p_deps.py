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
"""
tests/security/test_rust_p2p_deps.py

Security regression tests for prj0000049 (dependabot-security-fixes).

These tests assert that known-vulnerable dependency versions are NOT present
in rust_core/p2p/Cargo.lock, and that Cargo.toml references libp2p >= 0.56.

Pre-fix state (EXPECTED FAILURES):
  - Cargo.lock contains yamux 0.10.2, ring 0.16.20, idna 0.2.3,
    ed25519-dalek 1.0.1, curve25519-dalek 3.2.1, snow 0.9.3
  - Cargo.toml references libp2p 0.49

Post-fix state (EXPECTED PASSES):
  - All vulnerable versions replaced via libp2p 0.56 upgrade
"""
import re
import pytest
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent.parent
P2P_DIR = REPO_ROOT / "rust_core" / "p2p"
CARGO_LOCK = P2P_DIR / "Cargo.lock"
CARGO_TOML = P2P_DIR / "Cargo.toml"

# ---------------------------------------------------------------------------
# Vulnerable (package, version) pairs — CVEs from Dependabot alert prj0000049
# ---------------------------------------------------------------------------
VULNERABLE_VERSIONS = [
    ("yamux", "0.10.2"),        # GHSA-4jwc-w2hc-78qv — DoS via memory exhaustion
    ("ring", "0.16.20"),        # GHSA-48mm-762m-2xpm — RSA primitive exposure
    ("idna", "0.2.3"),          # GHSA-crh6-fp67-6883 — Unicode spoofing
    ("ed25519-dalek", "1.0.1"),  # GHSA-3f4c-fmq5-gfq7 — Weak signature check
    ("curve25519-dalek", "3.2.1"),  # GHSA-x62c-6mxr-74fh — Timing side-channel
    ("snow", "0.9.3"),          # GHSA-qg5g-gv98-5ffh — Memory safety in Noise
]


def _parse_lock_packages(lock_text: str) -> list[tuple[str, str]]:
    """Return list of (name, version) tuples from Cargo.lock text."""
    packages = []
    for block in lock_text.split("[[package]]"):
        name_match = re.search(r'name\s*=\s*"([^"]+)"', block)
        version_match = re.search(r'version\s*=\s*"([^"]+)"', block)
        if name_match and version_match:
            packages.append((name_match.group(1), version_match.group(1)))
    return packages


# ---------------------------------------------------------------------------
# Cargo.lock tests — will FAIL before fix, PASS after fix
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def cargo_lock_packages():
    """Parse Cargo.lock and return (name, version) list, or skip if missing."""
    if not CARGO_LOCK.exists():
        pytest.skip("Cargo.lock not yet generated — run `cargo generate-lockfile` in rust_core/p2p/")
    return _parse_lock_packages(CARGO_LOCK.read_text(encoding="utf-8"))


@pytest.mark.parametrize("pkg,vuln_version", VULNERABLE_VERSIONS)
def test_vulnerable_version_not_in_cargo_lock(cargo_lock_packages, pkg, vuln_version):
    """Assert that the known-vulnerable version of each package is NOT in Cargo.lock.

    This test FAILS before prj0000049 is applied (vulnerable versions present)
    and PASSES after the libp2p 0.56 upgrade removes them.
    """
    present = (pkg, vuln_version) in cargo_lock_packages
    assert not present, (
        f"SECURITY: {pkg} {vuln_version} is a known-vulnerable version "
        f"and must be removed. Upgrade libp2p to 0.56 to remediate. "
        f"See docs/project/prj0000049/dependabot-security-fixes.design.md"
    )


# ---------------------------------------------------------------------------
# Cargo.toml test — will FAIL before fix, PASS after fix
# ---------------------------------------------------------------------------

def test_libp2p_version_is_056_in_cargo_toml():
    """Assert Cargo.toml declares libp2p version 0.56 (not the vulnerable 0.49).

    This test FAILS before prj0000049 is applied and PASSES after.
    """
    assert CARGO_TOML.exists(), f"Cargo.toml not found at {CARGO_TOML}"
    content = CARGO_TOML.read_text(encoding="utf-8")

    # Must contain the safe version
    assert '"0.56"' in content, (
        f'Cargo.toml must declare libp2p version "0.56". '
        f'Currently contains: {_extract_libp2p_version(content)!r}. '
        f'See docs/project/prj0000049/dependabot-security-fixes.design.md'
    )

    # Must NOT contain the vulnerable version
    assert '"0.49"' not in content, (
        'Cargo.toml still references libp2p "0.49" which pulls in 6 vulnerable '
        'transitive dependencies. Upgrade to "0.56".'
    )


def _extract_libp2p_version(toml_text: str) -> str | None:
    """Extract the libp2p version string from Cargo.toml content."""
    match = re.search(r'libp2p\s*=\s*\{[^}]*version\s*=\s*"([^"]+)"', toml_text)
    return match.group(1) if match else None
