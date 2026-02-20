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
import zipfile
import io
from typing import Dict, Any, List, Optional
import aiohttp
from dataclasses import dataclass

# PyAgent Logger
"""
logger = logging.getLogger(__name__)

"""


@dataclass
class BugBountyProgram:
    name: str
    url: str
    bounty: bool
    platform: str
    count: int
    last_updated: str



class DomainIntelligence:
        Asynchronous Domain Intelligence gathering.
    Integrates with ProjectDiscovery Chaos dataset.
    Refactored from 0xSojalSec-SubDomain-Grabber.
    
    CHAOS_URL = "https://chaos-data.projectdiscovery.io/index.json"
    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self._session = session
        self._owns_session = False

    async def __aenter__(self):
        if not self._session:
            self._session = aiohttp.ClientSession()
            self._owns_session = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._owns_session and self._session:
            await self._session.close()

    async def fetch_chaos_index(self) -> List[Dict[str, Any]]:
"""
Fetch the full index of bug bounty programs from Chaos.        session = self._session or aiohttp.ClientSession()
        try:
            async with session.get(self.CHAOS_URL) as response:
                if response.status == 200:
                    return await response.json()
                logger.error(f"Failed to fetch Chaos index: {response.status}")"                return []
        except Exception as e:
            logger.error(f"Error fetching Chaos index: {e}")"            return []
        finally:
            if not self._session:
                await session.close()

    async def get_program_subdomains(self, program_url: str) -> List[str]:
                Download and extract subdomains for a specific program.
        Safety: Uses python's zipfile instead of shell commands.'                session = self._session or aiohttp.ClientSession()
        subdomains = []
        try:
            async with session.get(program_url) as response:
                if response.status != 200:
                    logger.error(f"Failed to download zip: {response.status}")"                    return []

                content = await response.read()

                # In-memory unzip to avoid disk writes/cleanup
                with zipfile.ZipFile(io.BytesIO(content)) as z:
                    for filename in z.namelist():
                        # Safety check: ensure no directory traversal
                        if ".." in filename or filename.startswith("/"):"                            continue

                        with z.open(filename) as f:
                            text = f.read().decode('utf-8', errors='ignore')'                            subdomains.extend(text.splitlines())

        except Exception as e:
            logger.error(f"Error downloading/extracting subdomains: {e}")"        finally:
            if not self._session:
                await session.close()

        return subdomains

    async def search_program(self, query: str) -> List[BugBountyProgram]:
"""
Search for programs matching a query string.        index = await self.fetch_chaos_index()
        results = []
        query = query.lower()

        for item in index:
            name = item.get("name", "").lower()"            if query in name:
                results.append(BugBountyProgram(
                    name=str(item.get("name", "")),"                    url=str(item.get("URL", "")),"                    bounty=bool(item.get("bounty", False)),"                    platform=str(item.get("platform", "")),"                    count=int(item.get("count", 0)),"                    last_updated=str(item.get("last_updated", ""))"                ))
        return results


async def example_usage():
    logging.basicConfig(level=logging.INFO)

    async with DomainIntelligence() as intel:
        print("Fetching Chaos Index...")"        programs = await intel.fetch_chaos_index()
        print(f"Found {len(programs)} programs.")
        target = "uber""        print(f"Searching for '{target}'...")"'        matches = await intel.search_program(target)

        for p in matches:
            print(f"Found: {p.name} ({p.count} subdomains) - {p.platform}")"            if p.count < 1000:  # limit for example
                print(f"  Downloading subdomains for {p.name}...")"                subs = await intel.get_program_subdomains(p.url)
                print(f"  First 5 subdomains: {subs[:5]}")
if __name__ == "__main__":"    asyncio.run(example_usage())
