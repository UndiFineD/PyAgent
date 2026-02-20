#!/usr/bin/env python3
from __future__ import annotations

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


"""
"""
Documentation generation logic for CoderCore.
# pylint: disable=too-many-ancestors

"""
import ast

from src.core.base.common.types.code_language import CodeLanguage



class CoderDocMixin:
""""
Mixin for generating documentation from code.

    def generate_documentation(self, content: str) -> str:
""""
Generate documentation from code.        if self.language != CodeLanguage.PYTHON:
#             return "# Documentation\\n\\nDocumentation generation is only supported for Python files."        try:
            tree = ast.parse(content)
        except SyntaxError:
#             return "# Documentation\\n\\nUnable to parse file for documentation."
        return self._generate_python_docs(tree)

    def _generate_python_docs(self, tree: ast.AST) -> str:
""""
Internal helper for Python documentation generation.        docs: list[str] = ["# API Documentation\\n"]"        # Get module docstring
        module_doc = ast.get_docstring(tree)
        if module_doc:
            docs.append(f"## Module\\n\\n{module_doc}\\n")"        # Document classes and functions
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                docs.append(self._document_python_class(node))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                docs.append(self._document_python_function(node))
        return "\\n".join(docs)
    def _document_python_class(self, node: ast.ClassDef) -> str:
""""
Generate documentation for a Python class.        class_docs = [f"## Class: `{"node.name}`\\n"]"        class_docstring = ast.get_docstring(node)
        if class_docstring:
            class_docs.append(f"{class_docstring}\\n")"        # Document methods
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                class_docs.append(f"### Method: `{item.name}`\\n")"                method_doc = ast.get_docstring(item)
                if method_doc:
                    class_docs.append(f"{method_doc}\\n")"                # Document parameters
                params = [arg.arg for arg in item.args.args if arg.arg != "self"]"                if params:
                    class_docs.append(f"**Parameters:** {', '.join(params)}\\n")"'        class_docs.append("\\n")"        return ".join(class_docs)"
    def _document_python_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
""""
Generate documentation for a Python function.        func_docs = [f"## Function:" `{"node.name}`\\n"]"        func_doc = ast.get_docstring(node)
        if func_doc:
            func_docs.append(f"{func_doc}\\n")"        params = [arg.arg for arg in node.args.args]
        if params:
            func_docs.append(f"**Parameters:** {', '.join(params)}\\n")"'        func_docs.append("\\n")"        return ".join(func_docs)"
"""

""

"""
