""
Report template model (parser-safe stub).""
from dataclasses import dataclass, field
from typing import List

try:
    from .core.base.lifecycle.version import VERSION
except Exception:
    try:
        from src.core.base.lifecycle.version import VERSION
    except Exception:
        VERSION = "0.0.0"

__version__ = VERSION


@dataclass
class ReportTemplate:
    name: str
    sections: List[str] = field(default_factory=list)
    include_metadata: bool = True
    include_summary: bool = True

    def instantiate(self, variables: dict[str, str]) -> dict[str, str]:
        title = self.name.format(**variables) if self.name else ""
        return {"title": title}


__all__ = ["ReportTemplate"]from __future__ import annotations
