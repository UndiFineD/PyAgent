# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\server.py\core.py\acontext_core.py\schema.py\mq.py\space_cd35ee07d72b.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\mq\space.py

from pydantic import BaseModel

from ..utils import asUUID


class NewTaskComplete(BaseModel):
    project_id: asUUID

    session_id: asUUID

    task_id: asUUID
