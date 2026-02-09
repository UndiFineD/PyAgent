# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\mq\session.py
from pydantic import BaseModel

from ..utils import asUUID


class InsertNewMessage(BaseModel):
    project_id: asUUID
    session_id: asUUID
    message_id: asUUID
