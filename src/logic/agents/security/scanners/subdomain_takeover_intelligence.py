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
import dns.resolver
from typing import List, Dict, Any, Optional, cast


class SubdomainTakeoverIntelligence:
    """
    Detects potential subdomain takeover vulnerabilities by checking CNAME records
    and analyzing HTTP responses for known service fingerprints.
    Ported logic from subjack and subowner.
    """

    # Combined fingerprints from subjack and other sources
    TAKEOVER_SIGNATURES: List[Dict[str, Any]] = [
        {"service": "fastly", "cname": ["fastly"], "fingerprint": ["Fastly error: unknown domain"], "nxdomain": False},
        {
            "service": "github",
            "cname": ["github.io"],
            "fingerprint": ["There isn't a GitHub Pages site here."],
            "nxdomain": False,
        },
        {
            "service": "heroku",
            "cname": ["herokuapp"],
            "fingerprint": ["herokucdn.com/error-pages/no-such-app.html"],
            "nxdomain": False,
        },
        {
            "service": "pantheon",
            "cname": ["pantheonsite.io"],
            "fingerprint": ["The gods are wise, but do not know of the site which you seek."],
            "nxdomain": False,
        },
        {
            "service": "tumblr",
            "cname": ["domains.tumblr.com"],
            "fingerprint": ["Whatever you were looking for doesn't currently exist at this address."],
            "nxdomain": False,
        },
        {
            "service": "wordpress",
            "cname": ["wordpress.com"],
            "fingerprint": ["Do you want to register"],
            "nxdomain": False,
        },
        {
            "service": "teamwork",
            "cname": ["teamwork.com"],
            "fingerprint": ["Oops - We didn't find your site."],
            "nxdomain": False,
        },
        {
            "service": "helpjuice",
            "cname": ["helpjuice.com"],
            "fingerprint": ["We could not find what you're looking for."],
            "nxdomain": False,
        },
        {
            "service": "helpscout",
            "cname": ["helpscoutdocs.com"],
            "fingerprint": ["No settings were found for this company:"],
            "nxdomain": False,
        },
        {
            "service": "s3 bucket",
            "cname": ["amazonaws"],
            "fingerprint": ["The specified bucket does not exist"],
            "nxdomain": False,
        },
        {
            "service": "ghost",
            "cname": ["ghost.io"],
            "fingerprint": ["The thing you were looking for is no longer here, or never was"],
            "nxdomain": False,
        },
        {
            "service": "shopify",
            "cname": ["myshopify.com"],
            "fingerprint": ["Sorry, this shop is currently unavailable."],
            "nxdomain": False,
        },
        {
            "service": "uservoice",
            "cname": ["uservoice.com"],
            "fingerprint": ["This UserVoice subdomain is currently available!"],
            "nxdomain": False,
        },
        {"service": "surge", "cname": ["surge.sh"], "fingerprint": ["project not found"], "nxdomain": False},
        {"service": "bitbucket", "cname": ["bitbucket.io"], "fingerprint": ["Repository not found"], "nxdomain": False},
        {
            "service": "intercom",
            "cname": ["custom.intercom.help"],
            "fingerprint": ["This page is reserved for artistic dogs.", "Uh oh. That page doesn't exist."],
            "nxdomain": False,
        },
        {
            "service": "webflow",
            "cname": ["proxy.webflow.com", "proxy-ssl.webflow.com"],
            "fingerprint": ["The page you are looking for doesn't exist or has been moved."],
            "nxdomain": False,
        },
        {
            "service": "azure",
            "cname": [
                ".azurewebsites.net",
                ".cloudapp.net",
                ".cloudapp.azure.com",
                ".trafficmanager.net",
                ".blob.core.windows.net",
            ],
            "fingerprint": ["404 Not Found"],
            "nxdomain": True,
        },
        {"service": "zendesk", "cname": ["zendesk.com"], "fingerprint": ["Help Center Closed"], "nxdomain": False},
        {
            "service": "readme",
            "cname": ["readme.io"],
            "fingerprint": ["Project doesnt exist... yet!"],
            "nxdomain": False,
        },
    ]

    def __init__(self):
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 2.0
        self.resolver.lifetime = 2.0

    async def get_cnames(self, domain: str) -> List[str]:
        """Resolves CNAME records for a domain."""
        try:
            loop = asyncio.get_event_loop()
            answers = await loop.run_in_executor(None, lambda: self.resolver.resolve(domain, "CNAME"))
            return [str(rdata.target).rstrip(".") for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
            return []
        except Exception:
            return []

    async def check_takeover(self, domain: str) -> Optional[Dict[str, Any]]:
        """Checks if a domain is vulnerable to takeover."""
        cnames = await self.get_cnames(domain)

        # If no CNAME, check for NXDOMAIN vulnerability if applicable for some services
        # (Though usually CNAME is required for these fingerprints)

        for cname in cnames:
            for sig in self.TAKEOVER_SIGNATURES:
                # Explicitly cast to List[str] for MyPy
                cname_patterns = cast(List[str], sig["cname"])
                match = any(pattern in cname.lower() for pattern in cname_patterns)
                if match:
                    # Potential match, verify with HTTP
                    status, body = await self._fetch_url(domain)
                    fingerprints = cast(List[str], sig["fingerprint"])
                    for fp in fingerprints:
                        if fp.lower() in body.lower():
                            return {
                                "domain": domain,
                                "cname": cname,
                                "service": sig["service"],
                                "vulnerable": True,
                                "fingerprint_match": fp,
                            }
                    if sig["nxdomain"]:
                        # Some azure/apigee services are vulnerable if they return NXDOMAIN or 404
                        if status == 404:
                            return {
                                "domain": domain,
                                "cname": cname,
                                "service": sig["service"],
                                "vulnerable": True,
                                "status": 404,
                            }
        return None

    async def _fetch_url(self, domain: str) -> tuple[int, str]:
        """Fetches URL content safely."""
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for proto in ["https://", "http://"]:
                try:
                    async with session.get(f"{proto}{domain}", ssl=False) as resp:
                        return resp.status, await resp.text()
                except Exception:
                    continue
        return 0, ""


async def main():
    # Example usage
    intel = SubdomainTakeoverIntelligence()
    result = await intel.check_takeover("test.github.io")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
