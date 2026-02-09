# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\mq\sop.py
from pydantic import BaseModel

from ..block.sop_block import SOPData
from ..utils import asUUID


class SOPComplete(BaseModel):
    project_id: asUUID
    space_id: asUUID
    task_id: asUUID
    sop_data: SOPData
