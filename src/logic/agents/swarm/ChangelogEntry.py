from dataclasses import dataclass, field
from typing import List


@dataclass
class ChangelogEntry:
    category: str
    description: str
    version: str
    date: str
    priority: int
    severity: str
    tags: List[str] = field(default_factory=list)
    linked_issues: List[str] = field(default_factory=list)
