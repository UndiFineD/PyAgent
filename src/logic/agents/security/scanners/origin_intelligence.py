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

import aiohttp
import dns.asyncresolver
from typing import List, Dict, Any


class OriginRecon:
    """
    Attempts to find the origin IP of a website behind a CDN.
    Ported from Origin_Recon.
    """

    def __init__(self):
        self.resolver = dns.asyncresolver.Resolver()
        self.resolver.nameservers = ["1.1.1.1", "8.8.8.8"]

    async def get_subdomains_from_crt(self, domain: str, session: aiohttp.ClientSession) -> List[str]:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        try:
            async with session.get(url, timeout=20) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return list({entry["name_value"].lower().strip() for entry in data})
        except Exception:
            pass
        return []

    async def check_ip_origin(self, domain: str, ip: str, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """
        Compares the Target Domain (CDN) with the direct IP response.
        """
        results: Dict[str, Any] = {"ip": ip, "reasons": [], "is_origin": False}

        try:
            # Check for high TTL on the domain itself (CDN check)
            answers = await self.resolver.resolve(domain, "A")
            if answers.rrset and answers.rrset.ttl > 300:
                results["reasons"].append(f"High TTL ({answers.rrset.ttl}s)")

            # Direct IP request
            headers = {"Host": domain}
            async with session.get(
                f"http://{ip}", headers=headers, timeout=5, ssl=False, allow_redirects=False
            ) as resp:
                server_header = resp.headers.get("Server", "").lower()

                # If the domain is behind Cloudflare but the IP shows Nginx/Apache/IIS directly
                if "cloudflare" not in server_header and server_header:
                    results["reasons"].append(f"Direct Server Banner: {server_header}")
                    results["is_origin"] = True

                # Check for sensitive headers usually stripped by CDNs
                if any(h in resp.headers for h in ["X-Powered-By", "X-AspNet-Version", "X-Runtime"]):
                    results["reasons"].append("Leaked Backend Technology Headers")
                    results["is_origin"] = True

        except Exception:
            pass

        return results


async def find_origin(domain: str):
    async with aiohttp.ClientSession() as session:
        recon = OriginRecon()
        await recon.get_subdomains_from_crt(domain, session)
        # Further logic for scanning these subdomains and their IPs...
        pass
