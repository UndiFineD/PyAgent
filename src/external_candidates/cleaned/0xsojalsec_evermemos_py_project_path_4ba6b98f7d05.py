# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\common_utils.py\project_path_4ba6b98f7d05.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\common_utils\project_path.py

from pathlib import Path

# Get the directory where load_env.py is located (utils directory)

# Do not import any other modules here, PROJECT_DIR is fundamental information

utils_dir = Path(__file__).parent

# src directory is the parent directory of utils

src_dir = utils_dir.parent

CURRENT_DIR = src_dir

PROJECT_DIR = src_dir.parent


def get_base_scan_path():
    """Get the base scan path"""

    return CURRENT_DIR
