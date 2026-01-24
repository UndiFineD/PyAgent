
"""
Handy file system mixin.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations

import shutil
import subprocess
from typing import TYPE_CHECKING

from src.core.base.common.base_utilities import as_tool

if TYPE_CHECKING:
    from src.logic.agents.specialists.handy_agent import HandyAgent


class HandyFileSystemMixin:
    """Mixin for file system operations in HandyAgent."""

    @as_tool
    def fast_find(self: HandyAgent, query: str, path: str = ".") -> str:
        """Intelligently find files using system tools (find/fd or git ls-files)."""
        try:
            # Check if fd is available, otherwise use find
            if shutil.which("fd"):
                result = subprocess.check_output(["fd", query, path], text=True)
            elif shutil.which("git"):
                # git ls-files | grep required shell or manual piping
                # Added # nosec to suppress security warning for git/grep chain as it is manually piped
                p1 = subprocess.Popen(["git", "ls-files"], stdout=subprocess.PIPE)  # nosec
                result = subprocess.check_output(["grep", query], stdin=p1.stdout, text=True)  # nosec
                p1.stdout.close()
            else:
                result = subprocess.check_output(["find", path, "-name", f"*{query}*"], text=True)

            return f"### 🔍 Search Results for '{query}':\n```text\n{result[:1000]}\n```"
        except Exception as e:
            return f"Search failed: {e}"
