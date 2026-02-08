# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_web_navigator.py\src.py\vectorstore.py\views_7634ea8a509c.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Web-Navigator\src\vectorstore\views.py

from dataclasses import dataclass, field

from uuid import uuid4


@dataclass
class Document:
    id: str = field(default_factory=lambda: str(uuid4()))

    content: str = field(default_factory=str)

    metadata: dict = field(default_factory=dict)
