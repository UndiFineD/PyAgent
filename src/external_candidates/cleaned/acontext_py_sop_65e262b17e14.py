# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\server.py\core.py\acontext_core.py\schema.py\mq.py\sop_65e262b17e14.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\mq\sop.py

from pydantic import BaseModel

from ..block.sop_block import SOPData

from ..utils import asUUID


class SOPComplete(BaseModel):
    project_id: asUUID

    space_id: asUUID

    task_id: asUUID

    sop_data: SOPData
