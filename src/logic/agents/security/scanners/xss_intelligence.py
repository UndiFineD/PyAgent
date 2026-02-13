#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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

import asyncio
import aiohttp
import re
from typing import List, Optional
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class XssIntelligence:
    """
    Refactored XSS detection logic from various external tools (AutoRecon-XSS, etc).
    Focuses on reflected XSS by verifying payload reflection in responses.
    """

    DEFAULT_PAYLOADS = [
        "<script>alert(1)</script>",
        '"><script>alert(1)</script>',
        "';alert(1)//",
        '";alert(1)//',
        "<img src=x onerror=alert(1)>",
        "javascript:alert(1)",
    ]

    @classmethod
    async def verify_reflection(cls, url: str, payloads: Optional[List[str]] = None) -> List[str]:
        """
        Injects payloads into URL parameters and checks if they are reflected in the response.
        Inspired by AutoRecon-XSS and qsreplace workflows.
        """
        if not payloads:
            payloads = cls.DEFAULT_PAYLOADS

        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        if not params:
            return []

        found = []
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for param_name in params:
                for payload in payloads:
                    # Replace only the current parameter value
                    new_params = params.copy()
                    new_params[param_name] = [payload]

                    test_query = urlencode(new_params, doseq=True)
                    test_url = urlunparse(parsed._replace(query=test_query))

                    try:
                        async with session.get(test_url, allow_redirects=True) as resp:
                            if resp.status == 200:
                                text = await resp.text()
                                if payload in text:
                                    found.append(test_url)
                                    # Optimization: if one payload works on this param, maybe move to next param
                                    break
                    except (asyncio.TimeoutError, aiohttp.ClientError):
                        continue
        return found

    @classmethod
    async def scan_dom_xss(cls, url: str) -> List[str]:
        """
        Heuristic scan for DOM-based XSS by looking for dangerous sinks in JS.
        Logic adapted from various DOM XSS scripts.
        """
        # Patterns for dangerous sinks and sources
        SINKS = re.compile(r"(eval|setTimeout|setInterval|innerHTML|outerHTML|document\.write|docment\.writeln)\s*\(")
        SOURCES = re.compile(r"(location\.(search|hash|href|pathname)|document\.(URL|referrer|cookie)|window\.name)")

        findings = []
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                # 1. Fetch the main page
                async with session.get(url) as resp:
                    if resp.status == 200:
                        content = await resp.text()

                        # Check inline scripts
                        if SINKS.search(content) and SOURCES.search(content):
                            findings.append(f"Potential inline DOM XSS sink/source found in {url}")

                        # 2. Extract and fetch external JS files
                        js_files = re.findall(r'src=["\'](.*?\.js)["\']', content)
                        base_url = f"{parsed.scheme}://{parsed.netloc}" if (parsed := urlparse(url)) else ""

                        for js_path in js_files:
                            if not js_path.startswith("http"):
                                js_url = f"{base_url.rstrip('/')}/{js_path.lstrip('/')}"
                            else:
                                js_url = js_path

                            try:
                                async with session.get(js_url, timeout=5) as js_resp:
                                    if js_resp.status == 200:
                                        js_content = await js_resp.text()
                                        if SINKS.search(js_content) and SOURCES.search(js_content):
                                            findings.append(f"Potential DOM XSS in external script: {js_url}")
                            except (asyncio.TimeoutError, aiohttp.ClientError):
                                continue
            except (asyncio.TimeoutError, aiohttp.ClientError):
                pass
        return findings
