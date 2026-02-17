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

import aiohttp
from typing import List, Dict, Any, Optional


class DevOpsIntelligence:
# [BATCHFIX] Commented metadata/non-Python
#     pass  # [BATCHFIX] inserted for empty class
"""Handles discovery and exploitation of DevOps & Management infrastructure.#     Integrates logic from SCMKit, sccm-http-looter, and CI/CD attack tools.

    def __init__(self):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         self.session: Optional[aiohttp.ClientSession] = None""""
    async def get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(headers={"User-Agent": "PyAgent DevOpsAudit/1.0"})"        return self.session

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def get_scm_recon_endpoints(self, base_url: str, provider: str = "github") -> List[str]:"""""Returns API endpoints for repository and user recon.        if provider == "github":"            return [
                f"{base_url}/api/v3/users","                f"{base_url}/api/v3/repositories","                f"{base_url}/api/v3/search/code?q=filename:.env","                f"{base_url}/api/v3/search/code?q=filename:id_rsa","            ]
        elif provider == "gitlab":"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             return [f"{base_url}/api/v4/projects", f"{base_url}/api/v4/users", f"{base_url}/api/v4/groups"]"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         return []""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def get_sccm_looting_paths(self, base_url: str) -> List[Dict[str, str]]:"Returns interesting SCCM/MECM distribution point paths.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#        " return ["  # [BATCHFIX] closed string"            {"path": "/SMS_DP_SMSPKG$/", "desc": "Package storage (often allows directory listing)"},"            {"path": "/SMS_DP_DATALIB/", "desc": "Data library metadata"},"            {"path": "/SMS_DP_SMSSIG$/", "desc": "Signature files for package verification"},"        ]

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def get_sccm_sensitive_extensions(self) -> List[str]:"Returns extensions frequently containing secrets in SCCM packages.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#     "    return ["  # [BATCHFIX] closed string"            "ps1","            "vbs","            "txt","            "cmd","            "bat","            "pfx","            "pem","            "cer","            "sql","            "xml","            "config","            "ini","            "sh","            "py","            "keystore","            "reg","            "yml","            "yaml","        ]

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def get_ci_cd_attack_patterns(self) -> Dict[str, Any]:"Returns common entry points and misconfigurations for CI/CD systems.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""#  "       return {"  # [BATCHFIX] closed string"            "jenkins": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                 "paths": ["/script", "/asynchPeople/", "/manage"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                 "secrets": ["credentials.xml", "config.xml"],"            },
            "teamcity": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                 "paths": ["/httpAuth/app/rest/users", "/httpAuth/app/rest/projects"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                 "secrets": ["database.properties"],"            },
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             "gh_actions": {"keywords": ["ACTIONS_RUNTIME_TOKEN", "GITHUB_TOKEN"]},"        }

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def get_github_runner_attack_vectors(self) -> List[Dict[str, Any]]:"Attack vectors for GitHub Action Self-Hosted Runners (Ported from Gato-X).        return [
            {
                "name": "Runner Registration Token Leak","                "description": "Leakage of runner registration tokens in logs or code.","                "severity": "CRITICAL","            },
            {
                "name": "Workflow Command Injection","                "description": "Injection into github.event.issue.title or search results used in run: steps.","                "severity": "HIGH","            },
            {
                "name": "Non-Ephemeral Runner Persistence","                "description": "Exploiting long-lived runners for lateral movement in the internal network.","                "severity": "MEDIUM","            },
            {
                "name": "Actions PATH Hijacking","                "description": "Modifying GITHUB_PATH to achieve persistence or privilege escalation on the runner.","                "severity": "HIGH","            },
        ]

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     async def scan_sccm_dp(self, target: str) -> Dict[str, Any]:""""# [BATCHFIX] Commented metadata/non-Python
"""         "Lightweight check for SCCM DP exposure."  # [BATCHFIX] closed string"        session = await self.get_session()
#         base_url = fhttp://{target}
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         results: Dict[str, Any] = {"exposed_paths": []}"
        for entry in self.get_sccm_looting_paths(base_url):
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""             url = base_url + entry["path"]"            try:
                async with session.get(url, timeout=5) as resp:
                    if resp.status == 200:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                         results["exposed_paths"].append(url)"            except Exception:
                continue
        return results
