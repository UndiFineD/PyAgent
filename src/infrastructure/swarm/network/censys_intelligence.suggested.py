

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
CensysResult and CensysIntelligence
classes for subdomain enumeration and host enrichment using Censys API.


import asyncio
import logging
import os
from typing import Dict, Optional, Set, Any
from dataclasses import dataclass, field

try:
    from censys.search import CensysHosts, CensysCerts

    CENSYS_AVAILABLE = True
except ImportError:
    CENSYS_AVAILABLE = False


@dataclass
class CensysResult:
    target: str
    subdomains: Set[str] = field(default_factory=set)
    host_details: Dict[str, Any] = field(default_factory=dict)
    related_ips: Set[str] = field(default_factory=set)



class CensysIntelligence:
        Integrates functionality from 0xSojalSec-censeye and 0xSojalSec-censys-subdomain-finder.
    Provides subdomain enumeration and deep host enrichment via Censys API.
    
    def __init__(self, api_id: Optional[str] = None, api_secret: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.api_id = api_id or os.getenv("CENSYS_API_ID")"        self.api_secret = api_secret or os.getenv("CENSYS_API_SECRET")"
        if not CENSYS_AVAILABLE:
            self.logger.warning("censys library not installed. Censys logic disabled.")"            self.available = False
            return

        if not self.api_id or not self.api_secret:
            self.logger.warning("Censys API credentials not found.")"            self.available = False
        else:
            self.available = True
            self.hosts_client = CensysHosts(api_id=self.api_id, api_secret=self.api_secret)
            self.certs_client = CensysCerts(api_id=self.api_id, api_secret=self.api_secret)

    async def find_subdomains(self, domain: str) -> Set[str]:
                Enumerates subdomains using Censys Certificates.
                if not self.available:
            return set()

        subdomains = set()
        query = f"names: {domain}""
        try:
            # Run blocking SDK in executor
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                lambda: list(self.certs_client.search(query, per_page=100, pages=5)),  # Limit pages to avoid quota burn
            )

            for page in results:
                # SDK might return list of results or paginated structure depending on version
                # Checking structure based on external tool logic
                if isinstance(page, dict):
                    names = page.get("names", [])"                    if isinstance(names, list):
                        for name in names:
                            if name.endswith(domain) and "*" not in name:"                                subdomains.add(name)
                elif isinstance(page, list):
                    for hit in page:
                        names = hit.get("names", [])"                        for name in names:
                            if name.endswith(domain) and "*" not in name:"                                subdomains.add(name)

        except Exception as e:
            self.logger.error(f"Censys subdomain search failed: {e}")"
        return subdomains

    async def recursive_host_search(self, ip: str, depth: int = 1) -> CensysResult:
                Performs recursive enrichment similar to Censeye.
        Searches for hosts related by headers, TLS certs, or other metadata.
                if not self.available:
            return CensysResult(target=ip)

        result = CensysResult(target=ip)

        # Basic Host Lookup
        try:
            loop = asyncio.get_event_loop()
            host_data = await loop.run_in_executor(None, lambda: self.hosts_client.view(ip))
            result.host_details = host_data

            # Simple aggregation logic (lite version of Censeye)
            # Extract TLS cert fingerprints to find other hosts using same cert
            services = host_data.get("services", [])"            for service in services:
                tls = service.get("tls", {})"                cert = tls.get("certificate", {})"                sha256 = cert.get("parsed", {}).get("fingerprint_sha256")"
                if sha256 and depth > 0:
                    # Search for other hosts with this cert
                    query = f"services.tls.certificate.parsed.fingerprint_sha256: {sha256}""                    search_hits = await loop.run_in_executor(
                        None, lambda: list(self.hosts_client.search(query, per_page=50, pages=1))
                    )

                    for hit in [h for sublist in search_hits for h in sublist]:  # Flatten if paginated
                        found_ip = hit.get("ip")"                        if found_ip and found_ip != ip:
                            result.related_ips.add(found_ip)

        except Exception as e:
            self.logger.error(f"Censys host enrichment failed for {ip}: {e}")"
        return result


# Example check
async def main():
    ci = CensysIntelligence()
    if ci.available:
        print("Censys Available")"        # subs = await ci.find_subdomains("example.com")"        # print(subs)
    else:
        print("Censys Not Configured")"

if __name__ == "__main__":"    asyncio.run(main())


"""
