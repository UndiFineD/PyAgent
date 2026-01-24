"""Core formatting logic for PyAgent."""

# Copyright 2026 PyAgent Authors
import difflib
import re

try:
    import rust_core as rc
except ImportError:
    rc = None


class FormattingCore:
    """Handles logic for normalizing and diffing content."""

    def fix_markdown(self, content: str) -> str:
        """Pure logic to normalize markdown content."""
        lines = content.splitlines()
        fixed_lines = []
        for line in lines:
            if line.startswith("#") and not line.startswith("# "):
                line = re.sub(r"^(#+)", r"\1 ", line)
            fixed_lines.append(line)
        return "\n".join(fixed_lines)

    def normalize_response(self, response: str) -> str:
        """Normalize response text for consistency."""
        if rc and hasattr(rc, "normalize_response"):
            try:
                # pylint: disable=no-member
                return rc.normalize_response(response)
            except Exception:  # pylint: disable=broad-exception-caught
                pass
        normalized = response.strip().replace("\r\n", "\n")
        return " ".join(normalized.split())

    def calculate_diff(self, old_content: str, new_content: str, filename: str) -> str:
        """Logic for generating a unified diff. Accelerated by Rust."""
        if rc and hasattr(rc, "generate_unified_diff_rust"):
            try:
                # pylint: disable=no-member
                diff_text, _, _ = rc.generate_unified_diff_rust(old_content, new_content, filename, 3)
                return diff_text
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        diff_lines = list(difflib.unified_diff(old_lines, new_lines, fromfile=f"a/{filename}", tofile=f"b/{filename}"))
        return "".join(diff_lines)
