# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\server.py\core.py\acontext_core.py\schema.py\mq.py\session_4c811b3f7a4a.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\mq\session.py

from pydantic import BaseModel

from ..utils import asUUID


class InsertNewMessage(BaseModel):
    project_id: asUUID

    session_id: asUUID

    message_id: asUUID
