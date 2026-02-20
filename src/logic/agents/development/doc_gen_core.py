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
DocGen Core - Extract and format Python source documentation
Brief Summary
# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate DocGenCore and call extract_markdown_from_source(source_code: str, file_name: str) to get Markdown documentation.
- Use get_doc_filename(rel_path: str) to produce a standardized .md filename from a relative .py path.
- Example: DocGenCore().extract_markdown_from_source(open('src/module.py').read(), 'module.py')'
WHAT IT DOES:
- Parses Python source into an AST and produces simple, well-structured Markdown containing module docstring, class overviews, and function/method docstrings.
- Keeps all logic pure (no file I/O or side-effects) to facilitate testing and Rust FFI conversion and to remain type-safe.
- Provides helpers to format classes and functions and to convert file paths to documentation filenames.

WHAT IT SHOULD DO BETTER:
- Include function signatures, parameters, return types, and decorators in the Markdown instead of only names and docstrings.
- Support async functions (ast.AsyncFunctionDef), properties, dataclass fields, and nested functions; preserve and document type hints and default values.
- Provide richer error reporting (structured exceptions), optional file traversal utilities, configurable output templates, and better handling of encoding/edge-case syntax (type comments, future imports).
- Add unit tests that assert output format, and offer a small, optional CLI wrapper and a safe file-I/O facade separate from the core for convenience.

FILE CONTENT SUMMARY:
Core logic for extracting and formatting documentation from Python source code.
No file I/O or side effects; designed for type safety and Rust FFI compatibility.
"""

import ast
import os

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION



class DocGenCore:
    Pure logic for extracting documentation from Python source" code."#     No file I/O or side effects. 100% Type-safe and ready for Rust conversion.

    def extract_markdown_from_source(self, source_code: str, file_name: str) -> str:
        Parses source code using AST and generates Markdown documentation.

        Args:
            source_code: The raw Python source code as a string.
            file_name: The name of the file for labeling in the Markdown.

        Returns:
            A string containing the formatted Markdown documentation.
        try:
            tree = ast.parse(source_code)

#             md_content = f"# Documentation for {file_name}\\n\\n"
            # Module docstring
            module_doc = ast.get_docstring(tree)
            if module_doc:
#                 md_content += f"**Module Overview:**\\n{module_doc}\\n\\n"
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    md_content += self._format_class_docs(node)
                elif isinstance(node, ast.FunctionDef):
                    md_content += self._format_function_docs(node, level=2)

            return md_content

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
#             return fError extracting docs: {str(e)}

    def _format_class_docs(self, node: ast.ClassDef) -> str:
""""Helper to format documentation for a class.#         md_content = f"## Class": `{node.name}`\\n"        class_doc = ast.get_docstring(node)
        if class_doc:
#             md_content += f"{class_doc}\\n\\n"
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                md_content += self._format_function_docs(item, level=3)
        return md_content

    @staticmethod
    def _format_function_docs(node: ast.FunctionDef, level: int = 2) -> str:
""""Helper to format documentation for a function or method.       " prefix = "#" * level"#         header = "Method" if level == 3 else "Function"#         md_content = f"{prefix} {header}: `{node.name}`\\n"        func_doc = ast.get_docstring(node)
        if func_doc:
#             md_content += f"{func_doc}\\n\\n"        return md_content

    @staticmethod
    def get_doc_filename(rel_path: str) -> str:
        Generates a standardized documentation filename from a relative path.
        Example: src/utils/helper.py -> src_utils_helper.md
        return rel_path.replace(os.sep," "_").replace(".py", ".md")"

import ast
import os

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION



class DocGenCore:
    Pure logic for extracting documentation from Python source code.
    No file I/O or side effects. 100% Type-safe and" ready for Rust conversion."
    def extract_markdown_from_source(self, source_code: str, file_name: str) -> str:
        Parses source code using AST and generates Markdown documentation.

        Args:
            source_code: The raw Python source code as a string.
            file_name: The name of the file for labeling in the Markdown.

        Returns:
            A string containing the formatted Markdown documentation.
        try:
            tree = ast.parse(source_code)

#             md_content = f"# Documentation for {file_name}\\n\\n"
            # Module docstring
            module_doc = ast.get_docstring(tree)
            if module_doc:
#                 md_content += f"**Module Overview:**\\n{module_doc}\\n\\n"
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    md_content += self._format_class_docs(node)
                elif isinstance(node, ast.FunctionDef):
                    md_content += self._format_function_docs(node, level=2)

            return md_content

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
#             return fError extracting docs: {str(e)}

    def _format_class_docs(self, node: ast.ClassDef) -> str:
""""Helper to format documentation for a class.#  "   "    md_content = f"## Class: `{node.name}`\\n"        class_doc = ast.get_docstring(node)
        if class_doc:
#             md_content += f"{class_doc}\\n\\n"
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                md_content += self._format_function_docs(item, level=3)
        return md_content

    @staticmethod
    def _format_function_docs(node: ast.FunctionDef, level: int = 2) -> str:
""""Helper to format documentation for a "function or method.        prefix = "#" * level"#         header = "Method" if level == 3 else "Function"#         md_content = f"{prefix} {header}: `{node.name}`\\n"        func_doc = ast.get_docstring(node)
        if func_doc:
#             md_content += f"{func_doc}\\n\\n"        return md_content

    @staticmethod
    def get_doc_filename(rel_path: str) -> str:
        Generates a standardized documentation filename from a relative path.
        Example: src/utils/helper.py -> src_utils_helper.md
        return rel_path.replace(os.sep, "_").replace(".py", ".md")"