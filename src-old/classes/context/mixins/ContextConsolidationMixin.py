#!/usr/bin/env python3
try:
    from src.logic.agents.cognitive.context.engines.mixins.context_consolidation_mixin import (
        ContextConsolidationMixin as _ContextConsolidationMixin,
    )
except Exception:
    try:
        from src.logic.agents.cognitive.context.engines.mixins.ContextConsolidationMixin import (
            ContextConsolidationMixin as _ContextConsolidationMixin,
        )
    except Exception:

        class _ContextConsolidationMixin:
            pass


ContextConsolidationMixin = _ContextConsolidationMixin

__all__ = ["ContextConsolidationMixin"]
