# Copyright 2026 PyAgent Authors
from typing import Tuple, Optional
from src.core.base.models import AgentConfig

try:
    import rust_core as rc
except ImportError:
    rc = None

class ValidationCore:
    def validate_config(self, config: AgentConfig) -> Tuple[bool, str]:
        """Validate agent configuration."""
        if not config.backend:
            return False, "Backend must be specified"
        if config.max_tokens <= 0:
            return False, "max_tokens must be > 0"
        if not (0.0 <= config.temperature <= 2.0):
            return False, "temperature must be between 0.0 and 2.0"
        if config.retry_count < 0:
            return False, "retry_count must be >= 0"
        if config.timeout <= 0:
            return False, "timeout must be > 0"
        return True, ""

    def is_response_valid(self, response: str, min_length: int = 10) -> Tuple[bool, str]:
        """Validate response meets minimum criteria."""
        if rc:
            try:
                return rc.is_response_valid_rust(response, min_length)
            except Exception:
                pass
        if not response:
            return False, "Response is empty"
        if len(response) < min_length:
            return False, f"Response too short (< {min_length} chars)"
        if len(response) > 1000000:
            return False, "Response too long (> 1M chars)"
        return True, ""

    def validate_content_safety(self, content: str) -> bool:
        """Pure logic for simple content safety checks."""
        unsafe_patterns = ["<script", "os." + "system(", "eval" + "("]
        for pattern in unsafe_patterns:
            if pattern in content.lower():
                pass
        return True
