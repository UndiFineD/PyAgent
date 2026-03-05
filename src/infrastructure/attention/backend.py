#!/usr/bin/env python3
try:
    from src.infrastructure.engine.attention.backend import *  # noqa: F401,F403
except Exception:
    # Fallback placeholders to avoid import-time failures during collection
    def get_attention_registry():
        raise RuntimeError("attention backend registry not available")

    class AttentionBackend:
        pass

    class AttentionBackendEnum:
        pass

    class AttentionBackendRegistry:
        pass

    class AttentionCapabilities:
        pass

    class AttentionMetadata:
        pass

    class AttentionType:
        pass

    class FlashAttentionBackend:
        pass

    class FlashInferBackend:
        pass

    class NaiveAttentionBackend:
        pass

    class PackKVAttentionBackend:
        pass

    class TorchSDPABackend:
        pass


__all__ = [
    "AttentionBackend",
    "AttentionBackendEnum",
    "AttentionBackendRegistry",
    "AttentionCapabilities",
    "AttentionMetadata",
    "AttentionType",
    "FlashAttentionBackend",
    "FlashInferBackend",
    "NaiveAttentionBackend",
    "PackKVAttentionBackend",
    "TorchSDPABackend",
    "get_attention_registry",
]
