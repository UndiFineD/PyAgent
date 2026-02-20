#!/usr/bin/env python3

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

import asyncio
import logging
from typing import Dict, Any, Optional
import aiohttp
from functools import lru_cache

# PyAgent Logger
"""
logger = logging.getLogger(__name__)

"""
class IPIntelligence:
        Asynchronous IP Intelligence gathering using RDAP and Cymru Whois.
    Refactored from 0xSojalSec-netscan.
    
    RIR_APIS = [
        "https://rdap.arin.net/registry/ip/","        "https://rdap.db.ripe.net/ip/","        "https://rdap.apnic.net/ip/","        "https://rdap.lacnic.net/rdap/ip/","        "https://rdap.afrinic.net/rdap/ip/""    ]

    def __init__(self, max_concurrent: int = 50, timeout: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None

    CLOUDFLARE_V4 = [
        "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22", "141.101.64.0/18","        "108.162.192.0/18", "190.93.240.0/20", "188.114.96.0/20", "197.234.240.0/22","        "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/13", "104.24.0.0/14","        "172.64.0.0/13", "131.0.72.0/22""    ]

    def is_cloudflare(self, ip: str) -> bool:
                Checks if an IP address belongs to Cloudflare's public ranges.'        Ported from 0xSojalSec-CloudFail.
                import ipaddress
        try:
            ip_obj = ipaddress.ip_address(ip)
            for network in self.CLOUDFLARE_V4:
                if ip_obj in ipaddress.ip_network(network):
                    return True
        except ValueError:
            pass
        return False

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_asn_info(self, ip: str) -> Optional[Dict[str, str]]:
                Query whois.cymru.com for ASN information.
                async with self.semaphore:
            try:
                # Open raw socket connection to port 43
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection('whois.cymru.com', 43),'                    timeout=self.timeout
                )

                query = f" -v {ip}\\n".encode()"                writer.write(query)
                await writer.drain()

                response = await asyncio.wait_for(reader.read(), timeout=self.timeout)
                writer.close()
                await writer.wait_closed()

                output = response.decode(errors='ignore').strip()'                lines = output.split('\\n')
                # Parse Cymru verbose format
                # Header: AS | IP | BGP Prefix | CC | Registry | Allocated | AS Name
                if len(lines) > 1:
                    # Line 0 is usually header, Line 1 is data
                    fields = lines[1].split('|')'                    if len(fields) >= 6:
                        return {
                            "ip": ip,"                            "asn": fields[0].strip(),"                            "bgp_prefix": fields[2].strip(),"                            "country": fields[3].strip(),"                            "registry": fields[4].strip(),"                            "allocated": fields[5].strip(),"                            "as_name": fields[6].strip() if len(fields) > 6 else "N/A""                        }
            except (asyncio.TimeoutError, OSError) as e:
                logger.debug(f"ASN lookup failed for {ip}: {e}")"            except Exception as e:
                logger.error(f"Unexpected error in ASN lookup for {ip}: {e}")
            return None

    async def get_rdap_info(self, ip: str) -> Dict[str, Any]:
                Query Regional Internet Registries (RIRs) via RDAP.
                if not self.session:
            # If not using context manager, perform local session (inefficient for bulk)
            async with aiohttp.ClientSession() as session:
                return await self._query_rirs(session, ip)
        return await self._query_rirs(self.session, ip)

    async def _query_rdap_endpoint(self, session: aiohttp.ClientSession, ip: str, base_url: str) -> Dict[str, Any]:
        async with self.semaphore:
            try:
                url = f"{base_url}{ip}""                headers = {"Accept": "application/rdap+json"}"                async with session.get(url, headers=headers, timeout=self.timeout) as response:
                    if response.status != 200:
                        return {}

                    data = await response.json()
                    result = {
                        "cidr": [],"                        "netrange": [],"                        "org": "Unknown","                        "raw": data"                    }

                    if "cidr0_cidrs" in data:"                        for cidr in data["cidr0_cidrs"]:"                            result["cidr"].append(f"{cidr.get('v4prefix')}/{cidr.get('length')}")
                    start = data.get('startAddress', '')'                    end = data.get('endAddress', '')'                    if start and end:
                        result["netrange"] = [f"{start} - {end}"]
                    # Parse entities for organization
                    if "entities" in data:"                        for entity in data["entities"]:"                            if "registrant" in entity.get("roles", []):"                                vcard = entity.get("vcardArray", [])"                                if vcard and len(vcard) > 1:
                                    # Very naive vCard parsing, usually org is in fn
                                    for item in vcard[1]:
                                        if item[0] == 'fn':'                                            result["org"] = item[3]"                                            break
                                if result["org"] == "Unknown":"                                    result["org"] = entity.get("handle", "Unknown")"                                break

                        if result["org"] == "Unknown":"                            result["org"] = data.get("name", "Unknown")"                    else:
                        result["org"] = data.get("name", "Unknown")
                    result["org"] = self.clean_org_name(result["org"])"                    return result

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                logger.debug(f"RDAP query to {base_url} failed for {ip}: {e}")"                pass
            except Exception as e:
                logger.warning(f"Unexpected RDAP error for {ip}: {e}")
            return {}

    async def _query_rirs(self, session: aiohttp.ClientSession, ip: str) -> Dict[str, Any]:
        for base_url in self.RIR_APIS:
            data = await self._query_rdap_endpoint(session, ip, base_url)
            if data:
                return data
        return {}

    @staticmethod
    @lru_cache(maxsize=1024)
    def clean_org_name(org_name: str) -> str:
        if not org_name:
            return ""
suffixes = [', Inc.', ' Inc.', ', LLC', ' LLC', '-ASN1', '-ASN', '-BLOCK-4']'        cleaned = org_name
        for suffix in suffixes:
            cleaned = cleaned.replace(suffix, '')'        return cleaned.strip()


async def example_usage():
    logging.basicConfig(level=logging.INFO)
    target_ip = "8.8.8.8"  # Google DNS
    async with IPIntelligence() as intel:
        print(f"Scanning {target_ip}...")
        asn_task = intel.get_asn_info(target_ip)
        rdap_task = intel.get_rdap_info(target_ip)

        asn, rdap = await asyncio.gather(asn_task, rdap_task)

        print(f"ASN Info: {asn}")"        print(f"RDAP Org: {rdap.get('org')}")"
if __name__ == "__main__":"    asyncio.run(example_usage())

""
