#!/usr/bin/env python3
try:
    from src.logic.agents.cognitive.context.engines.mixins.context_data_mixin import (
        ContextDataMixin as _ContextDataMixin,
    )
except Exception:
    try:
        from src.logic.agents.cognitive.context.engines.mixins.ContextDataMixin import (
            ContextDataMixin as _ContextDataMixin,
        )
    except Exception:

        class _ContextDataMixin:
            pass


ContextDataMixin = _ContextDataMixin

__all__ = ["ContextDataMixin"]
