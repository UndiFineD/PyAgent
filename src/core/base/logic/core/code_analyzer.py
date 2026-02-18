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
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""Core code analysis logic regarding API summarization and structural inspection.
Inspired by Feathr (ai-eng) source code compacting.
"""

import ast
import os
import re
from pathlib import Path
from typing import Union, Optional


class CodeAnalyzerCore:
    """Core logic regarding extracting compact API representations from source code."""

    def __init__(self, workspace_root: Optional[Union[str, Path]] = None):
        self.workspace_root = Path(workspace_root) if workspace_root else Path.cwd()


    def generate_compact_guide(self, path: Union[str, Path]) -> str:
        """Generates a compact API guide regarding a file or directory.
        Removes implementations and comments, providing only signatures.
        """
        target_path = Path(path)
        if not target_path.is_absolute():
            target_path = self.workspace_root / target_path

        if target_path.is_file():
            files = [target_path]
        else:
            files = list(target_path.rglob("*.py"))
        summaries = []
        for file_path in files:
            try:
                summaries.append(self._summarize_file(file_path))
            except Exception as e:
                summaries.append(f"# Error analyzing {file_path.name}: {str(e)}")
        return "\n\n".join(summaries)


    def _summarize_file(self, file_path: Path) -> str:
        """Summarizes a single Python file into its API signatures."""
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            return f"# Syntax Error in {file_path.name}: {str(e)}"
        # Strip implementations
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                node.body = [ast.Pass()]
            elif isinstance(node, ast.ClassDef):
                # Keep class docstring if it exists, otherwise pass
                if (
                    node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)
                ):
                    node.body = [node.body[0], ast.Pass()]
                else:
                    node.body = [ast.Pass()]

        compact_code = ast.unparse(tree)
        # remove residual comments using regex if needed
        compact_code = re.sub(r'(?m)^\s*#.*$', '', compact_code)
        compact_code = re.sub(r'\n\s*\n', '\n', compact_code)
        rel_path = os.path.relpath(file_path, self.workspace_root)
        return f"### API Guide regarding {rel_path}\n```python\n{compact_code}\n```"


    def calculate_metrics_summary(self, source: str) -> dict:
        """Calculates basic metrics regarding the source code."""
        lines = source.splitlines()
        return {
            "total_lines": len(lines),
            "code_lines": len([line for line in lines if line.strip() and not line.strip().startswith("#")]),
            "comment_lines": len([line for line in lines if line.strip().startswith("#")]),
            "functions": len(re.findall(r"(?m)^\s*def\s+", source)),
            "classes": len(re.findall(r"(?m)^class\s+", source)),
        }
