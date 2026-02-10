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

from typing import List


class SQLInjectionIntelligence:
    """
    Refactored logic from Atlas for SQLMap Tamper suggesting and WAF bypass logic.
    """

    TAMPER_LIST = [
        "apostrophemask", "apostrophenullencode", "base64encode", "between",
        "bluecoat", "chardoubleencode", "charencode", "charunicodeencode",
        "concat2concatws", "equaltolike", "greatest", "ifnull2ifisnull",
        "modsecurityversioned", "modsecurityzeroversioned", "multiplespaces",
        "nonrecursivereplacement", "percentage", "randomcase", "securesphere",
        "space2comment", "space2dash", "space2mssqlblank", "space2mysqland",
        "space2mysqlblank", "space2plus", "space2randomblank", "sp_password",
        "unionalltounion", "unmagicquotes", "versionedkeywords", "versionedmorekeywords"
    ]

    @classmethod
    async def suggest_tampers(cls, _url: str, _payload: str, _method: str = "GET") -> List[str]:
        """
        Suggests potential tampers by testing if a modified payload bypasses a 403/406 response.
        """
        # For now, return a default set of common bypass tampers if we suspect a WAF
        return ["space2comment", "randomcase", "charencode"]

    @classmethod
    def get_all_tampers(cls) -> List[str]:
        return cls.TAMPER_LIST
