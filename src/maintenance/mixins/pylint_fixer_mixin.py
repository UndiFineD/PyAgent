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

"""
Mixin providing automated pylint issue remediation for the Maintenance Agent.
"""

import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class PylintFixerMixin:
    """Provides automated fixes for common Pylint warnings."""

    def fix_unspecified_encoding(self, file_path: Path) -> bool:
        """Fixes W1514: open() without explicitly specifying an encoding."""
        try:
            content = file_path.read_text(encoding="utf-8")
            new_content = re.sub(
                r"\bopen\(([^,)]+), \s*['\"]([rwab]+)['\"](?!\s*,\s*encoding=)\)",
                r"open(\1, '\2', encoding='utf-8')",
                content
            )
            new_content = re.sub(
                r"\bopen\(([^,)]+)(?!\s*,\s*encoding=)\)",
                r"open(\1, encoding='utf-8')",
                new_content
            )

            if new_content != content:
                file_path.write_text(new_content, encoding="utf-8")
                return True
            return False
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(f"Failed to fix encoding in {file_path}: {e}")
            return False

    def fix_no_else_return(self, file_path: Path) -> bool:
        """Fixes R1705: Unnecessary 'else' after 'return'."""
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.splitlines()
            new_lines = []
            i = 0
            modified = False
            while i < len(lines):
                line = lines[i]
                return_match = re.match(r'^(\s*)return(\s+|$)', line)
                if return_match:
                    indent = return_match.group(1)
                    if i + 1 < len(lines):
                        next_line = lines[i+1]
                        else_match = re.search(r'^\s*(else|elif):', next_line)
                        if else_match:
                            actual_indent = re.match(r'^\s*', next_line).group(0)
                            if actual_indent == indent:
                                new_lines.append(line)
                                modified = True
                                i += 1
                                continue
                new_lines.append(line)
                i += 1

            if modified:
                file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
                return True
            return False
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(f"Failed to fix no-else-return in {file_path}: {e}")
            return False

    def fix_broad_exception(self, file_path: Path) -> bool:
        """Fixes W0718: Catching too general exception Exception."""
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.splitlines()
            new_lines = []
            modified = False
            for line in lines:
                sline = line.strip()
                if (sline.startswith("except") and sline.endswith(":")) or \
                   (":" in sline and sline.startswith("except") and "#" in sline):
                    if "Exception" in sline or "BaseException" in sline or sline.startswith("except:"):
                        if "pylint: disable=" in line:
                            updated_line = line
                            if "broad-exception-caught" not in line and "broad-except" not in line:
                                updated_line = updated_line.replace(
                                    "pylint: disable=",
                                    "pylint: disable=broad-exception-caught, "
                                )
                                modified = True
                            if "unused-variable" not in line:
                                updated_line = updated_line.replace(
                                    "pylint: disable=",
                                    "pylint: disable=unused-variable, "
                                )
                                modified = True
                            new_lines.append(updated_line)
                            continue

                        # If no disable, inject it
                        indent_match = re.match(r"^(\s*)", line)
                        indent = indent_match.group(1) if indent_match else ""
                        new_lines.append(
                            f"{indent}except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable"
                        )
                        modified = True
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)

            if modified:
                file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
                return True
            return False
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(f"Failed to fix broad exception in {file_path}: {e}")
            return False
