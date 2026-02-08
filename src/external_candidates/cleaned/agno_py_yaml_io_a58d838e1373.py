# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\agno.py\utils.py\yaml_io_a58d838e1373.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\utils\yaml_io.py

from pathlib import Path

from typing import Any, Dict, Optional

from agno.utils.log import log_debug, logger


def read_yaml_file(file_path: Optional[Path]) -> Optional[Dict[str, Any]]:
    if file_path is not None and file_path.exists() and file_path.is_file():
        import yaml

        log_debug(f"Reading {file_path}")

        data_from_file = yaml.safe_load(file_path.read_text())

        if data_from_file is not None and isinstance(data_from_file, dict):
            return data_from_file

        else:
            logger.error(f"Invalid file: {file_path}")

    return None


def write_yaml_file(file_path: Optional[Path], data: Optional[Dict[str, Any]], **kwargs) -> None:
    if file_path is not None and data is not None:
        import yaml

        log_debug(f"Writing {file_path}")

        file_path.write_text(yaml.safe_dump(data, **kwargs))
