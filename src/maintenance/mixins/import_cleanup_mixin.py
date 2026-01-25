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

<<<<<<< HEAD
<<<<<<< HEAD
=======
import os
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor)
=======
import os
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)
import re
import logging
from pathlib import Path
from typing import Dict, List, Tuple

<<<<<<< HEAD
<<<<<<< HEAD
logger: logging.Logger = logging.getLogger(__name__)
=======
logger = logging.getLogger(__name__)
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor)
=======
logger = logging.getLogger(__name__)
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)

class ImportCleanupMixin:
    """Provides utilities for resolving and fixing Python imports after refactors."""

    def build_module_map(self, root_dir: Path, dirs: List[str]) -> Dict[Tuple[str, str], str]:
        """
        Builds a map from (parent_path_lower, name_lower) to actual_case_name.
        Useful for fixing imports after snake_case renaming.
        """
        name_map = {}
        for d in dirs:
<<<<<<< HEAD
<<<<<<< HEAD
            dp: Path = root_dir / d
=======
            dp = root_dir / d
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor)
=======
            dp = root_dir / d
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)
            if not dp.exists():
                continue
            for p in dp.rglob("*"):
                if p.name == "__init__.py":
                    continue
<<<<<<< HEAD
<<<<<<< HEAD
                parent: str = str(p.parent.resolve()).lower()
                name: str = p.stem if not p.is_dir() else p.name
                # Remove underscores/dashes for fuzzy matching if needed
                low: str = name.replace("_", "").replace("-", "").lower()
=======
=======
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)
                parent = str(p.parent.resolve()).lower()
                name = p.stem if not p.is_dir() else p.name
                # Remove underscores/dashes for fuzzy matching if needed
                low = name.replace("_", "").replace("-", "").lower()
<<<<<<< HEAD
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor)
=======
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)
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
<<<<<<< HEAD
<<<<<<< HEAD
        parts: List[str] = mod_str.split(".")
        if mod_str.startswith("."):
            # Relative import
            m: re.Match[str] | None = re.match(r"^(\.+)", mod_str)
            dots: int = len(m.group(1))
            rel_parts: List[str] = parts[dots-1:]
=======
=======
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)
        parts = mod_str.split(".")
        if mod_str.startswith("."):
            # Relative import
            m = re.match(r"^(\.+)", mod_str)
            dots = len(m.group(1))
            rel_parts = parts[dots-1:]
<<<<<<< HEAD
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor)
=======
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)
            if rel_parts and rel_parts[0].startswith("."):
                rel_parts[0] = rel_parts[0].lstrip(".")
            if rel_parts and not rel_parts[0]:
                rel_parts.pop(0)

<<<<<<< HEAD
<<<<<<< HEAD
            curr: Path = current_file.parent.resolve()
=======
            curr = current_file.parent.resolve()
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor)
=======
            curr = current_file.parent.resolve()
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)
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
        else:
            # Absolute import
            curr_path = None
            res = []
            for i, p in enumerate(parts):
                if curr_path is None:
                    # Look for root/part
<<<<<<< HEAD
<<<<<<< HEAD
                    low: str = p.lower()
=======
                    low = p.lower()
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor)
=======
                    low = p.lower()
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)
                    for d in search_dirs:
                        if d.lower() == low:
                            curr_path = root_dir / d
                            res.append(d)
                            break
                    if curr_path:
                        continue
                    else:
                        return mod_str  # External module

<<<<<<< HEAD
<<<<<<< HEAD
                low: str = p.replace("_", "").replace("-", "").lower()
                key: Tuple[str] = (str(curr_path).lower(), low)
                if key in name_map:
                    real: str = name_map[key]
                    res.append(real)
                    curr_path: Path = curr_path / real
=======
=======
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)
                low = p.replace("_", "").replace("-", "").lower()
                key = (str(curr_path).lower(), low)
                if key in name_map:
                    real = name_map[key]
                    res.append(real)
                    curr_path = curr_path / real
<<<<<<< HEAD
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor)
=======
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)
                else:
                    res.extend(parts[i:])
                    break
            return ".".join(res)

<<<<<<< HEAD
<<<<<<< HEAD
    def fix_imports_in_file(self, file_path: Path, name_map: dict[tuple[str, str], str], root_dir: Path, search_dirs: list[str]) -> bool:
        """Updates imports in a file to match the actual filesystem casing/naming."""
        try:
            content: str = file_path.read_text(encoding="utf-8")

            def replacer(match) -> str:
                mod = match.group(2)
                resolved: str = self.resolve_module_path(mod, file_path, name_map, root_dir, search_dirs)
                return f"{match.group(1)}{resolved}"

            # Regex for 'import ...' and 'from ... import ...'
            new_content: str = re.sub(r"^(import\s+)([a-zA-Z0-9_\.]+)", replacer, content, flags=re.MULTILINE)
            new_content: str = re.sub(r"^(from\s+)([a-zA-Z0-9_\.]+)(?=\s+import)", replacer, new_content, flags=re.MULTILINE)
=======
=======
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)
    def fix_imports_in_file(self, file_path: Path, name_map: Dict, root_dir: Path, search_dirs: List[str]) -> bool:
        """Updates imports in a file to match the actual filesystem casing/naming."""
        try:
            content = file_path.read_text(encoding="utf-8")

            def replacer(match):
                mod = match.group(2)
                resolved = self.resolve_module_path(mod, file_path, name_map, root_dir, search_dirs)
                return f"{match.group(1)}{resolved}"

            # Regex for 'import ...' and 'from ... import ...'
            new_content = re.sub(r"^(import\s+)([a-zA-Z0-9_\.]+)", replacer, content, flags=re.MULTILINE)
            new_content = re.sub(r"^(from\s+)([a-zA-Z0-9_\.]+)(?=\s+import)", replacer, new_content, flags=re.MULTILINE)
<<<<<<< HEAD
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor)
=======
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)

            if new_content != content:
                file_path.write_text(new_content, encoding="utf-8")
                return True
            return False
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(f"Failed to fix imports in {file_path}: {e}")
            return False
