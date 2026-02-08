# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\server.py\core.py\acontext_core.py\schema.py\block.py\text_block_097327a6a03b.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\block\text_block.py

from typing import List, Optional

from pydantic import BaseModel

from ..utils import asUUID


class TextData(BaseModel):
    use_when: str

    notes: str


class TextBlock(TextData):
    id: asUUID

    space_id: asUUID
