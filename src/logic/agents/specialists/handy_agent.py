from __future__ import annotations
"""
Minimal parser-safe HandyAgent shim used during repository repair.

Offers a small set of filesystem/terminal helpers for imports/tests.
"""



from typing import Any, List
from pathlib import Path


class HandyAgent:
    def __init__(self, file_path: str | None = None) -> None:
        self._workspace = Path(file_path) if file_path else None

    def search_files(self, pattern: str) -> List[str]:
        # lightweight, non-recursive stub
        return []

    async def run_command(self, cmd: str) -> Dict[str, Any]:
        return {"cmd": cmd, "output": "", "returncode": 0}


__all__ = ["HandyAgent"]
