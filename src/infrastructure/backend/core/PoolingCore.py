
from __future__ import annotations
from typing import Dict, List
import re

class PoolingCore:
    """
    PoolingCore implements logic for HTTP/2 connection pooling and prompt compression.
    It prepares requests for faster TTFT (Time to First Token).
    """

    def __init__(self) -> None:
        # Stop words and redundant phrases for prompt compression
        self.compression_patterns = [
            (r"\bplease\b", ""),
            (r"\bi would like you to\b", ""),
            (r"\bthank you\b", ""),
            (r"\bhelpful assistant\b", "assistant"),
            (r"\s+", " ") # Collapse whitespace
        ]

    def compress_prompt(self, text: str) -> str:
        """
        Compresses a system prompt by removing redundant social tokens.
        (Simplified LLMLinqua-like logic).
        """
        compressed = text
        for pattern, replacement in self.compression_patterns:
            compressed = re.sub(pattern, replacement, compressed, flags=re.IGNORECASE)
        return compressed.strip()

    def select_best_endpoint(self, preferred_host: str, endpoint_stats: Dict[str, float]) -> str:
        """
        Selects the lowest-latency endpoint from a pool based on recent stats.
        """
        if not endpoint_stats:
            return preferred_host
            
        return min(endpoint_stats, key=endpoint_stats.get)

    def should_reuse_session(self, host: str, active_sessions: List[str]) -> bool:
        """Checks if a host already has an active persistent session."""
        return host in active_sessions