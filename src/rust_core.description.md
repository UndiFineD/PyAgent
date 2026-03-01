# rust_core

**File**: `src\rust_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 3 functions, 7 imports  
**Lines**: 118  
**Complexity**: 8 (moderate)

## Overview

Pure-Python fallback shim for the native `rust_core` extension.

This module provides minimal implementations of the functions used by
`src.logic.agents.cognitive.context.engines.graph_core.GraphCore` so the
test-suite can import and run without a compiled Rust extension present.

The implementations use the existing AST-based Python logic; they are
intended as compatibility shims for test environments only.

## Classes (1)

### `Visitor`

**Inherits from**: NodeVisitor

Class Visitor implementation.

**Methods** (5):
- `__init__(self)`
- `visit_Import(self, node)`
- `visit_ImportFrom(self, node)`
- `visit_ClassDef(self, node)`
- `visit_Call(self, node)`

## Functions (3)

### `_analyze_python(content)`

Return (imports, classes-as-(name,bases_csv), calls).

Classes are returned as (name, bases_csv) for compatibility with the
expected rust extension output shape.

### `extract_graph_entities_regex(content)`

Mimic the Rust extractor: return imports, classes, and calls.

Returns a dict with keys: `imports`, `classes` and `calls`. `classes`
is a list of tuples (name, bases_csv) to match the Rust output shape.

### `build_graph_edges_rust(rel_path, imports, inherits_list)`

Build edges in the same format the Rust helper would return.

`inherits_list` is expected as an iterable of (class_name, bases) where
`bases` may be a sequence or a comma-separated string.

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `ast`
- `typing.Any`
- `typing.Dict`
- `typing.Iterable`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
