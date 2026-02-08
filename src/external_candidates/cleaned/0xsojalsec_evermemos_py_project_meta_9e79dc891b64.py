# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\project_meta_9e79dc891b64.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\project_meta.py

import os

PROJECT_NAME = "EverMemOS"

PROJECT_VERSION = "1.0.0"


def get_env_project_name():
    """

    Get the project name from environment variables

    """

    project_name = os.getenv("project_name") or os.getenv("PROJECT_NAME")

    if project_name:
        return project_name

    else:
        return PROJECT_NAME
