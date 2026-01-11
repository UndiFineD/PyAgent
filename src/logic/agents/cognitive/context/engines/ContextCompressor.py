#!/usr/bin/env python3

"""Shell for ContextCompressorCore, handling File I/O and orchestration."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

from src.logic.agents.cognitive.context.engines.ContextCompressorCore import ContextCompressorCore

class ContextCompressor:
    """Reduces the size of source files while preserving structural context.
    
    Acts as the I/O Shell for ContextCompressorCore.
    """
    
    def __init__(self, workspace_root: Optional[str] = None) -> None:
        self.workspace_root: Optional[Path] = Path(workspace_root) if workspace_root else None
        self.core = ContextCompressorCore()

    def compress_file(self, file_path_raw: Any) -> str:
        """Determines compression strategy based on file extension and handles I/O."""
        file_path = Path(file_path_raw)
        
        if not file_path.exists():
            return f"Error: File {file_path} not found."
            
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
            mode = self.core.decide_compression_mode(file_path.name)
            header = self.core.get_summary_header(file_path.name, mode.capitalize())
            
            if mode == "python":
                return header + self.core.compress_python(content)
            elif mode == "markdown":
                return header + self.core.summarize_markdown(content)
            else:
                # For other files, just return the first 20 lines
                lines = content.splitlines()[:20]
                return header + "\n".join(lines)
        except Exception as e:
            logging.error(f"Failed to compress {file_path}: {e}")
            return f"Error compressing {file_path.name}: {str(e)}"

if __name__ == "__main__":
    # Test
    compressor = ContextCompressor()
    # Simple self-test
    print(compressor.compress_file(__file__))
