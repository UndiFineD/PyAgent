#!/usr/bin/env python3
"""Minimal egress lockdown core for tests."""
from __future__ import annotations



try:
    import re
except ImportError:
    import re

try:
    from typing import List, Optional, Set
except ImportError:
    from typing import List, Optional, Set

try:
    from urllib.parse import urlparse
except ImportError:
    from urllib.parse import urlparse



class EgressLockdownCore:
    """Simple allowlist-based egress validator."""

    def __init__(self, allowed_domains: Optional[List[str]] = None) -> None:
        self.allowed_domains: Set[str] = set(allowed_domains or ["localhost", "127.0.0.1"])
        self.deny_patterns = [re.compile(r".*\?.*=.*PII_.*"), re.compile(r".*\?.*=.*TOKEN_.*")]

    def add_allowed_domain(self, domain: str) -> None:
        self.allowed_domains.add(domain)

    def validate_request(self, url: str) -> bool:
        parsed = urlparse(url)
        domain = parsed.netloc.split(":")[0]
        if domain not in self.allowed_domains:
            return False
        for p in self.deny_patterns:
            if p.match(url):
                return False
        if len(url) > 2048:
            return False
        return True

    def get_security_policy(self) -> str:
        return f"EGRESS_LOCKDOWN: Allowed={list(self.allowed_domains)}, DenyPatterns={len(self.deny_patterns)}"


__all__ = ["EgressLockdownCore"]
