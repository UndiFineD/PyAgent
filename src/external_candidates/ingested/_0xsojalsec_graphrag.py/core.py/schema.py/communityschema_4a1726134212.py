# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GraphRAG\Core\Schema\CommunitySchema.py
from dataclasses import asdict, dataclass, field
from typing import List, Set


class CommunityReportsResult:
    """Community reports result class definition."""

    report_string: str
    report_json: dict


@dataclass
class LeidenInfo:
    level: str = field(default="")
    title: str = field(default="")
    edges: Set[str] = field(default_factory=set)
    nodes: Set[str] = field(default_factory=set)
    chunk_ids: Set[str] = field(default_factory=set)
    occurrence: float = field(default=0.0)
    sub_communities: List[str] = field(default_factory=list)

    @property
    def as_dict(self):
        return asdict(self)
