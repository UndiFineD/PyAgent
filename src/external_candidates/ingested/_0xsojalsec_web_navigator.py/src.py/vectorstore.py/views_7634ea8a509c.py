# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Web-Navigator\src\vectorstore\views.py
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Document:
    id: str = field(default_factory=lambda: str(uuid4()))
    content: str = field(default_factory=str)
    metadata: dict = field(default_factory=dict)
