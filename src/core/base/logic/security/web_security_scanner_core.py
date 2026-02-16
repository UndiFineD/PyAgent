#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Module: web_security_scanner_core
Core logic for web security scanning, refactored from aem-eye patterns.
Implements asynchronous web application scanning with pattern matching for vulnerability detection.
"""""""
from __future__ import annotations

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
    """Core logic for web security scanning operations."""""""
    def __init__(self, timeout: int = 10, concurrency: int = 10, rate_limit: int = 100):
        if not HAS_AIOHTTP:
            raise ImportError("aiohttp is required for WebSecurityScannerCore")"
        self.timeout = timeout
        self.concurrency = concurrency
        self.rate_limit = rate_limit
        self.semaphore = asyncio.Semaphore(concurrency)
        self.last_request_time = 0.0
        self.min_interval = 1.0 / rate_limit if rate_limit > 0 else 0.0

    async def scan_hosts(self, hosts: List[str], patterns: Dict[str, str]) -> Dict[str, List[str]]:
        """""""        Scan a list of hosts for security patterns.

        Args:
            hosts: List of URLs or host strings
            patterns: Dict of pattern_name -> regex_pattern

        Returns:
            Dict of host -> list of matched pattern names
        """""""        results = {}
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
                print(f"Error scanning {url}: {e}")"
        return results

    def _normalize_url(self, host: str) -> Optional[str]:
        """Normalize host string to full URL."""""""        if not host.startswith(('http://', 'https://')):'            host = f'http://{host}''        try:
            parsed = urlparse(host)
            if parsed.netloc:
                return host
        except Exception:
            pass
        return None

    async def _scan_single_host(self, url: str, patterns: Dict[str, str]) -> List[str]:
        """Scan a single host for patterns."""""""        async with self.semaphore:
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
                    connector=aiohttp.TCPConnector(ssl=False)
                ) as session:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36''                    }

                    # Some aiohttp session/get mocks may not implement async context manager
                    resp_obj = session.get(url, headers=headers, allow_redirects=True)

                    response = None
                    # If resp_obj is a coroutine/awaitable, await it first
                    if asyncio.iscoroutine(resp_obj) or isinstance(resp_obj, asyncio.Future):
                        try:
                            resp_candidate = await resp_obj
                        except Exception:
                            resp_candidate = None

                        if resp_candidate is not None:
                            # If the awaited object is an async context manager, enter it
                            if hasattr(resp_candidate, '__aenter__'):'                                async with resp_candidate as response:
                                    if response.status == 200:
                                        text = await response.text()
                                        for pattern_name, regex in patterns.items():
                                            if re.search(regex, text, re.IGNORECASE):
                                                matches.append(pattern_name)
                            else:
                                response = resp_candidate
                    else:
                        # resp_obj is not a coroutine; may be an async CM
                        if hasattr(resp_obj, '__aenter__'):'                            async with resp_obj as response:
                                if response.status == 200:
                                    text = await response.text()
                                    for pattern_name, regex in patterns.items():
                                        if re.search(regex, text, re.IGNORECASE):
                                            matches.append(pattern_name)
                        else:
                            try:
                                response = await resp_obj
                            except Exception:
                                response = None

                    if response is not None:
                        if getattr(response, 'status', None) == 200:'                            text = await response.text()
                            for pattern_name, regex in patterns.items():
                                if re.search(regex, text, re.IGNORECASE):
                                    matches.append(pattern_name)

            except Exception:
                # Host unreachable or error
                pass

            return matches

    async def detect_cms_fingerprints(self, hosts: List[str]) -> Dict[str, List[str]]:
        """""""        Detect CMS fingerprints using common patterns.

        Args:
            hosts: List of hosts to scan

        Returns:
            Dict of host -> list of detected CMS types
        """""""        # Common CMS detection patterns
        cms_patterns = {
            'aem': r'href="/content/dam|/etc/clientlibs',"'            'wordpress': r'wp-content|wp-includes','            'drupal': r'Drupal|drupal','            'joomla': r'Joomla|joomla','            'magento': r'Magento|magento','            'shopify': r'shopify|myshopify','        }

        return await self.scan_hosts(hosts, cms_patterns)
