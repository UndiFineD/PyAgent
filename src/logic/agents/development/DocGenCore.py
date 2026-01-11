from __future__ import annotations

import ast
import os
from typing import Dict, Optional

class DocGenCore:
    """
    Pure logic for extracting documentation from Python source code.
    No file I/O or side effects. 100% Type-safe and ready for Rust conversion.
    """

    @staticmethod
    def extract_markdown_from_source(source_code: str, file_name: str) -> str:
        """
        Parses source code using AST and generates Markdown documentation.
        
        Args:
            source_code: The raw Python source code as a string.
            file_name: The name of the file for labeling in the Markdown.
            
        Returns:
            A string containing the formatted Markdown documentation.
        """
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

    @staticmethod
    def get_doc_filename(rel_path: str) -> str:
        """
        Generates a standardized documentation filename from a relative path.
        Example: src/utils/helper.py -> src_utils_helper.md
        """
        return rel_path.replace(os.sep, '_').replace('.py', '.md')
