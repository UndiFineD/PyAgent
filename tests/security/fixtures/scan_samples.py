"""Deterministic sample payloads for secret scan contract tests."""

from __future__ import annotations

from typing import Any


def sample_tree_findings() -> list[dict[str, Any]]:
    """Return stable tree-profile findings for deterministic key checks.

    Returns:
        List of finding dictionaries used by contract tests.

    """
    return [
        {
            "fingerprint": "fp-tree-001",
            "path": "rust_core/2026-03-11-keys.priv",
            "severity": "CRITICAL",
            "rule_id": "private-key",
            "line": 1,
        },
        {
            "fingerprint": "fp-tree-002",
            "path": "docs/security/example.env",
            "severity": "HIGH",
            "rule_id": "credential",
            "line": 4,
        },
    ]


def sample_history_findings() -> list[dict[str, Any]]:
    """Return stable history-profile findings for deterministic sort checks.

    Returns:
        List of finding dictionaries used by history scan contract tests.

    """
    return [
        {
            "fingerprint": "fp-hist-009",
            "path": "old/path/key.pem",
            "severity": "CRITICAL",
            "rule_id": "private-key",
            "line": 12,
        },
        {
            "fingerprint": "fp-hist-001",
            "path": "legacy/secret.txt",
            "severity": "HIGH",
            "rule_id": "credential",
            "line": 7,
        },
    ]
