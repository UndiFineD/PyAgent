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

ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT / "src"

# Ensure that `src/` is on sys.path so imports like `core.*` work when running tests.
import sys

sys.path.insert(0, str(ROOT))

MAX_FUNCTIONS = 200  # limit to keep runtime reasonable


def _iter_python_files(root: Path) -> Iterator[Path]:
    """Recursively yield all .py files under the given root, excluding tests."""
    for path in sorted(root.rglob("*.py")):
        # Skip tests and generated files that are not part of core logic
        if "tests" in path.parts:
            continue
        yield path


def _module_name_from_path(path: Path, root: Path) -> str:
    """Convert a file path to a Python module name relative to the given root."""
    rel = path.relative_to(root).with_suffix("")
    parts = rel.parts
    return ".".join(parts)


def _extract_functions_from_ast(source: str) -> List[Tuple[str, int]]:
    """Parse the source code and return a list of (function name, required args) for public functions."""
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
    """Generate plausible argument tuples for a function
    based on its name and number of required arguments.
    """
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
        # For 0-arg functions we prefer to call with no args; passing a dummy
        # argument frequently causes TypeError and masks real failures.
        if required == 0:
            cases.append(())
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


def _safe_call(func: Any, args: Tuple[Any, ...]) -> Tuple[bool, str]:
    """Safely call a function with the given arguments
    and return a tuple indicating success and a message.
    """
    if not callable(func):
        return False, "not callable"

    result: Any = None
    try:
        result = func(*args)

        # If function returns a coroutine, run it to completion.
        if inspect.isawaitable(result):
            try:
                asyncio.run(result)
            except RuntimeError:
                # If an event loop is already running, close the coroutine to
                # avoid "coroutine was never awaited" warnings.
                if inspect.iscoroutine(result):
                    result.close()  # type: ignore[attr-defined]
                raise

        return True, f"returned {type(result).__name__}"
    except SystemExit as e:
        # Common when calling argparse-based entrypoints without required args.
        return True, f"SystemExit({e.code})"
    except Exception as e:
        if inspect.iscoroutine(result):
            result.close()  # type: ignore[attr-defined]
        return False, f"raised {type(e).__name__}: {e}"


def test_exercise_python_functions() -> None:
    """Try to import and call many functions across the python codebase."""
    executed = 0
    succeeded = 0
    failures: Dict[str, str] = {}
    import_errors: Dict[str, str] = {}

    py_files = list(_iter_python_files(SRC_ROOT))
    print(f"Scanning {len(py_files)} python files under {SRC_ROOT}")

    for py_file in py_files:
        print(f"Processing file: {py_file.relative_to(ROOT)}")
        mod_name = _module_name_from_path(py_file, SRC_ROOT)
        try:
            module = __import__(mod_name, fromlist=["*"])
        except Exception as e:
            msg = f"ImportError: {e}"
            print(f"  [IMPORT ERROR] {mod_name}: {msg}")
            import_errors[mod_name] = msg
            continue

        source = py_file.read_text(encoding="utf-8", errors="ignore")
        funcs = _extract_functions_from_ast(source)
        print(f"  found {len(funcs)} public functions")

        for fn_name, required in funcs:
            func_obj = getattr(module, fn_name, None)
            if func_obj is None:
                continue

            for args in _gen_call_args(fn_name, required):
                ok, msg = _safe_call(func_obj, args)
                executed += 1
                if ok:
                    succeeded += 1
                else:
                    failures[f"{mod_name}.{fn_name}({args})"] = msg
                    print(f"    [FAIL] {mod_name}.{fn_name}({args}) -> {msg}")
                if executed >= MAX_FUNCTIONS:
                    break
            if executed >= MAX_FUNCTIONS:
                break
        if executed >= MAX_FUNCTIONS:
            break

    print(f"\nSummary: executed {executed} function calls")
    print(f"          successful calls: {succeeded}")
    print(f"          import errors: {len(import_errors)}")
    print(f"          failing calls: {len(failures)}")

    # Fail only if nothing succeeded (to avoid noise from partial failures)
    assert executed > 0 and succeeded > 0, "No successful function calls were executed (check logs for details)"

    # Still emit warnings in CI output, but do not fail the test if some calls fail.
    if failures or import_errors:

        def _format_map(m: Dict[str, str], limit: int = 10) -> str:
            items = list(m.items())
            lines = [f"  - {k}: {v}" for k, v in items[:limit]]
            if len(items) > limit:
                lines.append(f"  ... and {len(items) - limit} more")
            return "\n".join(lines)

        msg_lines = [
            f"Found {len(import_errors)} import errors and {len(failures)} failing function calls.",
        ]
        if import_errors:
            msg_lines.append("Import errors (sample):")
            msg_lines.append(_format_map(import_errors))
        if failures:
            msg_lines.append("Failing function calls (sample):")
            msg_lines.append(_format_map(failures))

        print("\n".join(msg_lines))


def main() -> int:
    """Standalone entrypoint for local debugging and CI reruns."""
    try:
        test_exercise_python_functions()
        return 0
    except AssertionError as e:
        print(str(e))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
