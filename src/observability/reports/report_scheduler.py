""
Report scheduler helpers (parser-safe stub).""
try:
    from .core.base.lifecycle.version import VERSION
except Exception:
    try:
        from src.core.base.lifecycle.version import VERSION
    except Exception:
        VERSION = "0.0.0"

__version__ = VERSION


class ReportScheduler:
    def __init__(self) -> None:
        self.schedules: dict[str, dict] = {}

    def schedule(self, name: str, spec: dict) -> None:
        self.schedules[name] = spec


__all__ = ["ReportScheduler"]from __future__ import annotations
