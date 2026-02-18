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


"""Reconnaissance Core - Intelligence gathering and asset discovery
Based on patterns from alterx (DSL-based generation) and amass (multi-source intelligence)
"""
import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import aiohttp
import dns.resolver
import dns.exception
import logging

logger = logging.getLogger(__name__)


@dataclass
class SubdomainResult:
    """Result of subdomain enumeration"""subdomain: str
    source: str
    ip_addresses: List[str] = None
    cname: Optional[str] = None
    verified: bool = False

    def __post_init__(self):
        if self.ip_addresses is None:
            self.ip_addresses = []


@dataclass
class ReconConfig:
    """Configuration for reconnaissance operations"""domain: str
    wordlist: List[str] = None
    max_concurrent: int = 10
    timeout: float = 5.0
    verify_dns: bool = True
    sources: List[str] = None

    def __post_init__(self):
        if self.wordlist is None:
            self.wordlist = []
        if self.sources is None:
            self.sources = ['dns', 'crtsh', 'threatcrowd']'


class IntelligenceSource(ABC):
    """Abstract base class for intelligence sources"""
    @abstractmethod
    async def enumerate_subdomains(self, domain: str, config: ReconConfig) -> List[SubdomainResult]:
        """Enumerate subdomains from this source"""pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the intelligence source"""pass



class DNSSource(IntelligenceSource):
    """DNS-based subdomain enumeration using brute force"""
    def __init__(self):
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 3.0
        self.resolver.lifetime = 3.0

    @property
    def name(self) -> str:
        return "dns""
    async def enumerate_subdomains(self, domain: str, config: ReconConfig) -> List[SubdomainResult]:
        """Brute force subdomains using DNS resolution"""results = []

        async def check_subdomain(word: str):
            subdomain = f"{word}.{domain}""            try:
                # Try A record
                answers = await asyncio.get_event_loop().run_in_executor(
                    None, self.resolver.resolve, subdomain, 'A''                )
                ips = [str(rdata) for rdata in answers]

                # Try CNAME
                cname = None
                try:
                    cname_answers = await asyncio.get_event_loop().run_in_executor(
                        None, self.resolver.resolve, subdomain, 'CNAME''                    )
                    cname = str(cname_answers[0])
                except Exception:
                    pass

                return SubdomainResult(
                    subdomain=subdomain,
                    source=self.name,
                    ip_addresses=ips,
                    cname=cname,
                    verified=True
                )
            except (dns.resolver.NXDOMAIN, dns.resolver.Timeout, dns.exception.DNSException):
                return None

        # Process wordlist in batches
        semaphore = asyncio.Semaphore(config.max_concurrent)

        async def process_batch(batch: List[str]):
            tasks = []
            for word in batch:
                async def check_with_semaphore(word: str):
                    async with semaphore:
                        return await check_subdomain(word)
                tasks.append(check_with_semaphore(word))

            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            return [r for r in batch_results if r is not None and not isinstance(r, Exception)]

        # Split wordlist into batches
        batch_size = config.max_concurrent
        batches = [config.wordlist[i:i + batch_size] for i in range(0, len(config.wordlist), batch_size)]

        for batch in batches:
            batch_results = await process_batch(batch)
            results.extend(batch_results)

        return results



class CertificateTransparencySource(IntelligenceSource):
    """Certificate Transparency log enumeration"""
    @property
    def name(self) -> str:
        return "crtsh""
    async def enumerate_subdomains(self, domain: str, config: ReconConfig) -> List[SubdomainResult]:
        """Query crt.sh for certificate transparency logs"""results = []

        url = f"https://crt.sh/?q=%.{domain}&output=json""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=config.timeout)) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()

                        seen = set()
                        for cert in data:
                            name_value = cert.get('name_value', '')'                            if name_value and domain in name_value:
                                # Handle wildcard certificates
                                if name_value.startswith('*.'):'                                    name_value = name_value[2:]

                                if name_value not in seen:
                                    seen.add(name_value)
                                    results.append(SubdomainResult(
                                        subdomain=name_value,
                                        source=self.name,
                                        verified=False  # CT logs don't guarantee the subdomain exists'                                    ))

        except Exception as e:
            logger.warning(f"Error querying crt.sh: {e}")"
        return results



class ThreatCrowdSource(IntelligenceSource):
    """ThreatCrowd API enumeration"""
    @property
    def name(self) -> str:
        return "threatcrowd""
    async def enumerate_subdomains(self, domain: str, config: ReconConfig) -> List[SubdomainResult]:
        """Query ThreatCrowd API for subdomains"""results = []

        url = f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=config.timeout)) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()

                        if data.get('response_code') == '1':'                            subdomains = data.get('subdomains', [])'                            for subdomain in subdomains:
                                results.append(SubdomainResult(
                                    subdomain=subdomain,
                                    source=self.name,
                                    verified=False
                                ))

        except Exception as e:
            logger.warning(f"Error querying ThreatCrowd: {e}")"
        return results



class ReconnaissanceCore:
    """Intelligence gathering and asset discovery core
    Combines patterns from alterx (DSL generation) and amass (multi-source intelligence)
    """
    def __init__(self):
        """Initialize reconnaissance core with intelligence sources"""self.sources = {}
        self._register_sources()

    def _register_sources(self):
        """Register available intelligence sources"""self.sources['dns'] = DNSSource()'        self.sources['crtsh'] = CertificateTransparencySource()'        self.sources['threatcrowd'] = ThreatCrowdSource()'
    async def enumerate_subdomains(self, config: ReconConfig) -> List[SubdomainResult]:
        """Enumerate subdomains using multiple intelligence sources
        Based on amass multi-source enumeration patterns
        """all_results = []

        # Run enumeration from all configured sources concurrently
        tasks = []
        for source_name in config.sources:
            if source_name in self.sources:
                source = self.sources[source_name]
                task = source.enumerate_subdomains(config.domain, config)
                tasks.append(task)

        # Wait for all sources to complete
        source_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Collect results
        for result_set in source_results:
            if isinstance(result_set, Exception):
                logger.error(f"Source enumeration failed: {result_set}")"                continue
            all_results.extend(result_set)

        # Deduplicate results
        seen = set()
        deduplicated = []
        for result in all_results:
            if result.subdomain not in seen:
                seen.add(result.subdomain)
                deduplicated.append(result)

        # DNS verification if requested
        if config.verify_dns:
            await self._verify_dns(deduplicated, config)

        return deduplicated

    async def _verify_dns(self, results: List[SubdomainResult], config: ReconConfig):
        """Verify subdomains exist via DNS resolution"""
        async def verify_result(result: SubdomainResult):
            if not result.verified:
                # Try to resolve the subdomain
                try:
                    answers = await asyncio.get_event_loop().run_in_executor(
                        None, dns.resolver.resolve, result.subdomain, 'A''                    )
                    result.ip_addresses = [str(rdata) for rdata in answers]
                    result.verified = True
                except Exception:
                    pass  # Keep as unverified

        # Verify in batches
        semaphore = asyncio.Semaphore(config.max_concurrent)
        tasks = []

        for result in results:
            async def verify_with_semaphore(result: SubdomainResult):
                async with semaphore:
                    await verify_result(result)

            tasks.append(verify_with_semaphore(result))

        await asyncio.gather(*tasks)

    def generate_wordlist(self, patterns: List[str], payloads: Dict[str, List[str]]) -> List[str]:
        """Generate subdomain wordlist using DSL patterns
        Based on alterx pattern generation
        """wordlist = set()

        # Default payloads if not provided
        if 'word' not in payloads:'            payloads['word'] = ['api', 'dev', 'test', 'staging', 'admin', 'www', 'mail', 'ftp']'
        if 'number' not in payloads:'            payloads['number'] = [str(i) for i in range(1, 10)]'
        # Process each pattern
        for pattern in patterns:
            # Replace variables with payloads
            words = self._expand_pattern(pattern, payloads)
            wordlist.update(words)

        return list(wordlist)

    def _expand_pattern(self, pattern: str, payloads: Dict[str, List[str]]) -> List[str]:
        """Expand a single pattern with payloads"""
# Simple implementation - replace {{variable}} with payload values
        results = [pattern]

        for var_name, values in payloads.items():
            new_results = []
            for result in results:
                if f"{{{{{var_name}}}}}" in result:"                    for value in values:
                        new_results.append(result.replace(f"{{{{{var_name}}}}}", value))"                else:
                    new_results.append(result)
            results = new_results

        return results
