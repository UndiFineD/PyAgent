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
from typing import List, Dict, Optional

class ProxyIntelligence:
    """Intelligence engine for proxy discovery and validation."""

    SOURCES = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://www.proxy-list.download/api/v1/get?type=https",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
    ]

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self.session = session

    async def scrape_proxies(self) -> List[str]:
        """Scrape common free proxy lists."""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        all_proxies = []
        for url in self.SOURCES:
            try:
                async with self.session.get(url, timeout=15) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        proxies = re.findall(r"\d+\.\d+\.\d+\.\d+:\d+", text)
                        all_proxies.extend(proxies)
            except:
                continue
        return list(set(all_proxies))

    async def validate_proxy(self, proxy: str, test_url: str = "http://httpbin.org/ip") -> bool:
        """Validate if a proxy is working and anonymous."""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            async with self.session.get(test_url, proxy=f"http://{proxy}", timeout=10) as resp:
                if resp.status == 200:
                    return True
        except:
            pass
        return False

    @staticmethod
    def get_proxy_evasion_tips() -> List[str]:
        """Tips for using proxies to evade detection."""
        return [
            "Use SOCKS5 for better protocol support and encryption",
            "Rotate proxies every 10-50 requests",
            "Match the proxy location with the target domain's CDN edge if possible",
            "Check headers for leaking 'X-Forwarded-For' or 'Via'",
            "Use residential proxies to bypass datacenter IP blocks"
        ]
