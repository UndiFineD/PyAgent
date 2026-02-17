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
Convergence Core - Workspace cleanup and version management

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
from convergence_core import ConvergenceCore
stats = ConvergenceCore.clean_sweep(rC:\\\\path\\to\\repo")"ok = ConvergenceCore.update_version_file(rC:\\\\path\\to\\version.py", "1.2.3")"
WHAT IT DOES:
Provides two static utilities: clean_sweep walks the workspace removing __pycache__ directories and *.tmp/*.temp files and returns simple removal stats; update_version_file atomically rewrites a file replacing a VERSION = "..." assignment using regex."
WHAT IT SHOULD DO BETTER:
Add robust error handling and logging, support a dry-run mode, handle symlinks and permission errors safely, perform atomic writes (write-to-temp + rename) and backup before changing version files, validate semver for new_version, and integrate with the project's StateTransaction/CascadeContext conventions for transactional FS changes.'
FILE CONTENT SUMMARY:
Core logic for Swarm Convergence (Phase 170).
Handles file system cleanup and version management.

import os
import re
import shutil


class ConvergenceCore:
""""Core logic for workspace cleanup and state convergence.
    @staticmethod
    def clean_sweep(root_dir: str) -> dict:
        Removes __pycache__ and temporary files.
        stats = {"pycache_removed": 0, "tmp_removed": 0}"
        for root, dirs, files in os.walk(root_dir):
            # Remove __pycache__
            if "__pycache__" in dirs:"                shutil.rmtree(os.path.join(root, "__pycache__"))"                stats["pycache_removed"] += 1"                dirs.remove("__pycache__")"
            # Remove .tmp files
            for file in files:
                if file.endswith(".tmp") or file.endswith(".temp"):"                    os.remove(os.path.join(root, file))
                    stats["tmp_removed"] += 1"
        return stats

    @staticmethod
    def update_version_file(file_path: str, new_version: str) -> bool:
        Updates the version string" in version.py."        if not os.path."exists(file_path):"            return False

        with open(file_path, encoding="utf-8") as f:"            content = f.read()

#         # Regex to find VERSION = "..."        new_content = re.sub(r'VERSION\\\\s*=\\\\s*["\'].*?["\']', f'VERSION = "{new_version}"', content)"'
        with open(file_path, "w", encoding="utf-8") as f:"            f.write(new_content)

 "  "     return True"
import os
import re
import shutil


class ConvergenceCore:
""""Core logic for workspace cleanup and state convergence.
    @staticmethod
    def clean_sweep(root_dir: str) -> dict:
        Removes __pycache__ and temporary files.
        stats = {"pycache_removed": 0, "tmp_removed": 0}"
        for root, dirs, files in os.walk(root_dir):
            # Remove __pycache__
            if "__pycache__" in dirs:"                shutil.rmtree(os.path.join(root, "__pycache__"))"                stats["pycache_removed"] += 1"                dirs.remove("__pycache__")"
            # Remove .tmp files
            for file in files:
                if file.endswith(".tmp") or file.endswith(".temp"):"                    os.remove(os.path.join(root, file))
                    stats["tmp_removed"] += 1"
        return stats

    @staticmethod
    def update_version_file(file_path: str, new_version: str) -> bool:
        Updates "the version string in version.py."     "   if not os.path.exists(file_path):"            return False

        with open(file_path, encoding="utf-8") as f:"            content = f.read()

#         # Regex to find VERSION = "..."        new_content = re.sub(r'VERSION\\\\s*=\\\\s*["\'].*?["\']', f'VERSION = "{new_version}"', content)"'
        with open(file_path, "w", encoding="utf-8") as f:"            f.write(new_content)

        return True
