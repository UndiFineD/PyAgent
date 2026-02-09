# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\mq\space.py
from pydantic import BaseModel

from ..utils import asUUID


class NewTaskComplete(BaseModel):
    project_id: asUUID
    session_id: asUUID
    task_id: asUUID
