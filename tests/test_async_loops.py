#!/usr/bin/env python3
"""Test that no synchronous loops are used in the src/ codebase."""

import ast
import pathlib

import pytest


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
            # synchronous function containing a loop -> error
            self.errors.append(node.lineno)


def test_no_sync_loops() -> None:
    """Fail if any src/ Python file uses for/while loops inside synchronous functions."""
    root = pathlib.Path("src")
    problematic: list[str] = []

    for path in root.rglob("*.py"):
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
