#!/usr/bin/env python3
try:
    from src.core.base.common.types.changelog_entry import (
        ChangelogEntry as _ChangelogEntry,
    )
except Exception:

    class _ChangelogEntry:  # fallback placeholder
        pass


ChangelogEntry = _ChangelogEntry

__all__ = ["ChangelogEntry"]
