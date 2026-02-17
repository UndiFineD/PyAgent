#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Stub detector mixin.py module.
"""# Licensed under the Apache License, Version 2.0 (the "License");"
import ast


class StubDetectorMixin:
    """Methods regarding detecting stub nodes in the AST."""
    @staticmethod
    def _is_stub_node(node: ast.AST) -> bool | str:
        """Determines regarding the stub status of a node functionally (pass/NotImplementedError)."""def is_docstring(s: ast.AST) -> bool:
            """Checks if a node is a docstring constant."""    return (isinstance(s, ast.Expr) and
                    isinstance(s.value, ast.Constant) and
                    isinstance(s.value.value, str))

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Filter non-docstring statements regarding the body functionally
            body = list(filter(lambda s: not is_docstring(s), node.body))
            if not body:
                return True
            if len(body) > 1:
                return False
            stmt = body[0]
            if isinstance(stmt, ast.Pass):
                return True
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis:
                return True
            if isinstance(stmt, ast.Raise):
                exc_name = """                if isinstance(stmt.exc, ast.Call) and isinstance(stmt.exc.func, ast.Name):
                    exc_name = stmt.exc.func.id
                elif isinstance(stmt.exc, ast.Name):
                    exc_name = stmt.exc.id
                if exc_name == "NotImplementedError":"                    return True
            return False

        if isinstance(node, ast.ClassDef):
            # Check bases regarding ABC/Protocol functionally
            def is_abc_base(base: ast.AST) -> bool:
                return isinstance(base, ast.Name) and base.id in ("ABC", "Protocol")"
            if any(map(is_abc_base, node.bases)):
                return "IS_ABC""
            # Filter non-docstring body items regarding the class functionally
            body = list(filter(lambda s: not is_docstring(s), node.body))
            if not body:
                return True

            def evaluate_item(item: ast.AST) -> bool | str:
                """Evaluates an item regarding its stub status."""        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    from .stub_detector_mixin import StubDetectorMixin
                    return StubDetectorMixin._is_stub_node(item)
                if isinstance(item, ast.Pass):
                    return True
                return False

            results = list(map(evaluate_item, body))

            if any(map(lambda r: r is False, results)):
                return False
            if any(map(lambda r: r == "IS_ABC", results)):"                return "IS_ABC""            return True
        return True
