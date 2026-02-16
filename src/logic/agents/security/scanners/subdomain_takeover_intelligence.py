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
import dns.resolver
from typing import List, Dict, Any, Optional, cast


class SubdomainTakeoverIntelligence:
# [BATCHFIX] Commented metadata/non-Python
#     pass  # [BATCHFIX] inserted for empty class
"""Detects potential subdomain takeover vulnerabilities by checking CNAME records"""
#     and analyzing HTTP responses for known service fingerprints.
# [BATCHFIX] Commented metadata/non-Python
#     Ported logic from subjack and subowner.
# #

    # Combined fingerprints from subjack and other sources
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     TAKEOVER_SIGNATURES: List[Dict[str, Any]] = [
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         {"service": "fastly", "cname": ["fastly"], "fingerprint": ["Fastly error: unknown domain"], "nxdomain": False},
        {
            "service": "github",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cname": ["github.io"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#             "fingerprint": ["There isn't a GitHub Pages site here."],"  # [BATCHFIX] closed string
            "nxdomain": False,
        },
        {
            "service": "heroku",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cname": ["herokuapp"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "fingerprint": ["herokucdn.com/error-pages/no-such-app.html"],
            "nxdomain": False,
        },
        {
            "service": "pantheon",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cname": ["pantheonsite.io"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "fingerprint": ["The gods are wise, but do not know of the site which you seek."],
            "nxdomain": False,
        },
        {
            "service": "tumblr",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cname": ["domains.tumblr.com"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#             "fingerprint": ["Whatever you were looking for doesn't currently exist at this address."],"  # [BATCHFIX] closed string
            "nxdomain": False,
        },
        {
            "service": "wordpress",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cname": ["wordpress.com"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "fingerprint": ["Do you want to register"],
            "nxdomain": False,
        },
        {
            "service": "teamwork",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cname": ["teamwork.com"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#             "fingerprint": ["Oops - We didn't find your site."],"  # [BATCHFIX] closed string
            "nxdomain": False,
        },
        {
            "service": "helpjuice",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cname": ["helpjuice.com"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#             "fingerprint": ["We could not find what you're looking for."],"  # [BATCHFIX] closed string
            "nxdomain": False,
        },
        {
            "service": "helpscout",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cname": ["helpscoutdocs.com"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "fingerprint": ["No settings were found for this company:"],
            "nxdomain": False,
        },
        {
            "service": "s3 bucket",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cname": ["amazonaws"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "fingerprint": ["The specified bucket does not exist"],
            "nxdomain": False,
        },
        {
            "service": "ghost",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cname": ["ghost.io"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "fingerprint": ["The thing you were looking for is no longer here, or never was"],
            "nxdomain": False,
        },
        {
            "service": "shopify",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cname": ["myshopify.com"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "fingerprint": ["Sorry, this shop is currently unavailable."],
            "nxdomain": False,
        },
        {
            "service": "uservoice",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cname": ["uservoice.com"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "fingerprint": ["This UserVoice subdomain is currently available!"],
            "nxdomain": False,
        },
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         {"service": "surge", "cname": ["surge.sh"], "fingerprint": ["project not found"], "nxdomain": False},
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         {"service": "bitbucket", "cname": ["bitbucket.io"], "fingerprint": ["Repository not found"], "nxdomain": False},
        {
            "service": "intercom",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cname": ["custom.intercom.help"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#             "fingerprint": ["This page is reserved for artistic dogs.", "Uh oh. That page doesn't exist."],"  # [BATCHFIX] closed string
            "nxdomain": False,
        },
        {
            "service": "webflow",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cname": ["proxy.webflow.com", "proxy-ssl.webflow.com"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#             "fingerprint": ["The page you are looking for doesn't exist or has been moved."],"  # [BATCHFIX] closed string
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
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "fingerprint": ["404 Not Found"],
            "nxdomain": True,
        },
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         {"service": "zendesk", "cname": ["zendesk.com"], "fingerprint": ["Help Center Closed"], "nxdomain": False},
        {
            "service": "readme",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cname": ["readme.io"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "fingerprint": ["Project doesnt exist... yet!"],
            "nxdomain": False,
        },
    ]

    def __init__(self):
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 2.0
        self.resolver.lifetime = 2.0

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     async def get_cnames(self, domain: str) -> List[str]:
# [BATCHFIX] Commented metadata/non-Python
# #         "Resolves CNAME records for a domain."  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#       "  try:"  # [BATCHFIX] closed string
            loop = asyncio.get_event_loop()
            answers = await loop.run_in_executor(None, lambda: self.resolver.resolve(domain, "CNAME"))
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             return [str(rdata.target).rstrip(".") for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             return []
        except Exception:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             return []

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     async def check_takeover(self, domain: str) -> Optional[Dict[str, Any]]:
# [BATCHFIX] Commented metadata/non-Python
# #         "Checks if a domain is vulnerable to takeover."  # [BATCHFIX] closed string
        cnames = await self.get_cnames(domain)

        # If no CNAME, check for NXDOMAIN vulnerability if applicable for some services
        # (Though usually CNAME is required for these fingerprints)

        for cname in cnames:
            for sig in self.TAKEOVER_SIGNATURES:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                 # Explicitly cast to List[str] for MyPy
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                 cname_patterns = cast(List[str], sig["cname"])
                match = any(pattern in cname.lower() for pattern in cname_patterns)
                if match:
                    # Potential match, verify with HTTP
                    status, body = await self._fetch_url(domain)
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                     fingerprints = cast(List[str], sig["fingerprint"])
                    for fp in fingerprints:
                        if fp.lower() in body.lower():
                            return {
                                "domain": domain,
                                "cname": cname,
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                                 "service": sig["service"],
                                "vulnerable": True,
                                "fingerprint_match": fp,
                            }
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                     if sig["nxdomain"]:
                        # Some azure/apigee services are vulnerable if they return NXDOMAIN or 404
                        if status == 404:
                            return {
                                "domain": domain,
                                "cname": cname,
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                                 "service": sig["service"],
                                "vulnerable": True,
                                "status": 404,
                            }
        return None

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     async def _fetch_url(self, domain: str) -> tuple[int, str]:
# [BATCHFIX] Commented metadata/non-Python
# #         "Fetches URL content safely."  # [BATCHFIX] closed string
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             for proto in ["https://", "http://"]:
                try:
                    async with session.get(f"{proto}{domain}", ssl=False) as resp:
                        return resp.status, await resp.text()
                except Exception:
                    continue
#         return 0,


async def main():
    # Example usage
    intel = SubdomainTakeoverIntelligence()
    result = await intel.check_takeover("test.github.io")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
