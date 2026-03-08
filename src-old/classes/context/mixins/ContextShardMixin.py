#!/usr/bin/env python3
try:
    from src.logic.agents.cognitive.context.engines.mixins.context_shard_mixin import (
        ContextShardMixin as _ContextShardMixin,
    )
except Exception:
    try:
        from src.logic.agents.cognitive.context.engines.mixins.ContextShardMixin import (
            ContextShardMixin as _ContextShardMixin,
        )
    except Exception:

        class _ContextShardMixin:
            pass


ContextShardMixin = _ContextShardMixin

__all__ = ["ContextShardMixin"]
