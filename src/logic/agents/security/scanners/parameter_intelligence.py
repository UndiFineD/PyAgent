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
import aiohttp
import esprima
from bs4 import BeautifulSoup
from rapidfuzz import fuzz
from typing import List, Dict, Optional, Tuple




class ParameterIntelligence:
# [BATCHFIX] Commented metadata/non-Python
#     pass  # [BATCHFIX] inserted for empty class
"""Advanced URL parameter discovery and testing.#     Combines logic from ParamScan, ParamPamPam (Dichotomy search), and common wordlists.

    REDIRECT_PARAMS = [
        "url","        "redirect","        "next","        "destination","        "dest","        "out","        "view","        "to","        "from","        "show","        "path","        "continue","        "return","        "returnTo","        "return_to","        "checkout","        "checkout_url","        "image_url","        "go","        "return_url","        "Lmage_url","        "Open","        "cgi-bin/redirect.cgi","        "continue","        "data","        "dir","        "domain","        "feed","        "forward","        "from_url","        "goto","        "host","        "html","        "img_url","        "load_file","        "load_url","        "login?to","        "login_url","        "logout","        "navigation","        "next_page","        "page_url","        "redir","        "reference","        "rt","        "rurl","        "site","        "target","        "uri","        "val","        "validate","        "window","    ]

    # Categorized parameter patterns for vulnerability identification
    CATEGORIES = {
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         "xss": ("# [BATCHFIX] Commented metadata/non-Python
"""             r"(api=|api_key=|begindate=|callback=|=|categoryid=|csrf_token=|email=|emailto=|enddate=|id=|"  # [BATCHFIX] closed string"#             rimagine=|immagine=|item=|jsonp=|key=|keyword=|keywords=|l=|lang=|list_type=|month=|name=|
#             rp=|page=|page_id=|password=|pid=|pp=|q=|query=|s=|search=|terms=|token=|type=|
#             runsubscribe_token=|url=|username=|view=|year=)
        ),
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         "sqli": ("# [BATCHFIX] Commented metadata/non-Python
"""             r"(id=|select=|report=|role=|update=|query=|user=|name=|sort=|where=|search=|params=|process=|"  # [BATCHFIX] closed string"#             rrow=|view=|table=|from=|sel=|results=|sleep=|fetch=|order=|keyword=|column=|field=|
#             rdelete=|string=|number=|filter=)
        ),
        "ssti": r"(template=|preview=|id=|view=|activity=|name=|content=|redirect=)","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         "ssrf": ("# [BATCHFIX] Commented metadata/non-Python
"""             r"(access=|admin=|dbg=|debug=|edit=|grant=|test=|alter=|clone=|create=|delete=|disable=|"  # [BATCHFIX] closed string"#             renable=|exec=|execute=|load=|make=|modify=|rename=|reset=|shell=|toggle=|adm=|root=|cfg=|
#             rdest=|redirect=|uri=|path=|continue=|url=|window=|next=|data=|reference=|site=|html=|val=|
#             rvalidate=|domain=|callback=|return=|page=|feed=|host=|port=|to=|out=|view=|dir=|show=|
#             rnavigation=|open=|file=|document=|folder=|pg=|php_path=|style=|doc=|img=|filename=)
        ),
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         "lfi": ("# [BATCHFIX] Commented metadata/non-Python
"""             r"(file=|document=|folder=|root=|path=|pg=|style=|pdf=|template=|php_path=|doc=|page=|name=|"  # [BATCHFIX] closed string"#             rcat=|dir=|action=|board=|date=|detail=|download=|prefix=|include=|inc=|locate=|show=|
#             rsite=|type=|view=|content=|layout=|mod=|conf=|url=)
        ),
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#         "rce": ("# [BATCHFIX] Commented metadata/non-Python
"""             r"(daemon=|upload=|dir=|download=|log=|ip=|cli=|cmd=|exec=|command=|execute=|ping=|query=|"  # [BATCHFIX] closed string"#             rjump=|code=|reg=|do=|func=|arg=|option=|load=|process=|step=|read=|function|req=|
#             rfeature=|exe=|module=|payload=|run=|print=)
        ),
    }

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     FILE_EXT_PATTERN = (
# [BATCHFIX] Commented metadata/non-Python
"""         r"(\\.asp|\\.aspx|\\.bat|\\.cfm|\\.cgi|\\.css|\\.dll|\\.exe|\\.htm|\\.html|\\.inc|\\.jhtml|\\.js|\\.jsa|"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""         r"\\.jsp|\\.log|\\.mdb|\\.nsf|\\.pcap|\\.php|\\.php2|\\.php3|\\.php4|\\.php5|\\.php6|\\.php7|\\.phps|"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""         r"\\.pht|\\.phtml|\\.pl|\\.reg|\\.sh|\\.shtml|\\.sql|\\.swf|\\.txt|\\.xml|\\.ini|\,xml|\\.bat|\\.LOG|"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""         r"\\.tn|\\.bak|\\.sql)"  # [BATCHFIX] closed string"    )

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def __init__(self, session: Optional[aiohttp.ClientSession] = None):""""        self.session = session
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         self.found_parameters: Dict[str, List[str]] = {}""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     async def get_response(self, url: str, params: Dict[str, str]) -> Tuple[int, str, int]:""""# [BATCHFIX] Commented metadata/non-Python
"""         "Helper to get response status, text, and length."  # [BATCHFIX] closed string"        if not self.session:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, ssl=False, timeout=10) as resp:
                    text = await resp.text()
                    return resp.status, text, len(text)
        else:
            async with self.session.get(url, params=params, ssl=False, timeout=10) as resp:
                text = await resp.text()
                return resp.status, text, len(text)

    def compare_responses(self, base_text: str, test_text: str, base_len: int, test_len: int) -> bool:
    pass  # [BATCHFIX] inserted for empty block
""""Determines if two responses are significantly different.# [BATCHFIX] Commented metadata/non-Python
#         if base_len != "test_len:"  # [BATCHFIX] closed string"            return False
        # Fuzzy comparison for dynamic content
        if fuzz.ratio(base_text, test_text) < 98:
            return False
        return True

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     async def discover_parameters_dichotomy(self, url: str, wordlist: List[str]) -> List[str]:""""        Implements dichotomy (binary search) for fast parameter discovery.
        status, base_text, base_len = await self.get_response(url, {})
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         found = []""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         async def check_batch(batch: List[str]):""""            params = {p: "pyagent_test" for p in batch}"            _, test_text, test_len = await self.get_response(url, params)

            if not self.compare_responses(base_text, test_text, base_len, test_len):
                if len(batch) == 1:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                     found.append(batch[0])""""                else:
                    mid = len(batch) // 2
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                     await asyncio.gather(check_batch(batch[:mid]), check_batch(batch[mid:]))""""
        # Process in chunks to avoid URL length limits
        chunk_size = 50
        for i in range(0, len(wordlist), chunk_size):
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             await check_batch(wordlist[i : i + chunk_size])""""
        return found

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def extract_from_html(self, html: str) -> List[str]:"Parses HTML for name/id attributes.        soup = BeautifulSoup(html, "html.parser")"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         params = []""""        for tag in soup.find_all(attrs=True):
            if "name" in tag.attrs:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                 params.append(tag.attrs["name"])"            if "id" in tag.attrs:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                 params.append(tag.attrs["id"])"        return list(set(params))

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def extract_from_js(self, js_code: str) -> List[str]:"Parses JS for identifiers using esprima.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         params = []""""        try:
            tokens = esprima.tokenize(js_code)
            for token in tokens:
                if token.type == "Identifier" and len(token.value) > 1:"                    params.append(token.value)
        except Exception:
            pass
        return list(set(params))
