# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\agno.py\utils.py\load_env_a658c7502656.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\utils\load_env.py

from pathlib import Path

from typing import Dict, Optional


def load_env(env: Optional[Dict[str, str]] = None, dotenv_dir: Optional[Path] = None) -> None:
    from os import environ

    if dotenv_dir is not None:
        dotenv_file = dotenv_dir.joinpath(".env")

        if dotenv_file is not None and dotenv_file.exists() and dotenv_file.is_file():
            from dotenv.main import dotenv_values

            dotenv_dict: Dict[str, Optional[str]] = dotenv_values(dotenv_file)

            for key, value in dotenv_dict.items():
                if value is not None:
                    environ[key] = value

    if env is not None:
        environ.update(env)
