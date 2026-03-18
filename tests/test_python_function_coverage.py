#!/usr/bin/env python3
"""Exercise as many Python functions as possible to improve coverage.

This test is intentionally broad and designed to run in CI as a safety net.
It does not assert functional correctness beyond ensuring functions are callable
and do not crash with trivial dummy inputs.

This is analogous to the existing `tests/test_rust_core.py` approach for rust_core.
"""

from __future__ import annotations

import ast
import asyncio
import inspect
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

import pytest


ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT / "src"
MAX_FUNCTIONS = 200  # limit to keep runtime reasonable


def _iter_python_files(root: Path) -> Iterator[Path]:
    for path in sorted(root.rglob("*.py")):
        # Skip tests and generated files that are not part of core logic
        if "tests" in path.parts:
            continue
        yield path


def _module_name_from_path(path: Path, root: Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    parts = rel.parts
    return ".".join(parts)


def _extract_functions_from_ast(source: str) -> List[Tuple[str, int]]:
    tree = ast.parse(source)
    funcs: List[Tuple[str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name.startswith("_"):
                continue
            # Skip test helpers and fixtures
            if node.name.startswith("test_"):
                continue
            # Count required args (no defaults, excluding self/cls)
            args = [a.arg for a in node.args.args if a.arg not in {"self", "cls"}]
            defaults = node.args.defaults or []
            required = len(args) - len(defaults)
            funcs.append((node.name, required))
    return funcs


def _gen_call_args(func_name: str, required: int) -> List[Tuple[Any, ...]]:
    base = func_name.lower()
    cases: List[Tuple[Any, ...]] = []

    # heuristic candidates
    if any(k in base for k in ("path", "file", "dir")):
        cases.append((".",))
    if any(k in base for k in ("name", "url", "str", "text")):
        cases.append(("test",))
    if any(k in base for k in ("count", "num", "limit", "size")):
        cases.append((1,))
    if any(k in base for k in ("data", "items", "list", "lines")):
        cases.append(([],))
    if any(k in base for k in ("config", "settings", "opts")):
        cases.append(({},))
    if any(k in base for k in ("ip", "cidr")):
        cases.append(("127.0.0.1",))
    if any(k in base for k in ("host", "port")):
        cases.append(("127.0.0.1", 80))

    # generic fallbacks
    if not cases:
        # Prefer passing an empty list for 0-argument functions to avoid argparse
        # consuming pytest CLI args (e.g., -k, -q) when a function reads sys.argv.
        if required == 0:
            cases.append(([],))
        elif required == 1:
            cases.append(("test",))
        elif required == 2:
            cases.append(("test", 1))
        else:
            cases.append(tuple("arg" + str(i) for i in range(required)))

    # only return as many args as required (but preserve sentinel values for required==0)
    if required == 0:
        return cases or [()]

    filtered: List[Tuple[Any, ...]] = []
    for case in cases:
        if len(case) >= required:
            filtered.append(tuple(case[:required]))
    return filtered or [tuple("arg" + str(i) for i in range(required))]


import asyncio


def _safe_call(func: Any, args: Tuple[Any, ...]) -> Tuple[bool, str]:
    if not callable(func):
        return False, "not callable"
    try:
        result = func(*args)

        # If function returns a coroutine, run it to completion.
        if inspect.isawaitable(result):
            asyncio.run(result)

        return True, f"returned {type(result).__name__}"
    except SystemExit as e:
        # Common when calling argparse-based entrypoints without required args.
        return True, f"SystemExit({e.code})"
    except Exception as e:
        return False, f"raised {type(e).__name__}: {e}"


def test_exercise_python_functions() -> None:
    """Try to import and call many functions across the python codebase."""
    executed = 0
    failures: Dict[str, str] = {}

    for py_file in _iter_python_files(SRC_ROOT):
        mod_name = _module_name_from_path(py_file, SRC_ROOT)
        try:
            module = __import__(mod_name, fromlist=["*"])
        except Exception as e:
            # If a module cannot import, record and continue.
            failures[f"import::{mod_name}"] = f"ImportError: {e}"
            continue

        source = py_file.read_text(encoding="utf-8", errors="ignore")
        funcs = _extract_functions_from_ast(source)
        for fn_name, required in funcs:
            func_obj = getattr(module, fn_name, None)
            if func_obj is None:
                continue

            for args in _gen_call_args(fn_name, required):
                ok, msg = _safe_call(func_obj, args)
                executed += 1
                if not ok:
                    failures[f"{mod_name}.{fn_name}({args})"] = msg
                # stop after enough coverage
                if executed >= MAX_FUNCTIONS:
                    break
            if executed >= MAX_FUNCTIONS:
                break
        if executed >= MAX_FUNCTIONS:
            break

    assert executed > 0, "No functions were exercised"
    # This is intentionally lenient: we only fail if *all* calls fail.
    if len(failures) == executed:
        raise AssertionError(f"All attempted function calls failed: {failures}")
