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
