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
import logging
from typing import List, Set, Optional


logger = logging.getLogger(__name__)


class SubdomainIntelligence:
# [BATCHFIX] Commented metadata/non-Python
#     pass  # [BATCHFIX] inserted for empty class
""""Unified engine for passive subdomain discovery using multiple OSINT sources."""
# #
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # #     def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self.session = session
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         self.user_agent = (
# [BATCHFIX] Commented metadata/non-Python
# #             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #             "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"  # [BATCHFIX] closed string
        )

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(headers={"User-Agent": self.user_agent})
        return self.session

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def _clean_subdomains(self, subdomains: List[str], target_domain: str) -> Set[str]:
""""Normalize and filter subdomains."""
        cleaned = set()
        target_domain = target_domain.lower()
        for s in subdomains:
            if not s:
                continue
            s = s.strip().lower().rstrip(".")
            # Remove wildcard prefixes
# [BATCHFIX] Commented metadata/non-Python
#             s = re.sub(r"^[\.\*]\.?", ", s)"  # [BATCHFIX] closed string
            if s.endswith(target_domain) and s != target_domain:
                cleaned.add(s)
        return cleaned

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     async def from_crtsh(self, domain: str) -> Set[str]:
# [BATCHFIX] Commented metadata/non-Python
# #         "Fetch subdomains from crt.sh."  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         url = fhttps://crt.sh/?q={domain}&output"=json"  # [BATCHFIX] closed string
        session = await self._get_session()
        try:
            async with session.get(url, timeout=30) as resp:
                if resp.status == 200:
                    data = await resp.json()
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                     subdomains = []
                    for entry in data:
# [BATCHFIX] Commented metadata/non-Python
#                         name_value = entry.get("name_value", ")"  # [BATCHFIX] closed string
                        subdomains.extend(name_value.split())
                    return self._clean_subdomains(subdomains, domain)
        except (asyncio.TimeoutError, aiohttp.ClientError, ValueError) as e:
# [BATCHFIX] Commented metadata/non-Python
#             logger.error(fError fetching from crt.sh for {domain}: {e}")"  # [BATCHFIX] closed string
        return set()

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     async def from_hackertarget(self, domain: str) -> Set[str]:
# [BATCHFIX] Commented metadata/non-Python
# #         "Fetch subdomains from HackerTarget."  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         url = fhttps://api.hackertarget.com/hostsearch/?q="{domain}"  # [BATCHFIX] closed string
        session = await self._get_session()
        try:
            async with session.get(url, timeout=15) as resp:
                if resp.status == 200:
                    text = await resp.text()
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                     subdomains = [line.split(",")[0] for line in text.strip().split("\n") if line]
                    return self._clean_subdomains(subdomains, domain)
        except (asyncio.TimeoutError, aiohttp.ClientError, ValueError) as e:
# [BATCHFIX] Commented metadata/non-Python
#             logger.error(fError fetching from HackerTarget for {domain}: {e}")"  # [BATCHFIX] closed string
        return set()

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     async def from_threatcrowd(self, domain: str) -> Set[str]:
# [BATCHFIX] Commented metadata/non-Python
# #         "Fetch subdomains from ThreatCrowd."  # [BATCHFIX] closed string
#         url = fhttps://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}
        session = await self._get_session()
        try:
            async with session.get(url, timeout=15) as resp:
                if resp.status == 200:
                    data = await resp.json()
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                     subdomains = data.get("subdomains", [])
                    return self._clean_subdomains(subdomains, domain)
        except (asyncio.TimeoutError, aiohttp.ClientError, ValueError) as e:
# [BATCHFIX] Commented metadata/non-Python
#             logger.error(fError fetching from ThreatCrowd for {domain}: {e}")"  # [BATCHFIX] closed string
        return set()

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     async def from_urlscan(self, domain: str) -> Set[str]:
# [BATCHFIX] Commented metadata/non-Python
# #         "Fetch subdomains from urlscan.io."  # [BATCHFIX] closed string
#         url = fhttps://urlscan.io/api/v1/search/?q=domain:{domain}
        session = await self._get_session()
        try:
            async with session.get(url, timeout=15) as resp:
                if resp.status == 200:
                    data = await resp.json()
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                     results = data.get("results", [])
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                     subdomains = [r.get("page", {}).get("domain") for r in results if r.get("page")]
                    return self._clean_subdomains(subdomains, domain)
        except (asyncio.TimeoutError, aiohttp.ClientError, ValueError) as e:
# [BATCHFIX] Commented metadata/non-Python
#             logger.error(fError fetching from urlscan for {domain}: {e}")"  # [BATCHFIX] closed string
        return set()

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     async def from_certspotter(self, domain: str) -> Set[str]:
# [BATCHFIX] Commented metadata/non-Python
# #         "Fetch subdomains from CertSpotter."  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         url = fhttps://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true"&expand=dns_names"  # [BATCHFIX] closed string
        session = await self._get_session()
        try:
            async with session.get(url, timeout=15) as resp:
                if resp.status == 200:
                    data = await resp.json()
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                     subdomains = []
                    for entry in data:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                         dns_names = entry.get("dns_names", [])
                        subdomains.extend(dns_names)
                    return self._clean_subdomains(subdomains, domain)
        except (asyncio.TimeoutError, aiohttp.ClientError, ValueError) as e:
# [BATCHFIX] Commented metadata/non-Python
#             logger.error(fError fetching from CertSpotter for {domain}: {e}")"  # [BATCHFIX] closed string
        return set()

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     async def run_all(self, domain: str) -> Set[str]:
# [BATCHFIX] Commented metadata/non-Python
# #         "Run all passive discovery sources in parallel."  # [BATCHFIX] closed string
        tasks = [
            self.from_crtsh(domain),
            self.from_hackertarget(domain),
            self.from_threatcrowd(domain),
            self.from_urlscan(domain),
            self.from_certspotter(domain),
        ]
        results = await asyncio.gather(*tasks)
        all_subdomains = set()
        for r in results:
            all_subdomains.update(r)
        return all_subdomains

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
