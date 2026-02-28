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

"""Pure-Python fallback shim for the native `rust_core` extension.

This module provides minimal implementations of the functions used by
`src.logic.agents.cognitive.context.engines.graph_core.GraphCore` so the
test-suite can import and run without a compiled Rust extension present.

The implementations use the existing AST-based Python logic; they are
intended as compatibility shims for test environments only.
"""

from __future__ import annotations

import ast
from typing import Any, Dict, Iterable, List, Tuple


def _analyze_python(content: str) -> Tuple[List[str], List[Tuple[str, str]], List[str]]:
    """Return (imports, classes-as-(name,bases_csv), calls).

    Classes are returned as (name, bases_csv) for compatibility with the
    expected rust extension output shape.
    """

    class Visitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.imports: set[str] = set()
            self.classes: List[Tuple[str, List[str]]] = []
            self.calls: set[str] = set()

        def visit_Import(self, node: ast.Import) -> None:  # pragma: no cover - tiny helper
            for alias in node.names:
                self.imports.add(alias.name)

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # pragma: no cover - tiny helper
            if node.module:
                self.imports.add(node.module)

        def visit_ClassDef(self, node: ast.ClassDef) -> None:  # pragma: no cover - tiny helper
            bases: List[str] = []
            for base in node.bases:
                if isinstance(base, ast.Name):
                    bases.append(base.id)
                elif isinstance(base, ast.Attribute):
                    bases.append(base.attr)
            self.classes.append((node.name, bases))
            self.generic_visit(node)

        def visit_Call(self, node: ast.Call) -> None:  # pragma: no cover - tiny helper
            if isinstance(node.func, ast.Name):
                self.calls.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                self.calls.add(node.func.attr)
            self.generic_visit(node)

    try:
        tree = ast.parse(content)
    except Exception:
        return [], [], []

    visitor = Visitor()
    visitor.visit(tree)

    # Convert classes bases list to comma-joined string for compatibility
    classes_out: List[Tuple[str, str]] = []
    for name, bases in visitor.classes:
        classes_out.append((name, ",".join(bases)))

    return list(visitor.imports), classes_out, list(visitor.calls)


def extract_graph_entities_regex(content: str) -> Dict[str, Any]:
    """Mimic the Rust extractor: return imports, classes, and calls.

    Returns a dict with keys: `imports`, `classes` and `calls`. `classes`
    is a list of tuples (name, bases_csv) to match the Rust output shape.
    """
    imports, classes, calls = _analyze_python(content)
    return {"imports": imports, "classes": classes, "calls": calls}


def build_graph_edges_rust(rel_path: str, imports: Iterable[str], inherits_list: Iterable[Tuple[str, Any]]) -> List[Tuple[str, str, str]]:
    """Build edges in the same format the Rust helper would return.

    `inherits_list` is expected as an iterable of (class_name, bases) where
    `bases` may be a sequence or a comma-separated string.
    """
    edges: List[Tuple[str, str, str]] = []

    for imp in imports:
        edges.append((rel_path, imp, "imports"))

    for cls, bases in inherits_list:
        if bases is None:
            continue
        # accept both list-like and comma-separated strings
        if isinstance(bases, (list, tuple)):
            base_iter = bases
        else:
            base_iter = [b.strip() for b in str(bases).split(",") if b.strip()]

        for base in base_iter:
            edges.append((f"{rel_path}::{cls}", base, "inherits"))

    return edges
