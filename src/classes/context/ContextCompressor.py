#!/usr/bin/env python3

"""Engine for compressing large code files into summarized signatures."""

import re
import ast
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

class ContextCompressor:
    """Reduces the size of source files while preserving structural context.
    
    This is useful for fitting large codebases into constrained LLM context windows.
    """
    
    def __init__(self, workspace_root: Optional[str] = None) -> None:
        self.workspace_root = Path(workspace_root) if workspace_root else None

    def compress_python(self, content: str) -> str:
        """Removes function bodies and keeps only class/function signatures."""
        try:
            tree = ast.parse(content)
            compressed_lines = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    compressed_lines.append(f"class {node.name}:")
                    # Capture inheritance if any
                    if node.bases:
                        bases = ", ".join([ast.unparse(b) for b in node.bases])
                        compressed_lines[-1] = f"class {node.name}({bases}):"
                        
                elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                    # For functions inside classes, this walk might get messy, 
                    # but for a "summary" it's often okay to just list them.
                    args = ast.unparse(node.args)
                    indent = "    " if any(isinstance(p, ast.ClassDef) for p in ast.walk(node)) else ""
                    # Note: ast.walk doesn't preserve parent info easily without custom visitor
                    # Simple version:
                    compressed_lines.append(f"def {node.name}({args}): ...")
            
            # Extract docstrings if available (optional enhancement)
            return "\n".join(sorted(list(set(compressed_lines))))
        except Exception as e:
            logging.debug(f"AST compression failed, falling back to regex: {e}")
            # Fallback to simple regex if AST fails (e.g. invalid syntax)
            signatures = re.findall(r"^\s*(?:def|class)\s+[a-zA-Z_][a-zA-Z0-9_]*.*?:", content, re.MULTILINE)
            return "\n".join(signatures)

    def summarize_markdown(self, content: str) -> str:
        """Keeps only headers from markdown files."""
        headers = re.findall(r"^(#+ .*)$", content, re.MULTILINE)
        return "\n".join(headers)

    def compress_file(self, file_path: Path) -> str:
        """Determines compression strategy based on file extension."""
        if not file_path.exists():
            return f"Error: File {file_path} not found."
            
        content = file_path.read_text(encoding="utf-8")
        if file_path.suffix == ".py":
            return f"### {file_path.name} (Compressed)\n" + self.compress_python(content)
        elif file_path.suffix == ".md":
            return f"### {file_path.name} (Summary)\n" + self.summarize_markdown(content)
        else:
            # For other files, just return the first 20 lines
            lines = content.splitlines()[:20]
            return f"### {file_path.name} (Head)\n" + "\n".join(lines)

if __name__ == "__main__":
    # Test
    compressor = ContextCompressor()
    test_code = """
class MyClass:
    def __init__(self, x: int) -> None:
        self.x = x
    
    def method_a(self, y):
        return y * 2
"""
    print(compressor.compress_python(test_code))
