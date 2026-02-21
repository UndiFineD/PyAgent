"""Minimal notification manager used by tests and lightweight codepaths."""

from __future__ import annotations
from typing import Callable, Dict, List


class NotificationManager:
    """Tiny manager to register and notify subscribers."""

    def __init__(self) -> None:
        self._subs: Dict[str, List[Callable[..., None]]] = {}

    def subscribe(self, topic: str, fn: Callable[..., None]) -> None:
        self._subs.setdefault(topic, []).append(fn)

    def notify(self, topic: str, *args, **kwargs) -> None:
        for fn in list(self._subs.get(topic, [])):
            try:
                fn(*args, **kwargs)
            except Exception:
                # swallow errors in minimal test shim
                pass


__all__ = ["NotificationManager"]
