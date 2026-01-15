from dataclasses import dataclass
from typing import List




@dataclass
class ChangelogTemplate:
    name: str
    project_type: str
    sections: List[str]
    header_format: str = "## [{version}] - {date}"
    include_links: bool = True
    include_contributors: bool = False
