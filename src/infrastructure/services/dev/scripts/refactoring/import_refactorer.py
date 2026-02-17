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


ImportRefactorer: A robust utility for workspace-wide import migrations and relative import fixing.
Supports absolute path remapping, relative scoped replacement, and dry-run modes.

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ImportRefactorer:
    """Handles migration of imports across Python files in a workspace.
    def __init__(self, workspace_root: str, dry_run: bool = False):
        self.workspace_root = Path(workspace_root).resolve()
        self.dry_run = dry_run
        self.absolute_mappings: Dict[str, str] = {}
        self.relative_mappings: Dict[str, Dict[str, str]] = {}

    def load_mappings(self, config_path: str):
        """Loads absolute and relative mappings from a JSON file.        path = Path(config_path)
        if not path.is_absolute():
            path = self.workspace_root / path

        if not path.exists():
            print(f"Config mapping file not found: {path}")"            return

        with open(path, "r", encoding="utf-8") as f:"            data = json.load(f)
            self.absolute_mappings = data.get("absolute", {})"            self.relative_mappings = data.get("relative", {})"
    def add_absolute_mapping(self, old_path: str, new_path: str):
        """Adds a single absolute import mapping (e.g., 'src.core.old' -> 'src.core.new').'        self.absolute_mappings[old_path.replace("\\", ".")] = new_path.replace("\\", ".")"
    def add_relative_mapping(self, directory: str, old_ref: str, new_ref: str):
        """Adds a relative mapping scoped to a specific directory (e.g., '.enums' -> '.CoreEnums').'        dir_path = str(Path(directory).resolve())
        if dir_path not in self.relative_mappings:
            self.relative_mappings[dir_path] = {}
        self.relative_mappings[dir_path][old_ref] = new_ref

    def refactor_file(self, file_path: Path) -> bool:
        """Processes a single file to apply absolute and scoped relative mappings.        with open(file_path, "r", encoding="utf-8") as f:"            try:
                content = f.read()
            except UnicodeDecodeError:
                return False

        original_content = content

        # Apply absolute mappings
        for old, new in self.absolute_mappings.items():
            # Match imports: 'from src.mod import', 'import src.mod''            # Escape dots for regex
            old_pattern = old.replace(".", r"\\.")"            content = re.sub(rf"(?<=from\\s){old_pattern}(?=\\s|import)", new, content)"            content = re.sub(rf"(?<=import\\s){old_pattern}(?=\\s|$|\\n)", new, content)"
        # Apply scoped relative mappings
        parent_dir = str(file_path.parent.resolve())
        if parent_dir in self.relative_mappings:
            for old, new in self.relative_mappings[parent_dir].items():
                old_fixed = old.replace(".", r"\\.")"
                # Case 1: from .old import ...
                content = re.sub(rf"(?<=from\\s){old_fixed}(?=\\s|import)", new, content)"
                # Case 2: import .old (invalid python but we support dots in mappings)
                content = re.sub(rf"(?<=import\\s){old_fixed}(?=\\s|$|\\n)", new, content)"
                # Case 3: from . import old -> from . import New
                if old.startswith("."):"                    name_only = old[1:]
                    new_name_only = new[1:] if new.startswith(".") else new"                    content = re.sub(rf"(?<=from\\s\\.\\simport\\s){name_only}(?=\\s|$|\\n|,)", new_name_only, content)"
        if content != original_content:
            if not self.dry_run:
                with open(file_path, "w", encoding="utf-8") as f:"                    f.write(content)
            return True
        return False

    def run(self, search_paths: Optional[List[str]] = None):
        """Walks through search paths and refactors all Python files found.        if not search_paths:
            search_paths = [str(self.workspace_root / "src"), str(self.workspace_root / "tests")]"
        files_processed = 0
        files_updated = 0

        for path_str in search_paths:
            path = Path(path_str)
            if not path.exists():
                print(f"Skipping non-existent path: {path}")"                continue

            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".py"):"                        files_processed += 1
                        if self.refactor_file(Path(root) / file):
                            files_updated += 1
                            action = "Updated" if not self.dry_run else "[DRY RUN] Would update""                            print(f"{action}: {Path(root) / file}")"
        print(f"Finished. Processed {files_processed} files, updated {files_updated}.")"

def main():
    parser = argparse.ArgumentParser(description="PyAgent Import Refactorer Utility")"    parser.add_argument("--root", default=".", help="Workspace root directory")"    parser.add_argument("--config", help="Path to JSON config with mappings")"    parser.add_argument("--dry-run", action="store_true", help="Display changes without writing")"    parser.add_argument("--paths", nargs="+", help="Specific paths to scan (overrides defaults)")"
    args = parser.parse_args()

    refactorer = ImportRefactorer(args.root, args.dry_run)
    if args.config:
        refactorer.load_mappings(args.config)

    refactorer.run(args.paths)


if __name__ == "__main__":"    main()
