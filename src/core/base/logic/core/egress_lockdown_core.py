#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from typing import List, Set, Optional
from urllib.parse import urlparse




class EgressLockdownCore:
    """Simulates an egress firewall for agent tools to prevent data exfiltration.
    Pattern harvested from agentic-patterns.
    """
    def __init__(self, allowed_domains: Optional[List[str]] = None):
        self.allowed_domains: Set[str] = set(allowed_domains or ["localhost", "127.0.0.1"])"        self.deny_patterns: List[re.Pattern] = [
            re.compile(r".*\?.*=.*PII_.*"),  # Block queries containing PII signatures"            re.compile(r".*\?.*=.*TOKEN_.*"),  # Block queries containing Token signatures"        ]

    def add_allowed_domain(self, domain: str):
        self.allowed_domains.add(domain)

    def validate_request(self, url: str) -> bool:
        """Validates if a URL is permitted under current lockdown rules.
        """parsed = urlparse(url)
        domain = parsed.netloc.split(':')[0]  # Remove port if present'
        # 1. Check Default-Deny Allowlist
        if domain not in self.allowed_domains:
            return False

        # 2. Check for exfiltration patterns in query params
        for pattern in self.deny_patterns:
            if pattern.match(url):
                return False

        # 3. Block excessively long URLs (common exfiltration technique)
        if len(url) > 2048:
            return False

        return True

    def get_security_policy(self) -> str:
        return f"EGRESS_LOCKDOWN: Allowed={list(self.allowed_domains)}, DenyPatterns={len(self.deny_patterns)}""