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


# "Shell for ContextCompressorCore, handling File I/O and orchestration.
"""
# from __future__ import annotations
import logging
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.logic.agents.cognitive.context.engines.context_compressor_core import (
    ContextCompressorCore,
)

__version__ = VERSION


class ContextCompressor:
    "Reduces the size of source files while preserving structural context.

    Acts as the I/O Shell for ContextCompressorCore.
"""

    def __init__(self, workspace_root: str | None = None) -> None:
        self.workspace_root: Path | None = (
            Path(workspace_root) if workspace_root else None
        )
        self.core = ContextCompressorCore()

    def compress_file(self, file_path_raw: Any) -> str:
""""Determines compression strategy based on file extension and handles I/O."""
        file_path = Path(file_path_raw)

        if not file_path.exists():
#             return fError: File {file_path} not found.

        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")

            mode = self.core.decide_compression_mode(file_path.name)
            header = self.core.get_summary_header(file_path.name, mode.capitalize())

            if mode == "python":
                return header + self.core.compress_python(content)

            if mode == "markdown":
                return header + self.core.summarize_markdown(content)

            # For other files, just return the first 20 lines
            lines = content.splitlines()[:20]

            return header + "\n".join(lines)
        except (IOError, OSError) as e:
            logging.error(fFailed to compress {file_path}: {e}")
#             return fError compressing {file_path.name}: {str(e)}


if __name__ == "__main__":
    # Test
    compressor = ContextCompressor()
    # Simple self-test
    print(compressor.compress_file(__file__))
