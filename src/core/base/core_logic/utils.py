# Copyright 2026 PyAgent Authors
import hashlib
import os
from typing import List, Any, Dict, Optional
from src.core.base.models import AgentConfig

try:
    import rust_core as rc
except ImportError:
    rc = None

class UtilsCore:
    def deduplicate_entries(self, entries: List[str]) -> List[str]:
        """Deduplicate string entries while preserving order."""
        if rc:
            try:
                return rc.deduplicate_entries(entries)
            except Exception:
                pass
        seen = set()
        result = []
        for entry in entries:
            if entry not in seen:
                seen.add(entry)
                result.append(entry)
        return result

    def merge_configurations(self, base: AgentConfig, override: AgentConfig) -> AgentConfig:
        """Merge two configurations."""
        return AgentConfig(
            backend=override.backend or base.backend,
            model=override.model or base.model,
            max_tokens=override.max_tokens if override.max_tokens != base.max_tokens else base.max_tokens,
            temperature=override.temperature if override.temperature != base.temperature else base.temperature,
            retry_count=override.retry_count if override.retry_count != base.retry_count else base.retry_count,
            timeout=override.timeout if override.timeout != base.timeout else base.timeout,
            cache_enabled=override.cache_enabled if override.cache_enabled != base.cache_enabled else base.cache_enabled,
            token_budget=override.token_budget if override.token_budget != base.token_budget else base.token_budget,
        )

    def generate_cache_key(self, prompt: str, context: str) -> str:
        """Logic to generate a hash for caching."""
        if rc:
            try:
                return rc.generate_cache_key(prompt, context)
            except Exception:
                pass
        combined = f"{prompt}:{context}"
        return hashlib.sha256(combined.encode()).hexdigest()

    def get_default_content(self, filename: str) -> str:
        """Logic for default content based on file extension."""
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".py": return "#!/usr/bin/env python3\n\npass\n"
        elif ext in [".md", ".markdown"]: return "# New Document\n"
        return ""
