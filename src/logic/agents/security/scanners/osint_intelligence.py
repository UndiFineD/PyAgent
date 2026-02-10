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

from typing import List, Dict


class OsintIntelligence:
    """
    Consolidates Google, Shodan, and GitHub dorks for reconnaissance.
    Ported logic from OneDorkForAll, Shodan-Dorks, and Github-Dorks.
    """

    # High-value Google Dorks
    GOOGLE_DORKS = {
        "sensitive_files": [
            'filetype:log "PHP Parse error"',
            'filetype:sql "MySQL dump"',
            "filetype:env DB_PASSWORD",
            '"index of" "config.php"',
            'intitle:"index of" "api.txt"',
        ],
        "bug_bounty": [
            'site:github.com "target.com"',
            'site:s3.amazonaws.com "target.com"',
            'site:atlassian.net "target.com"',
        ],
    }

    # High-value Shodan Dorks
    SHODAN_DORKS = [
        'product:"Elastic" port:9200',
        'product:"Redis"',
        'product:"MongoDB"',
        '"X-OWA-Version"',
        '"X-Powered-By: PHP/"',
        'title:"index of /"',
    ]

    # High-value GitHub Dorks
    GITHUB_DORKS = ['"target.com" password', '"target.com" api_key', '"target.com" token', "filename:.env target.com"]

    @staticmethod
    def generate_dorks(domain: str) -> Dict[str, List[str]]:
        """Generates domain-specific dorks."""
        results = {
            "google": [d.replace("target.com", domain) for d in OsintIntelligence.GOOGLE_DORKS["bug_bounty"]],
            "github": [d.replace("target.com", domain) for d in OsintIntelligence.GITHUB_DORKS],
            "shodan": [f"hostname:{domain}", f"http.html:{domain}", f"ssl:{domain}"],
        }
        return results

    @staticmethod
    def get_cxsecurity_dork_url(page: int = 1) -> str:
        """Returns the URL for fetching dorks from CXSecurity."""
        return f"https://cxsecurity.com/dorks/{page}"
