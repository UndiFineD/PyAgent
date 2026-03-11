#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/core/base/logic/security/web_security_scanner_core.description.md

# web_security_scanner_core

**File**: `src\\core\base\\logic\\security\\web_security_scanner_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 150  
**Complexity**: 2 (simple)

## Overview

Module: web_security_scanner_core
Core logic for web security scanning, refactored from aem-eye patterns.
Implements asynchronous web application scanning with pattern matching for vulnerability detection.

## Classes (1)

### `WebSecurityScannerCore`

Core logic for web security scanning operations.

**Methods** (2):
- `__init__(self, timeout, concurrency, rate_limit)`
- `_normalize_url(self, host)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `aiohttp`
- `asyncio`
- `re`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `urllib.parse.urlparse`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/security/web_security_scanner_core.improvements.md

# Improvements for web_security_scanner_core

**File**: `src\\core\base\\logic\\security\\web_security_scanner_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 150 lines (medium)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `web_security_scanner_core_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Module: web_security_scanner_core
Core logic for web security scanning, refactored from aem-eye patterns.
Implements asynchronous web application scanning with pattern matching for vulnerability detection.
"""


import asyncio
import re
import time
from typing import Dict, List, Optional
from urllib.parse import urlparse

try:
    import aiohttp

    HAS_AIOHTTP = True
except ImportError:
    aiohttp = None
    HAS_AIOHTTP = False


class WebSecurityScannerCore:
    """Core logic for web security scanning operations."""

    def __init__(self, timeout: int = 10, concurrency: int = 10, rate_limit: int = 100):
        if not HAS_AIOHTTP:
            raise ImportError("aiohttp is required for WebSecurityScannerCore")

        self.timeout = timeout
        self.concurrency = concurrency
        self.rate_limit = rate_limit
        self.semaphore = asyncio.Semaphore(concurrency)
        self.last_request_time = 0.0
        self.min_interval = 1.0 / rate_limit if rate_limit > 0 else 0.0

    async def scan_hosts(
        self, hosts: List[str], patterns: Dict[str, str]
    ) -> Dict[str, List[str]]:
        """Scan a list of hosts for security patterns.

        Args:
            hosts: List of URLs or host strings
            patterns: Dict of pattern_name -> regex_pattern

        Returns:
            Dict of host -> list of matched pattern names

        """
        results = {}
        tasks = []

        for host in hosts:
            # Normalize host to URL
            url = self._normalize_url(host)
            if url:
                task = asyncio.create_task(self._scan_single_host(url, patterns))
                tasks.append((url, task))

        # Process results
        for url, task in tasks:
            try:
                matches = await task
                if matches:
                    results[url] = matches
            except Exception as e:
                # Log error but continue
                print(f"Error scanning {url}: {e}")

        return results

    def _normalize_url(self, host: str) -> Optional[str]:
        """Normalize host string to full URL."""
        if not host.startswith(("http://", "https://")):
            host = f"http://{host}"
        try:
            parsed = urlparse(host)
            if parsed.netloc:
                return host
        except:
            pass
        return None

    async def _scan_single_host(self, url: str, patterns: Dict[str, str]) -> List[str]:
        """Scan a single host for patterns."""
        async with self.semaphore:
            # Rate limiting
            now = time.time()
            elapsed = now - self.last_request_time
            if elapsed < self.min_interval:
                await asyncio.sleep(self.min_interval - elapsed)
            self.last_request_time = time.time()

            matches = []

            try:
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                    connector=aiohttp.TCPConnector(verify_ssl=False),
                ) as session:
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }

                    async with session.get(
                        url, headers=headers, allow_redirects=True
                    ) as response:
                        if response.status == 200:
                            text = await response.text()
                            for pattern_name, regex in patterns.items():
                                if re.search(regex, text, re.IGNORECASE):
                                    matches.append(pattern_name)

            except Exception:
                # Host unreachable or error
                pass

            return matches

    async def detect_cms_fingerprints(self, hosts: List[str]) -> Dict[str, List[str]]:
        """Detect CMS fingerprints using common patterns.

        Args:
            hosts: List of hosts to scan

        Returns:
            Dict of host -> list of detected CMS types

        """
        # Common CMS detection patterns
        cms_patterns = {
            "aem": r'href="/content/dam|/etc/clientlibs',
            "wordpress": r"wp-content|wp-includes",
            "drupal": r"Drupal|drupal",
            "joomla": r"Joomla|joomla",
            "magento": r"Magento|magento",
            "shopify": r"shopify|myshopify",
        }

        return await self.scan_hosts(hosts, cms_patterns)
