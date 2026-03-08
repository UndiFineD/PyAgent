"""
LLM_CONTEXT_START

## Source: src-old/classes/specialized/DocGenAgent.description.md

# DocGenAgent

**File**: `src\classes\specialized\DocGenAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 86  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for DocGenAgent.

## Classes (1)

### `DocGenAgent`

**Inherits from**: BaseAgent

Autonomous Documentation Generator: Extracts docstrings from Python modules 
and generates Markdown files compatible with Sphinx/Jekyll.

**Methods** (3):
- `__init__(self, workspace_path)`
- `extract_docs(self, file_path)`
- `generate_documentation_site(self, output_dir)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `ast`
- `os`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.VERSION`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/DocGenAgent.improvements.md

# Improvements for DocGenAgent

**File**: `src\classes\specialized\DocGenAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 86 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `DocGenAgent_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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


from src.core.base.version import VERSION
import os
import ast
from src.core.base.BaseAgent import BaseAgent

__version__ = VERSION


class DocGenAgent(BaseAgent):
    """
    Autonomous Documentation Generator: Extracts docstrings from Python modules
    and generates Markdown files compatible with Sphinx/Jekyll.
    """

    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.doc_registry = {}  # module_path -> extracted_docs

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
                    md_content += f"## Class: `{node.name}`\n"
                    class_doc = ast.get_docstring(node)
                    if class_doc:
                        md_content += f"{class_doc}\n\n"

                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            md_content += f"### Method: `{item.name}`\n"
                            func_doc = ast.get_docstring(item)
                            if func_doc:
                                md_content += f"{func_doc}\n\n"

                elif isinstance(node, ast.FunctionDef):
                    md_content += f"## Function: `{node.name}`\n"
                    func_doc = ast.get_docstring(node)
                    if func_doc:
                        md_content += f"{func_doc}\n\n"

            self.doc_registry[file_path] = md_content
            return md_content

        except Exception as e:
            return f"Error extracting docs: {str(e)}"

    def generate_documentation_site(self, output_dir: str) -> int:
        """Generates documentation files for all modules in the registry."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for file_path, content in self.doc_registry.items():
            rel_path = os.path.relpath(file_path, self.workspace_path)
            doc_filename = rel_path.replace(os.sep, "_").replace(".py", ".md")
            with open(
                os.path.join(output_dir, doc_filename), "w", encoding="utf-8"
            ) as f:
                f.write(content)

        return len(self.doc_registry)
