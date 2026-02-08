# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\agno.py\utils.py\pyproject_4a0433e1fda4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\utils\pyproject.py

from pathlib import Path

from typing import Dict, Optional

from agno.utils.log import log_debug, logger


def read_pyproject_agno(pyproject_file: Path) -> Optional[Dict]:
    log_debug(f"Reading {pyproject_file}")

    try:
        import tomli

        pyproject_dict = tomli.loads(pyproject_file.read_text())

        agno_conf = pyproject_dict.get("tool", {}).get("agno", None)

        if agno_conf is not None and isinstance(agno_conf, dict):
            return agno_conf

    except Exception as e:
        logger.error(f"Could not read {pyproject_file}: {e}")

    return None
