from pathlib import Path


def download_repo(repo: str, dest: Path) -> None:
    """Create a placeholder directory for the given repo."""
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "README.md").write_text("")
