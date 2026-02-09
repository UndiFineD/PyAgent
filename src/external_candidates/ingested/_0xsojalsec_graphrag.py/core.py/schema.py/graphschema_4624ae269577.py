# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GraphRAG\Core\Schema\GraphSchema.py
from typing import List

from Core.Schema.EntityRelation import Entity, Relationship


class ERGraphSchema:
    nodes: List[Entity]
    edges: List[Relationship]
