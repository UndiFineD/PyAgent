# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\server.py\core.py\acontext_core.py\llm.py\tool.py\sop_lib.py\ctx_b1f9c69bd5c2.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\llm\tool\sop_lib\ctx.py

from dataclasses import dataclass

from ....schema.session.task import TaskSchema

from ....schema.utils import asUUID


@dataclass
class SOPCtx:
    project_id: asUUID

    space_id: asUUID

    task: TaskSchema
