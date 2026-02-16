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
ImportCleanupMixin - Automated import resolution and normalization

[Brief Summary]
# DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
Used by maintenance/refactor agents to scan a project tree, build a filesystem
name map and update Python files' import statements to match actual module/file
names and casing, handling relative and absolute imports.

WHAT IT DOES:
Builds fuzzy name maps from filesystem layout, resolves relative and absolute
module strings to real names using that map, and rewrites import/from lines in
files to match the filesystem.

WHAT IT SHOULD DO BETTER:
Handle package __init__ exports, support aliased imports and multi-target
from-imports, preserve formatting and comments around complex import lines, and
add dry-run/backup and logging levels for safe mass edits.

FILE CONTENT SUMMARY:
Mixin providing automated import cleanup and optimization for the Maintenance
Agent.
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Tuple

logger: logging.Logger = logging.getLogger(__name__)


class ImportCleanupMixin:
    """Provides utilities for resolving and fixing Python imports after refactors."""

    def build_module_map(self, root_dir: Path, dirs: List[str]) -> Dict[Tuple[str, str], str]:
        """
        Builds a map from (parent_path_lower, name_lower) to actual_case_name.
        Useful for fixing imports after snake_case renaming.
        """
        name_map = {}
        for d in dirs:
            dp: Path = root_dir / d
            if not dp.exists():
                continue
            for p in dp.rglob("*"):
                if p.name == "__init__.py":
                    continue
                parent: str = str(p.parent.resolve()).lower()
                name: str = p.stem if not p.is_dir() else p.name
                # Remove underscores/dashes for fuzzy matching if needed
                low: str = name.replace("_", "").replace("-", "").lower()
                name_map[(parent, low)] = name
        return name_map

    def resolve_module_path(
        self,
        mod_str: str,
        current_file: Path,
        name_map: Dict[Tuple[str, str], str],
        root_dir: Path,
        search_dirs: List[str]
    ) -> str:
        """Resolves a module string to its correct casing and path."""
        parts: List[str] = mod_str.split(".")
        if mod_str.startswith("."):
            # Relative import
            m: re.Match[str] | None = re.match(r"^(\.+)", mod_str)
            if not m:
                return mod_str
            dots: int = len(m.group(1))
            rel_parts: List[str] = parts[dots-1:]
            if rel_parts and rel_parts[0].startswith("."):
                rel_parts[0] = rel_parts[0].lstrip(".")
            if rel_parts and not rel_parts[0]:
                rel_parts.pop(0)

            curr: Path = current_file.parent.resolve()
            for _ in range(dots - 1):
                curr = curr.parent

            res = []
            for p in rel_parts:
                key = (str(curr).lower(), p.replace("_", "").replace("-", "").lower())
                if key in name_map:
                    real = name_map[key]
                    res.append(real)
                    curr = curr / real
                else:
                    return mod_str  # Cannot resolve
            return "." * dots + ".".join(res)

        # Absolute import
        curr_path: Path | None = None
        res = []
        for i, p in enumerate(parts):
            if curr_path is None:
                # Look for root/part
                low: str = p.lower()
                for d in search_dirs:
                    if d.lower() == low:
                        curr_path = root_dir / d
                        res.append(d)
                        break
                if curr_path:
                    continue
                else:
                    return mod_str  # External module

            low: str = p.replace("_", "").replace("-", "").lower()
            key: Tuple[str, str] = (str(curr_path).lower(), low)
            if key in name_map:
                real: str = name_map[key]
                res.append(real)
                curr_path = curr_path / real
            else:
                res.extend(parts[i:])
                break
        return ".".join(res)

    def fix_imports_in_file(
        self,
        file_path: Path,
        name_map: Dict[Tuple[str, str], str],
        root_dir: Path,
        search_dirs: List[str]
    ) -> bool:
        """Updates imports in a file to match the actual filesystem casing/naming."""
        try:
            content: str = file_path.read_text(encoding="utf-8")

            def replacer(match) -> str:
                mod = match.group(2)
                resolved: str = self.resolve_module_path(mod, file_path, name_map, root_dir, search_dirs)
                return f"{match.group(1)}{resolved}"

            # Regex for 'import ...' and 'from ... import ...'
            new_content: str = re.sub(
                r"^((?:import|from)\s+)([a-zA-Z0-9_\.]+)",
                replacer,
                content,
                flags=re.MULTILINE
            )
            file_path.write_text(new_content, encoding="utf-8")
            return True
        except (OSError, UnicodeDecodeError, UnicodeEncodeError) as e:
            logger.error(f"Failed to fix imports in {file_path}: {e}")
            return False
