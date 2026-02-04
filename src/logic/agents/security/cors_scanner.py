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
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse
from dataclasses import dataclass

@dataclass
class CORSVulnerability:
    url: str
    vulnerability_type: str
    description: str
    severity: str
    exploitation: str
    acao_header: Optional[str]
    acac_header: Optional[str]

class CORSScanner:
    """
    Ported logic from 0xSojalSec-Corsy.
    Scans a target URL for CORS misconfigurations.
    """

    DETAILS = {
        "wildcard value" : {
            "class" : "wildcard value",
            "description" : "This host allows requests made from any origin. However, browsers will block all requests to this host by default.",
            "severity" : "low",
            "exploitation" : "Not possible"
        },
        "third party allowed" : {
            "class" : "third party allowed",
            "description" : "This host has whitelisted a third party host for cross origin requests.",
            "severity" : "Medium",
            "exploitation" : "If the whitelisted host is a code hosting platform such as codepen.io or has an XSS vulnerability, it can be used to exploit this misconfiguration."

        },
        "origin reflected": {
            "class" : "origin reflected",
            "description" : "This host allows any origin to make requests to it.",
            "severity" : "high",
            "exploitation" : "Make requests from any domain you control."
        },
        "invalid value" : {
            "class" : "invalid value",
            "description" : "Header's value is invalid, this CORS implementation doesn't work at all.",
            "severity" : "low",
            "exploitation" : "Not possible"
        },
        "post-domain wildcard" : {
            "class" : "post-domain wildcard",
            "description" : "The origin verification is flawed, it allows requests from a host that has this host as a prefix.",
            "severity" : "high",
            "exploitation" : "Make requests from target.com.attacker.com"
        },
        "pre-domain wildcard" : {
            "class" : "pre-domain wildcard",
            "description" : "The origin verification is flawed, it allows requests from a host that has this host as a suffix.",
            "severity" : "high",
            "exploitation" : "Make requests from attacker-target.com"
        },
        "null origin allowed" : {
            "class" : "null origin allowed",
            "description" : "This host allows requests from 'null' origin.",
            "severity" : "high",
            "exploitation" : "Make requests from a sandboxed iframe."
        },
        "http origin allowed" : {
            "class" : "http origin allowed",
            "description" : "This host allows sharing resources over an unencrypted (HTTP) connection.",
            "severity" : "low",
            "exploitation" : "Sniff requests made over the unencrypted channel."
        },
        "unrecognized underscore": {
            "class": "unrecognized underscore",
            "description": "The origin verification allowed an origin with an underscore which might not be what was intended.",
            "severity": "medium",
            "exploitation": "Depends on regex implementation."
        },
        "broken parser": {
            "class": "broken parser",
            "description": "The origin verification allowed a malformed origin which indicates a broken parser.",
            "severity": "medium",
            "exploitation": "Depends on the parser implementation."
        },
        "unescaped regex": {
            "class": "unescaped regex",
            "description": "The origin verification allowed a dot variation, suggesting unescaped regex.",
            "severity": "high",
            "exploitation": "Register a domain that matches the regex (e.g. siteXcom)."
        }
    }

    def __init__(self, timeout: int = 10, concurrency: int = 10):
        self.timeout = timeout
        self.semaphore = asyncio.Semaphore(concurrency)

    def _get_host(self, url: str) -> str:
        parsed = urlparse(url)
        return parsed.netloc

    async def _request(self, session: aiohttp.ClientSession, url: str, origin: str) -> Dict[str, str]:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Origin': origin
        }
        try:
            async with self.semaphore:
                async with session.get(url, headers=headers, timeout=self.timeout, ssl=False) as response:
                    return response.headers
        except Exception:
            return {}

    async def scan(self, url: str) -> List[CORSVulnerability]:
        """
        Runs the suite of CORS tests against the target URL.
        """
        results = []
        parsed = urlparse(url)
        if not parsed.scheme:
            url = f"http://{url}"
            parsed = urlparse(url)
        
        root = parsed.netloc
        scheme = parsed.scheme
        target_url = f"{scheme}://{root}{parsed.path}"

        # Logic ported from active_tests in core/tests.py
        
        async with aiohttp.ClientSession() as session:
            
            # 1. Origin Reflected
            origin = f"{scheme}://example.com"
            headers = await self._request(session, target_url, origin)
            acao = headers.get('Access-Control-Allow-Origin')
            acac = headers.get('Access-Control-Allow-Credentials')
            if acao and acao == origin:
                results.append(self._create_vuln(target_url, 'origin reflected', acao, acac))

            # 2. Post-domain wildcard
            origin = f"{scheme}://{root}.example.com"
            headers = await self._request(session, target_url, origin)
            acao = headers.get('Access-Control-Allow-Origin')
            acac = headers.get('Access-Control-Allow-Credentials')
            if acao and acao == origin:
                results.append(self._create_vuln(target_url, 'post-domain wildcard', acao, acac))

            # 3. Pre-domain wildcard
            origin = f"{scheme}://d3v{root}"
            headers = await self._request(session, target_url, origin)
            acao = headers.get('Access-Control-Allow-Origin')
            acac = headers.get('Access-Control-Allow-Credentials')
            if acao and acao == origin:
                results.append(self._create_vuln(target_url, 'pre-domain wildcard', acao, acac))

            # 4. Null origin
            origin = "null"
            headers = await self._request(session, target_url, origin)
            acao = headers.get('Access-Control-Allow-Origin')
            acac = headers.get('Access-Control-Allow-Credentials')
            if acao and acao == "null":
                results.append(self._create_vuln(target_url, 'null origin allowed', acao, acac))

            # 5. Unrecognized underscore
            origin = f"{scheme}://{root}_.example.com"
            headers = await self._request(session, target_url, origin)
            acao = headers.get('Access-Control-Allow-Origin')
            acac = headers.get('Access-Control-Allow-Credentials')
            if acao and acao == origin:
                results.append(self._create_vuln(target_url, 'unrecognized underscore', acao, acac))

            # 6. Broken Parser
            origin = f"{scheme}://{root}%60.example.com"
            headers = await self._request(session, target_url, origin)
            acao = headers.get('Access-Control-Allow-Origin')
            acac = headers.get('Access-Control-Allow-Credentials')
            if acao and '`.example.com' in acao:
                 results.append(self._create_vuln(target_url, 'broken parser', acao, acac))

            # 7. Unescaped Regex
            if root.count('.') > 1:
                origin = f"{scheme}://{root.replace('.', 'x', 1)}"
                headers = await self._request(session, target_url, origin)
                acao = headers.get('Access-Control-Allow-Origin')
                acac = headers.get('Access-Control-Allow-Credentials')
                if acao and acao == origin:
                    results.append(self._create_vuln(target_url, 'unescaped regex', acao, acac))

            # 8. HTTP Origin Allowed
            origin = f"http://{root}"
            headers = await self._request(session, target_url, origin)
            acao = headers.get('Access-Control-Allow-Origin')
            acac = headers.get('Access-Control-Allow-Credentials')
            if acao and acao.startswith("http://"):
                results.append(self._create_vuln(target_url, 'http origin allowed', acao, acac))

            # 9. Passive / Wildcard
            # (Just check the response from the first request or a generic one)
            # We can re-use the target_url but with a trusted origin to see default behavior or generic info
            origin = f"{scheme}://{root}"
            headers = await self._request(session, target_url, origin)
            acao = headers.get('Access-Control-Allow-Origin')
            acac = headers.get('Access-Control-Allow-Credentials')
            
            if acao == '*':
                results.append(self._create_vuln(target_url, 'wildcard value', acao, acac))
            elif acao and self._get_host(acao) and root != self._get_host(acao):
                 results.append(self._create_vuln(target_url, 'third party allowed', acao, acac))

        return results

    def _create_vuln(self, url: str, key: str, acao: Optional[str], acac: Optional[str]) -> CORSVulnerability:
        info = self.DETAILS.get(key, {
            "class": key,
            "description": "Unknown vulnerability",
            "severity": "Unknown",
            "exploitation": "Unknown"
        })
        return CORSVulnerability(
            url=url,
            vulnerability_type=info['class'],
            description=info['description'],
            severity=info['severity'],
            exploitation=info['exploitation'],
            acao_header=acao,
            acac_header=acac
        )

# Example usage
async def main():
    scanner = CORSScanner()
    # Mocking for test purposes or CLI usage
    # vulns = await scanner.scan("http://example.com")
    # for v in vulns:
    #     print(v)

if __name__ == "__main__":
    asyncio.run(main())
