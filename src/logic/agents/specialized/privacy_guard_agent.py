
"""
Privacy guard agent.py module.
"""
# Copyright 2026 PyAgent Authors
# Apache 2.0 License

from __future__ import annotations

import asyncio
import os
import re
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent


class PrivacyGuardAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """
    Phase 286: Privacy Guard Agent.
    Scans for AWS keys, private tokens, and other secrets.
    """

    def __init__(self, file_path: str = "security_scan.audit") -> None:
        super().__init__(file_path)
        self.secret_patterns = {
            "AWS_KEY": re.compile(r"(?i)AKIA[0-9A-Z]{16}"),
            "AWS_SECRET": re.compile(r"(?i)SECRET.*['\"]?[a-zA-Z0-9/+=]{40}['\"]?"),
            "GENERIC_TOKEN": re.compile(
                r"(?i)(token|auth|key|secret)[ \t]*[:=][ \t]*['\"]?[a-zA-Z0-9_\-\.]{16,}['\"]?"
            ),
            "GITHUB_TOKEN": re.compile(r"ghp_[a-zA-Z0-9]{36}"),
        }

    @as_tool
    async def scan_secrets(self, target_dir: str) -> list[dict[str, Any]]:
        """Scans directory for potential secrets."""

        def _check_line(line: str, path: str, line_idx: int) -> list[dict[str, Any]]:
            """Helper to check a single line for all patterns."""
            line_leaks = []
            for name, pattern in self.secret_patterns.items():
                if pattern.search(line):
                    line_leaks.append(
                        {
                            "file": path,
                            "line": line_idx + 1,
                            "type": name,
                            "snippet": line.strip()[:50] + "...",
                        }
                    )
            return line_leaks

        def run_scan() -> list[dict[str, Any]]:
            leaks = []
            for root, _, files in os.walk(target_dir):
                if any(p in root for p in [".git", "__pycache__"]):
                    continue
                for file in files:
                    path = os.path.join(root, file)
                    try:
                        with open(path, encoding="utf-8") as f:
                            for idx, line in enumerate(f):
                                leaks.extend(_check_line(line, path, idx))
                    except (OSError, UnicodeDecodeError):
                        continue
            return leaks

        return await asyncio.to_thread(run_scan)

    async def get_improvement_items(self, context: dict[str, Any]) -> list[dict[str, Any]]:
        """Identify improvement items relating to privacy leaks."""
        target = context.get("target_dir", ".")
        leaks = await self.scan_secrets(target)

        improvements = []
        for leak in leaks:
            improvements.append(
                {
                    "path": leak["file"],
                    "improvement": f"REMOVE EXPOSED SECRET ({leak['type']}) at line {leak['line']}",
                    "priority": 1.0,  # Highest priority
                }
            )
        return improvements

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Scan for secrets in the given prompt or file."""
        path = target_file if target_file else prompt
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                leaks = []
                for idx, line in enumerate(f):
                    for name, pattern in self.secret_patterns.items():
                        if pattern.search(line):
                            leaks.append(f"- Line {idx+1}: {name}")
                if not leaks:
                    return "✅ No secrets detected in the file."
                return f"🚨 Exposed Secrets in {path}:\n" + "\n".join(leaks)

        leaks = await self.scan_secrets(path)
        if not leaks:
            return "✅ No secrets detected in the directory."
        return f"🚨 Found {len(leaks)} potential secret leaks in {path}."
