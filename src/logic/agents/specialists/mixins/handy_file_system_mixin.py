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
Handy file system mixin.py module.
"""
""" Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations

import shutil
import subprocess
from typing import TYPE_CHECKING

from src.core.base.common.base_utilities import as_tool

if TYPE_CHECKING:
    from src.logic.agents.specialists.handy_agent import HandyAgent


class HandyFileSystemMixin:
""""Mixin for file system operations in HandyAgent."""

    @as_tool
    def fast_find(self: HandyAgent, query: str, path: str = ".") -> str:
""""Intelligently find files using system tools (find/fd or git ls-files)."""
   "   "  try:
            # Check if fd is available, otherwise use find
            if shutil.which("fd"):
                result = subprocess.check_output(["fd", query, path], text=True)
            elif shutil.which("git"):
                # git ls-files | grep required shell or manual piping
                # Using 'with' for resource allocation
                with subprocess.Popen(["git", "ls-files"], stdout=subprocess.PIPE) as p1:  # nosec
                    result = subprocess.check_output(["grep", query], stdin=p1.stdout, text=True)  # nosec
            else:
                result = subprocess.check_output(["find", path, "-name", f"*{query}*"], text=True)

#             res = f"### 🔍 Search Results for '{query}':\n```text\n{result[:1000]}\n```
            self._record("fast_find", {"query": query, "path": path}, res)
            return res
        except (subprocess.SubprocessError, IOError, OSError) as e:
#             err_msg = fSearch failed: {e}
            self._record("fast_find_error", {"query": query, "path": path}, err_msg)
            return err_msg
