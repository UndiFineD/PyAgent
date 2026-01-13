# Copyright 2026 PyAgent Authors
# Apache 2.0 License

from __future__ import annotations
import os
import re
import asyncio
from typing import List, Dict, Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

class PrivacyGuardAgent(BaseAgent):
    """
    Phase 286: Privacy Guard Agent.
    Scans for AWS keys, private tokens, and other secrets.
    """

    def __init__(self, file_path: str = "security_scan.audit") -> None:
        super().__init__(file_path)
        self.secret_patterns = {
            "AWS_KEY": re.compile(r"(?i)AKIA[0-9A-Z]{16}"),
            "AWS_SECRET": re.compile(r"(?i)SECRET.*['\"]?[a-zA-Z0-9/+=]{40}['\"]?"),
            "GENERIC_TOKEN": re.compile(r"(?i)(token|auth|key|secret)[ \t]*[:=][ \t]*['\"]?[a-zA-Z0-9_\-\.]{16,}['\"]?"),
            "GITHUB_TOKEN": re.compile(r"ghp_[a-zA-Z0-9]{36}")
        }

    @as_tool
    async def scan_secrets(self, target_dir: str) -> list[dict[str, Any]]:
        """Scans directory for potential secrets."""
        def run_scan() -> list[dict[str, Any]]:
            leaks = []
            for root, _, files in os.walk(target_dir):
                if ".git" in root or "__pycache__" in root:
                    continue
                for file in files:
                    path = os.path.join(root, file)
                    try:
                        with open(path, encoding="utf-8") as f:
                            lines = f.readlines()
                        
                        for i, line in enumerate(lines):
                            for name, pattern in self.secret_patterns.items():
                                if pattern.search(line):
                                    leaks.append({
                                        "file": path,
                                        "line": i + 1,
                                        "type": name,
                                        "snippet": line.strip()[:50] + "..."
                                    })
                    except Exception:
                        continue
            return leaks
            
        return await asyncio.to_thread(run_scan)

    async def get_improvement_items(self, context: dict[str, Any]) -> list[dict[str, Any]]:
        target = context.get("target_dir", ".")
        leaks = await self.scan_secrets(target)
        
        improvements = []
        for leak in leaks:
            improvements.append({
                "path": leak["file"],
                "improvement": f"REMOVE EXPOSED SECRET ({leak['type']}) at line {leak['line']}",
                "priority": 1.0 # Highest priority
            })
        return improvements
