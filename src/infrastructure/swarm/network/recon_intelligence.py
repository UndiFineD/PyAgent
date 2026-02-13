#!/usr/bin/env python3
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

import aiohttp
from typing import List, Dict, Set


class ReconIntelligence:
    """
    Refactored Reconnaissance logic from Argus.
    Focuses on OSINT and infrastructure detection.
    """

    FIREWALL_SIGNATURES = {
        'cloudflare': 'Cloudflare Firewall',
        'akamai': 'Akamai Firewall',
        'sucuri': 'Sucuri Firewall',
        'imperva': 'Imperva Firewall',
        'incapsula': 'Incapsula Firewall',
        'f5 big-ip': 'F5 BIG-IP',
        'bunnycdn': 'BunnyCDN'
    }

    @classmethod
    async def detect_waf(cls, url: str) -> Set[str]:
        results = set()
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as response:
                    headers = response.headers
                    server = headers.get('Server', '').lower()

                    for sig, name in cls.FIREWALL_SIGNATURES.items():
                        if sig in server:
                            results.add(name)

                    if 'X-Akamai' in headers:
                        results.add('Akamai Firewall')
                    if 'x-sucuri-id' in headers:
                        results.add('Sucuri Firewall')
                    if 'x-amz-cf-id' in headers:
                        results.add('AWS CloudFront/Shield')
            except Exception:
                pass
        return results

    @classmethod
    async def search_exposed_data(cls, query: str) -> Dict[str, List[Dict]]:
        """
        Search for leaked data on Scylla and Pastebin (public APIs).
        """
        out = {"scylla": [], "pastebin": []}
        async with aiohttp.ClientSession() as session:
            # Scylla
            try:
                scylla_url = f"https://scylla.sh/search?q=email:*@{query}&size=10"
                async with session.get(scylla_url, timeout=15) as resp:
                    if resp.status == 200:
                        out["scylla"] = await resp.json()
            except Exception:
                pass

            # Pastebin (v3 API emulator often used by scanners)
            try:
                paste_url = f"https://psbdmp.ws/api/v3/search/{query}"
                async with session.get(paste_url, timeout=15) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        out["pastebin"] = data.get('data', [])
            except Exception:
                pass
        return out
