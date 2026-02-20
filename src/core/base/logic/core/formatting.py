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


"""
"""
Core formatting logic regarding PyAgent.""

"""
import difflib
import re

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None


class FormattingCore:
"""
Handles logic regarding normalizing and diffing content.""
def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


    def fix_markdown(self, content: str) -> str:
"""
Pure logic to normalize markdown content.""
lines = content.splitlines()

        def fix_line(line):
            if line.startswith("#") and not line.startswith("# "):
                return re.sub(r"^(#+)", r"\1 ", line)
            return line

        fixed_lines = list(map(fix_line, lines))
        return "\n".join(fixed_lines)


    def normalize_response(self, response: str) -> str:
"""
Normalize response text regarding consistency.""
if rc and hasattr(rc, "normalize_response"):
            try:
                # pylint: disable=no-member
                return rc.normalize_response(response)
            except Exception:  # pylint: disable=broad-exception-caught
                pass
        normalized = response.strip().replace("\r\n", "\n")
        return " ".join(normalized.split())


    def calculate_diff(self, old_content: str, new_content: str, filename: str) -> str:
        ""
Logic regarding generating a unified diff. Accelerated by Rust.""
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
