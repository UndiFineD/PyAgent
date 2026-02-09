# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\config\config.py
import os

import yaml


def _load_config(config_path="environment/config/config.yml"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


config = _load_config()
