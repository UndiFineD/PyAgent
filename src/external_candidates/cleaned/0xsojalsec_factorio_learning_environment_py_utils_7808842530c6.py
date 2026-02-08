# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\data.py\vqa.py\utils_7808842530c6.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\data\vqa\utils.py

from pathlib import Path


def find_blueprints_dir() -> Path:
    """Walk up the directory tree until we find .fle directory."""

    current = Path.cwd()

    while current != current.parent:
        fle_dir = current / ".fle"

        if fle_dir.exists() and fle_dir.is_dir():
            return fle_dir / "blueprints"

        current = current.parent

    # Fallback - return the path even if it doesn't exist

    return Path.cwd() / ".fle" / "blueprints"
