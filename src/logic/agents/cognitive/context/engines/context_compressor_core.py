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




from __future__ import annotations
import re
import ast

from src.core.base.lifecycle.version import VERSION

try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

__version__ = VERSION


class ContextCompressorCore:
    """
    Pure logic core for code and document compression.
    """
    @staticmethod
    def compress_python(content: str) -> str:
        """
        Removes function bodies and keeps only class/function signatures using AST.
        """
        try:
            tree = ast.parse(content)
            compressed_lines: list[str] = []

            # Use a visitor pattern for cleaner separation if needed,
            # but for simple signature extraction, a walk is acceptable
            # as long as we maintain some structure.

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if node.bases:
                        try:
                            bases_str = f"({', '.join([ast.unparse(b) for b in node.bases])})"
                        except (AttributeError, ValueError, TypeError):
                            bases_str = "(...)"
                    else:
                        bases_str = ""
                    compressed_lines.append(f"class {node.name}{bases_str}:")
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    try:
                        args_str = ast.unparse(node.args)
                    except (AttributeError, ValueError, TypeError):
                        args_str = "..."
                    prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
                    # Note: Detecting indentation level in a walk is hard.
                    # We'll just list them as signatures for now.
                    compressed_lines.append(f"{prefix}def {node.name}({args_str}): ...")
            # Deduplicate and sort to provide a stable signature
            unique_signatures = sorted(list(set(compressed_lines)))
            return "\n".join(unique_signatures)
        except (SyntaxError, ValueError, AttributeError):
            # Fallback to simple regex if AST fails (e.g. invalid syntax)
            return ContextCompressorCore.regex_fallback_compress(content)
            compressed_lines: list[str] = []

            # Use a visitor pattern for cleaner separation if needed,
            # but for simple signature extraction, a walk is acceptable
            # as long as we maintain some structure.

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if node.bases:
                        try:
                            bases_str = f"({', '.join([ast.unparse(b) for b in node.bases])})"
                        except (AttributeError, ValueError, TypeError):
                            bases_str = "(...)"
                    else:
                        bases_str = ""
                    compressed_lines.append(f"class {node.name}{bases_str}:")
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    try:
                        args_str = ast.unparse(node.args)
                    except (AttributeError, ValueError, TypeError):
                        args_str = "..."
                    prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
                    # Note: Detecting indentation level in a walk is hard.
                    # We'll just list them as signatures for now.
                    compressed_lines.append(f"{prefix}def {node.name}({args_str}): ...")
            # Deduplicate and sort to provide a stable signature
            unique_signatures = sorted(list(set(compressed_lines)))
            return "\n".join(unique_signatures)
        except (SyntaxError, ValueError, AttributeError):
            # Fallback to simple regex if AST fails (e.g. invalid syntax)
            return ContextCompressorCore.regex_fallback_compress(content)

    @staticmethod
    def regex_fallback_compress(content: str) -> str:
        """
        Simple regex-based signature extraction for Python.
        """
        if HAS_RUST:
            try:
                return rust_core.regex_compress_python(content)  # type: ignore[attr-defined]
            except (RuntimeError, AttributeError):
                pass
        signatures = re.findall(
            r"^\s*(?:async\s+)?(?:def|class)\s+[a-zA-Z_][a-zA-Z0-9_]*.*?:",
            content,
            re.MULTILINE,
        )
        return "\n".join([s.strip() for s in signatures])
    @staticmethod
    def get_summary_header(filename: str, mode: str) -> str:
        """
        Logic for formatting summary headers.
        """
        return f"### {filename} ({mode})\n"

    @staticmethod
    def decide_compression_mode(filename: str) -> str:
        """
        Determines logic mode based on file extension.
        """
        if filename.endswith(".py"):
            return "python"
        if filename.endswith(".md"):
            return "markdown"
        return "head"