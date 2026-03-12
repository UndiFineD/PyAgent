from pathlib import Path
from typing import Tuple


async def parse_manifest(path: Path) -> list[Tuple[str, str]]:
    """Read a github manifest file and return list of (user, repo) tuples."""
    repos: list[Tuple[str, str]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("/")
            if len(parts) == 2:
                repos.append((parts[0], parts[1]))
    return repos
