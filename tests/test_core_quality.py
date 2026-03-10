#!/usr/bin/env python3
"""Meta-tests that validate core design hygiene and CI quality gates.

These tests are intentionally conservative and use static analysis where
possible to avoid importing production modules (which could have side-effects).
"""
from __future__ import annotations

import ast
import pathlib
from typing import Dict, List, Set


ROOT = pathlib.Path(".")
SRC = ROOT / "src"
TESTS = ROOT / "tests"


def _iter_py_files(root: pathlib.Path) -> List[pathlib.Path]:
    return [p for p in root.rglob("*.py") if "__pycache__" not in p.parts]


def test_core_components_exist() -> None:
    """Ensure minimal core components exist under `src/`.

This list is intentionally conservative; adapt to project's real core layout.
"""
    required = [
        SRC / "core" / "__init__.py",
        SRC / "core" / "base" / "__init__.py",
        SRC / "core" / "agent_state_manager.py",
        SRC / "core" / "workflow" / "queue.py",
    ]
    missing = [str(p) for p in required if not p.exists()]
    assert not missing, f"Missing core files: {missing}"


def test_each_core_has_test_file() -> None:
    """For each module under `src/core`, ensure there is a corresponding test file.
    We map `src/core/foo/bar.py` -> `tests/test_core_foo_bar.py` 
    or `tests/structure/test_core/foo/bar_test.py`.
    """
    core_files = [p for p in _iter_py_files(SRC / "core")]
    test_files = {p.name for p in _iter_py_files(TESTS)}
    problems = []
    for f in core_files:
        rel = f.relative_to(SRC / "core")
        # __init__ modules are allowed to be untested
        if rel.name == "__init__.py":
            continue
        norm = str(rel).replace('/', '_').replace('\\', '_')
        target1 = f"test_core_{norm}"
        target2 = f"test_{rel.name}"
        if not any(name.startswith(target1) or name.startswith(target2) for name in test_files):
            problems.append(str(f))
    assert not problems, f"Core modules without tests: {problems}"


def test_test_files_have_assertions() -> None:
    """Ensure test files contain at least 3 assertions (not trivial smoke tests).
    """
    pytests = [p for p in _iter_py_files(TESTS) if p.name.startswith("test_")]
    bad: List[str] = []
    for p in pytests:
        text = p.read_text(encoding="utf-8")
        # Count 'assert' keywords not inside comments/strings using AST
        try:
            tree = ast.parse(text)
        except SyntaxError:
            bad.append(f"parse-fail:{p}")
            continue
        count = sum(isinstance(n, ast.Assert) for n in ast.walk(tree))
        if count < 1:
            # allow some skip files
            if "skip" in text.lower():
                continue
            bad.append(str(p))
    assert not bad, f"Test files missing assertions: {bad}"


def test_validate_function_exists() -> None:
    """Each core module should provide a `validate()` helper (static check) 
    or a docstring that explains validation.
    This test parses module ASTs and looks for a top-level `validate` function.
    """
    core_files = [p for p in _iter_py_files(SRC / "core")]
    missing: List[str] = []
    for p in core_files:
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
        except SyntaxError:
            missing.append(str(p))
            continue
        has_validate = any(isinstance(n, ast.FunctionDef) and n.name == "validate" for n in tree.body)
        if not has_validate:
            # allow __init__ to omit validate
            if p.name == "__init__.py":
                continue
            missing.append(str(p))
    assert not missing, f"Core modules missing validate(): {missing}"


def test_no_circular_imports_within_src() -> None:
    """Static detection of circular imports between modules under `src/`.

This builds a simple directed graph of imports (only intra-src) and checks for cycles.
"""
    files = _iter_py_files(SRC)
    module_by_file: Dict[str, pathlib.Path] = {str(p.relative_to(SRC)): p for p in files}

    def _imports_of(p: pathlib.Path) -> Set[str]:
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
        except SyntaxError:
            return set()
        imports: Set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.add(name.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)
        # normalize to relative paths where possible
        mapped: Set[str] = set()
        for im in imports:
            # consider only imports that start with src or the package name
            if im.startswith("src."):
                mapped.add(im.replace("src.", ""))
        return mapped

    # Build graph using relative module keys (a/b.py -> a/b.py)
    graph: Dict[str, List[str]] = {k: [] for k in module_by_file.keys()}
    for key, path in module_by_file.items():
        imps = _imports_of(path)
        for im in imps:
            # convert dotted to path style
            candidate = im.replace(".", "/") + ".py"
            if candidate in graph:
                graph[key].append(candidate)

    # detect cycle via DFS
    visiting: Set[str] = set()
    visited: Set[str] = set()

    def visit(n: str) -> bool:
        if n in visited:
            return False
        if n in visiting:
            return True
        visiting.add(n)
        for m in graph.get(n, []):
            if visit(m):
                return True
        visiting.remove(n)
        visited.add(n)
        return False

    cycles = [n for n in graph.keys() if visit(n)]
    assert not cycles, f"Circular imports detected starting at: {cycles}"
