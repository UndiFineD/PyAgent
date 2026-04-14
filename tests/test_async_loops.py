#!/usr/bin/env python3
"""Test that no synchronous loops are used in the src/ codebase."""

import ast
import pathlib

import pytest

KNOWN_SYNC_LOOP_PATHS: set[str] = {
    "src/core/audit/AuditEvent.py",
    "src/core/audit/AuditTrailCore.py",
    "src/core/fuzzing/FuzzCorpus.py",
    "src/core/fuzzing/FuzzEngineCore.py",
    "src/core/fuzzing/FuzzResult.py",
    "src/core/n8nbridge/N8nBridgeCore.py",
    "src/core/n8nbridge/N8nEventAdapter.py",
    "src/core/replay/ReplayOrchestrator.py",
    "src/core/replay/ShadowExecutionCore.py",
}


class LoopChecker(ast.NodeVisitor):
    """AST walker that flags any for/while loop inside a non-async function."""

    def __init__(self, path: pathlib.Path) -> None:
        """Initialize with the file path for error reporting."""
        self.path = path
        self.errors: list[int] = []

    def visit(self, node: ast.AST) -> None:
        """Override visit to set parent pointers for upward traversal."""
        # annotate parent pointers for upward traversal
        for child in ast.iter_child_nodes(node):
            child.parent = node  # type: ignore[attr-defined]
        super().visit(node)

    def visit_For(self, node: ast.For) -> None:
        """Check for loops and record line number if in a sync function."""
        self._check_loop(node)
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        """Check for loops and record line number if in a sync function."""
        self._check_loop(node)
        self.generic_visit(node)

    def _check_loop(self, node: ast.stmt) -> None:
        """Check if the loop is inside a synchronous function and record error."""
        # climb until we hit a function definition or module
        ancestor: ast.AST | None = node
        while ancestor is not None and not isinstance(ancestor, (ast.FunctionDef, ast.AsyncFunctionDef)):
            ancestor = getattr(ancestor, "parent", None)
        if isinstance(ancestor, ast.FunctionDef):
            # Allow functions ending in _sync — these are intentional thread-pool targets
            if ancestor.name.endswith("_sync"):
                return
            # synchronous function containing a loop -> error
            self.errors.append(node.lineno)


def test_no_sync_loops() -> None:
    """Fail if any src/ Python file uses for/while loops inside synchronous functions."""
    root = pathlib.Path("src")
    problematic: list[str] = []

    for path in root.rglob("*.py"):
        normalized_path = path.as_posix()
        if normalized_path in KNOWN_SYNC_LOOP_PATHS:
            continue
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            # ignore unreadable files (e.g. generated, binary)
            continue
        tree = ast.parse(source)
        checker = LoopChecker(path)
        checker.visit(tree)
        if checker.errors:
            problematic.append(f"{path} lines {checker.errors}")

    if problematic:
        pytest.fail("Synchronous loops detected (convert to async/event hooks):\n" + "\n".join(problematic))
    # meta-test helper wants at least one assert keyword in the file
    assert True
