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
import esprima
from bs4 import BeautifulSoup
from rapidfuzz import fuzz
from typing import List, Dict, Optional, Tuple


class ParameterIntelligence:
    """
    Advanced URL parameter discovery and testing.
    Combines logic from ParamScan, ParamPamPam (Dichotomy search), and common wordlists.
    """

    REDIRECT_PARAMS = [
        "url",
        "redirect",
        "next",
        "destination",
        "dest",
        "out",
        "view",
        "to",
        "from",
        "show",
        "path",
        "continue",
        "return",
        "returnTo",
        "return_to",
        "checkout",
        "checkout_url",
        "image_url",
        "go",
        "return_url",
        "Lmage_url",
        "Open",
        "cgi-bin/redirect.cgi",
        "continue",
        "data",
        "dir",
        "domain",
        "feed",
        "forward",
        "from_url",
        "goto",
        "host",
        "html",
        "img_url",
        "load_file",
        "load_url",
        "login?to",
        "login_url",
        "logout",
        "navigation",
        "next_page",
        "page_url",
        "redir",
        "reference",
        "rt",
        "rurl",
        "site",
        "target",
        "uri",
        "val",
        "validate",
        "window",
    ]

    # Categorized parameter patterns for vulnerability identification
    CATEGORIES = {
        "xss": (
            r"(api=|api_key=|begindate=|callback=|=|categoryid=|csrf_token=|email=|emailto=|enddate=|id=|"
            r"imagine=|immagine=|item=|jsonp=|key=|keyword=|keywords=|l=|lang=|list_type=|month=|name=|"
            r"p=|page=|page_id=|password=|pid=|pp=|q=|query=|s=|search=|terms=|token=|type=|"
            r"unsubscribe_token=|url=|username=|view=|year=)"
        ),
        "sqli": (
            r"(id=|select=|report=|role=|update=|query=|user=|name=|sort=|where=|search=|params=|process=|"
            r"row=|view=|table=|from=|sel=|results=|sleep=|fetch=|order=|keyword=|column=|field=|"
            r"delete=|string=|number=|filter=)"
        ),
        "ssti": r"(template=|preview=|id=|view=|activity=|name=|content=|redirect=)",
        "ssrf": (
            r"(access=|admin=|dbg=|debug=|edit=|grant=|test=|alter=|clone=|create=|delete=|disable=|"
            r"enable=|exec=|execute=|load=|make=|modify=|rename=|reset=|shell=|toggle=|adm=|root=|cfg=|"
            r"dest=|redirect=|uri=|path=|continue=|url=|window=|next=|data=|reference=|site=|html=|val=|"
            r"validate=|domain=|callback=|return=|page=|feed=|host=|port=|to=|out=|view=|dir=|show=|"
            r"navigation=|open=|file=|document=|folder=|pg=|php_path=|style=|doc=|img=|filename=)"
        ),
        "lfi": (
            r"(file=|document=|folder=|root=|path=|pg=|style=|pdf=|template=|php_path=|doc=|page=|name=|"
            r"cat=|dir=|action=|board=|date=|detail=|download=|prefix=|include=|inc=|locate=|show=|"
            r"site=|type=|view=|content=|layout=|mod=|conf=|url=)"
        ),
        "rce": (
            r"(daemon=|upload=|dir=|download=|log=|ip=|cli=|cmd=|exec=|command=|execute=|ping=|query=|"
            r"jump=|code=|reg=|do=|func=|arg=|option=|load=|process=|step=|read=|function|req=|"
            r"feature=|exe=|module=|payload=|run=|print=)"
        ),
    }

    FILE_EXT_PATTERN = (
        r"(\.asp|\.aspx|\.bat|\.cfm|\.cgi|\.css|\.dll|\.exe|\.htm|\.html|\.inc|\.jhtml|\.js|\.jsa|"
        r"\.jsp|\.log|\.mdb|\.nsf|\.pcap|\.php|\.php2|\.php3|\.php4|\.php5|\.php6|\.php7|\.phps|"
        r"\.pht|\.phtml|\.pl|\.reg|\.sh|\.shtml|\.sql|\.swf|\.txt|\.xml|\.ini|\,xml|\.bat|\.LOG|"
        r"\.tn|\.bak|\.sql)"
    )

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self.session = session
        self.found_parameters: Dict[str, List[str]] = {}

    async def get_response(self, url: str, params: Dict[str, str]) -> Tuple[int, str, int]:
        """Helper to get response status, text, and length."""
        if not self.session:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, ssl=False, timeout=10) as resp:
                    text = await resp.text()
                    return resp.status, text, len(text)
        else:
            async with self.session.get(url, params=params, ssl=False, timeout=10) as resp:
                text = await resp.text()
                return resp.status, text, len(text)

    def compare_responses(self, base_text: str, test_text: str, base_len: int, test_len: int) -> bool:
        """Determines if two responses are significantly different."""
        if base_len != test_len:
            return False
        # Fuzzy comparison for dynamic content
        if fuzz.ratio(base_text, test_text) < 98:
            return False
        return True

    async def discover_parameters_dichotomy(self, url: str, wordlist: List[str]) -> List[str]:
        """
        Implements dichotomy (binary search) for fast parameter discovery.
        """
        status, base_text, base_len = await self.get_response(url, {})
        found = []

        async def check_batch(batch: List[str]):
            params = {p: "pyagent_test" for p in batch}
            _, test_text, test_len = await self.get_response(url, params)

            if not self.compare_responses(base_text, test_text, base_len, test_len):
                if len(batch) == 1:
                    found.append(batch[0])
                else:
                    mid = len(batch) // 2
                    await asyncio.gather(check_batch(batch[:mid]), check_batch(batch[mid:]))

        # Process in chunks to avoid URL length limits
        chunk_size = 50
        for i in range(0, len(wordlist), chunk_size):
            await check_batch(wordlist[i : i + chunk_size])

        return found

    def extract_from_html(self, html: str) -> List[str]:
        """Parses HTML for name/id attributes."""
        soup = BeautifulSoup(html, "html.parser")
        params = []
        for tag in soup.find_all(attrs=True):
            if "name" in tag.attrs:
                params.append(tag.attrs["name"])
            if "id" in tag.attrs:
                params.append(tag.attrs["id"])
        return list(set(params))

    def extract_from_js(self, js_code: str) -> List[str]:
        """Parses JS for identifiers using esprima."""
        params = []
        try:
            tokens = esprima.tokenize(js_code)
            for token in tokens:
                if token.type == "Identifier" and len(token.value) > 1:
                    params.append(token.value)
        except Exception:
            pass
        return list(set(params))
