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

"""Red-phase workspace unification contract tests for prj0000117."""

import tomllib
from pathlib import Path


def _repo_root() -> Path:
    """Return the repository root path.

    Returns:
        Path: Repository root directory.

    """
    return Path(__file__).resolve().parents[2]


def _load_toml(path: Path) -> dict:
    """Load a TOML file into a Python dictionary.

    Args:
        path: TOML file path.

    Returns:
        dict: Parsed TOML mapping.

    """
    with path.open("rb") as file_handle:
        return tomllib.load(file_handle)


def _has_patch_crates_io(toml_data: dict) -> bool:
    """Return whether TOML contains a patch.crates-io block.

    Args:
        toml_data: Parsed TOML mapping.

    Returns:
        bool: True when patch.crates-io exists.

    """
    patch_section = toml_data.get("patch", {})
    return isinstance(patch_section, dict) and isinstance(patch_section.get("crates-io"), dict)


def test_root_manifest_declares_workspace_members_for_target_subcrates() -> None:
    """Assert root Cargo.toml declares workspace members for crdt, p2p, security.

    This enforces AC-WS-001 and should fail in red phase until [workspace]
    members are introduced in rust_core/Cargo.toml.

    """
    root_manifest = _load_toml(_repo_root() / "rust_core" / "Cargo.toml")
    workspace_block = root_manifest.get("workspace", {})

    assert isinstance(workspace_block, dict), "rust_core/Cargo.toml must define a [workspace] mapping"
    members = workspace_block.get("members", [])
    assert isinstance(members, list), "rust_core/Cargo.toml [workspace].members must be a list"

    expected_members = {"crdt", "p2p", "security"}
    assert expected_members.issubset(set(members)), (
        "rust_core/Cargo.toml [workspace].members must include 'crdt', 'p2p', and 'security'"
    )


def test_root_workspace_lockfile_is_single_authoritative_lockfile() -> None:
    """Assert lockfile strategy is root-only for workspace members.

    This enforces AC-WS-002 and should fail in red phase while member-level
    lockfiles still exist under rust_core/crdt, rust_core/p2p, or rust_core/security.

    """
    root = _repo_root()
    root_lockfile = root / "rust_core" / "Cargo.lock"
    member_lockfiles = [
        root / "rust_core" / "crdt" / "Cargo.lock",
        root / "rust_core" / "p2p" / "Cargo.lock",
        root / "rust_core" / "security" / "Cargo.lock",
    ]

    assert root_lockfile.exists(), "rust_core/Cargo.lock must exist as the canonical workspace lockfile"
    unexpected_member_locks = [str(path.relative_to(root)) for path in member_lockfiles if path.exists()]
    assert not unexpected_member_locks, (
        f"Workspace lockfile contract violation: member lockfiles must be removed. Found: {unexpected_member_locks}"
    )


def test_root_manifest_keeps_package_and_benchmark_contract() -> None:
    """Assert root package and benchmark contract remain compatible.

    This enforces AC-WS-003 and AC-WS-004 at structure level without running
    heavy builds.

    """
    root_manifest = _load_toml(_repo_root() / "rust_core" / "Cargo.toml")

    package_block = root_manifest.get("package", {})
    assert isinstance(package_block, dict), "rust_core/Cargo.toml must keep a [package] block"
    assert package_block.get("name") == "rust_core", "rust_core/Cargo.toml package.name must remain rust_core"

    bench_entries = root_manifest.get("bench", [])
    assert isinstance(bench_entries, list), "rust_core/Cargo.toml [[bench]] declarations must be a list"
    stats_baseline_entry = next(
        (entry for entry in bench_entries if isinstance(entry, dict) and entry.get("name") == "stats_baseline"),
        None,
    )
    assert stats_baseline_entry is not None, "rust_core/Cargo.toml must retain [[bench]] name='stats_baseline'"
    assert stats_baseline_entry.get("harness") is False, "stats_baseline bench must keep harness=false"


def test_patch_governance_is_root_owned_not_member_owned() -> None:
    """Assert patch.crates-io governance is root-owned for workspace policy.

    This enforces AC-WS-006 and should fail in red phase when patch overrides
    are still crate-local or absent at the root workspace manifest.

    """
    root = _repo_root()
    root_manifest = _load_toml(root / "rust_core" / "Cargo.toml")
    p2p_manifest = _load_toml(root / "rust_core" / "p2p" / "Cargo.toml")
    crdt_manifest = _load_toml(root / "rust_core" / "crdt" / "Cargo.toml")
    security_manifest = _load_toml(root / "rust_core" / "security" / "Cargo.toml")

    assert _has_patch_crates_io(root_manifest), (
        "rust_core/Cargo.toml must own [patch.crates-io] for workspace-wide dependency overrides"
    )
    assert not _has_patch_crates_io(p2p_manifest), "rust_core/p2p/Cargo.toml must not own [patch.crates-io]"
    assert not _has_patch_crates_io(crdt_manifest), "rust_core/crdt/Cargo.toml must not own [patch.crates-io]"
    assert not _has_patch_crates_io(security_manifest), "rust_core/security/Cargo.toml must not own [patch.crates-io]"
