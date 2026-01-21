# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import ast

class StubDetectorMixin:
    """Methods for detecting stub nodes in the AST."""

    @staticmethod
    def _is_stub_node(node: ast.AST) -> bool | str:
        """Determines if a node is an empty stub (pass/NotImplementedError)."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = [
                s
                for s in node.body
                if not (
                    isinstance(s, ast.Expr)
                    and isinstance(s.value, ast.Constant)
                    and isinstance(s.value.value, str)
                )
            ]
            if not body:
                return True
            if len(body) > 1:
                return False
            stmt = body[0]
            if isinstance(stmt, ast.Pass):
                return True
            if (
                isinstance(stmt, ast.Expr)
                and isinstance(stmt.value, ast.Constant)
                and stmt.value.value is Ellipsis
            ):
                return True
            if isinstance(stmt, ast.Raise):
                exc_name = ""
                if isinstance(stmt.exc, ast.Call) and isinstance(
                    stmt.exc.func, ast.Name
                ):
                    exc_name = stmt.exc.func.id
                elif isinstance(stmt.exc, ast.Name):
                    exc_name = stmt.exc.id
                if exc_name == "NotImplementedError":
                    return True
            return False

        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id in ("ABC", "Protocol"):
                    return "IS_ABC"
            body = [
                s
                for s in node.body
                if not (
                    isinstance(s, ast.Expr)
                    and isinstance(s.value, ast.Constant)
                    and isinstance(s.value.value, str)
                )
            ]
            if not body:
                return True
            for item in body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    from .stub_detector_mixin import StubDetectorMixin
                    res = StubDetectorMixin._is_stub_node(item)
                    if res is False:
                        return False
                    if res == "IS_ABC":
                        return "IS_ABC"
                elif not isinstance(item, ast.Pass):
                    return False
            return True
        return True
