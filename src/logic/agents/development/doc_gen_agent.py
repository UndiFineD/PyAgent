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

# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Doc gen agent.py module.
"""

# pylint: disable=too-many-ancestors


from __future__ import annotations

import ast
import os
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class DocGenAgent(BaseAgent):
    """
    Autonomous Documentation Generator: Extracts docstrings from Python modules
    and generates Markdown files compatible with Sphinx/Jekyll.
    """

    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.doc_registry: dict[Any, Any] = {}  # module_path -> extracted_docs

    def extract_docs(self, file_path: str) -> str:
        """Extracts docstrings from a Python file and returns Markdown content."""
        if not file_path.endswith(".py"):
            return ""

        try:
            with open(file_path, encoding="utf-8") as f:
                tree = ast.parse(f.read())

            md_content = f"# Documentation for {os.path.basename(file_path)}\n\n"

            # Module docstring
            module_doc = ast.get_docstring(tree)
            if module_doc:
                md_content += f"**Module Overview:**\n{module_doc}\n\n"

            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    md_content += self._format_class_docs(node)
                elif isinstance(node, ast.FunctionDef):
                    md_content += self._format_function_docs(node, level=2)

            self.doc_registry[file_path] = md_content
            return md_content

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            return f"Error extracting docs: {str(e)}"

    def _format_class_docs(self, node: ast.ClassDef) -> str:
        """Helper to format documentation for a class."""
        md_content = f"## Class: `{node.name}`\n"
        class_doc = ast.get_docstring(node)
        if class_doc:
            md_content += f"{class_doc}\n\n"

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                md_content += self._format_function_docs(item, level=3)
        return md_content

    @staticmethod
    def _format_function_docs(node: ast.FunctionDef, level: int = 2) -> str:
        """Helper to format documentation for a function or method."""
        prefix = "#" * level
        header = "Method" if level == 3 else "Function"
        md_content = f"{prefix} {header}: `{node.name}`\n"
        func_doc = ast.get_docstring(node)
        if func_doc:
            md_content += f"{func_doc}\n\n"
        return md_content

    def generate_documentation_site(self, output_dir: str) -> int:
        """Generates documentation files for all modules in the registry."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for file_path, content in self.doc_registry.items():
            rel_path = os.path.relpath(file_path, self.workspace_path)
            doc_filename = rel_path.replace(os.sep, "_").replace(".py", ".md")
            with open(os.path.join(output_dir, doc_filename), "w", encoding="utf-8") as f:
                f.write(content)

        return len(self.doc_registry)