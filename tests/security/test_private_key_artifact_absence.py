"""Red-phase tests that enforce active-tree private key artifact absence."""

from __future__ import annotations

from pathlib import Path

PRIVATE_KEY_ARTIFACT_PATH = Path("rust_core/2026-03-11-keys.priv")


def test_active_tree_excludes_private_key_artifact_path() -> None:
    """Verify active tree no longer contains the known leaked key artifact path."""
    assert not PRIVATE_KEY_ARTIFACT_PATH.exists()
