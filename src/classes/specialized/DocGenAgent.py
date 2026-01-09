import os
import ast
from typing import Dict, List, Any
from src.classes.base_agent import BaseAgent

class DocGenAgent(BaseAgent):
    """
    Autonomous Documentation Generator: Extracts docstrings from Python modules 
    and generates Markdown files compatible with Sphinx/Jekyll.
    """
    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.doc_registry = {} # module_path -> extracted_docs

    def extract_docs(self, file_path: str) -> str:
        """Extracts docstrings from a Python file and returns Markdown content."""
        if not file_path.endswith('.py'):
            return ""

        try:
            with open(file_path, "r", encoding="utf-8") as f:
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
            doc_filename = rel_path.replace(os.sep, '_').replace('.py', '.md')
            with open(os.path.join(output_dir, doc_filename), "w", encoding="utf-8") as f:
                f.write(content)
        
        return len(self.doc_registry)
