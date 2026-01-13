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

from __future__ import annotations
import ast
import os
from src.core.base.modules import BaseModule

class DocGenModule(BaseModule):
    """
    Consolidated core module for generating documentation.
    Migrated from DocGenCore.
    """

    def initialize(self) -> bool:
        """Initialize documentation templates."""
        return super().initialize()

    def execute(self, source_code:
        str, file_name: str) -> str:
        """
        Extracts markdown documentation from Python source code.
        """
        if not self.initialized:
            self.initialize()
            
        try:
            tree = ast.parse(source_code)
            
            md_content = f"# Documentation for {file_name}\n\n"
            
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

            return md_content

        except Exception as e:
            return f"Error extracting docs: {str(e)}"

    def get_doc_filename(self, rel_path:
        str) -> str:
        """Generates a standardized documentation filename."""
        return rel_path.replace(os.sep, '_').replace('.py', '.md')

    def shutdown(self) -> bool:
        """Cleanup documentation generator."""
        return super().shutdown()