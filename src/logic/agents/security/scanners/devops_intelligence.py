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

import aiohttp
from typing import List, Dict, Any, Optional


class DevOpsIntelligence:
    """
    Handles discovery and exploitation of DevOps & Management infrastructure.
    Integrates logic from SCMKit, sccm-http-looter, and CI/CD attack tools.
    """

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None

    async def get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(headers={"User-Agent": "PyAgent DevOpsAudit/1.0"})
        return self.session

    def get_scm_recon_endpoints(self, base_url: str, provider: str = "github") -> List[str]:
        """Returns API endpoints for repository and user recon."""
        if provider == "github":
            return [
                f"{base_url}/api/v3/users",
                f"{base_url}/api/v3/repositories",
                f"{base_url}/api/v3/search/code?q=filename:.env",
                f"{base_url}/api/v3/search/code?q=filename:id_rsa",
            ]
        elif provider == "gitlab":
            return [f"{base_url}/api/v4/projects", f"{base_url}/api/v4/users", f"{base_url}/api/v4/groups"]
        return []

    def get_sccm_looting_paths(self, base_url: str) -> List[Dict[str, str]]:
        """Returns interesting SCCM/MECM distribution point paths."""
        return [
            {"path": "/SMS_DP_SMSPKG$/", "desc": "Package storage (often allows directory listing)"},
            {"path": "/SMS_DP_DATALIB/", "desc": "Data library metadata"},
            {"path": "/SMS_DP_SMSSIG$/", "desc": "Signature files for package verification"},
        ]

    def get_sccm_sensitive_extensions(self) -> List[str]:
        """Returns extensions frequently containing secrets in SCCM packages."""
        return [
            "ps1",
            "vbs",
            "txt",
            "cmd",
            "bat",
            "pfx",
            "pem",
            "cer",
            "sql",
            "xml",
            "config",
            "ini",
            "sh",
            "py",
            "keystore",
            "reg",
            "yml",
            "yaml",
        ]

    def get_ci_cd_attack_patterns(self) -> Dict[str, Any]:
        """Returns common entry points and misconfigurations for CI/CD systems."""
        return {
            "jenkins": {
                "paths": ["/script", "/asynchPeople/", "/manage"],
                "secrets": ["credentials.xml", "config.xml"],
            },
            "teamcity": {
                "paths": ["/httpAuth/app/rest/users", "/httpAuth/app/rest/projects"],
                "secrets": ["database.properties"],
            },
            "gh_actions": {"keywords": ["ACTIONS_RUNTIME_TOKEN", "GITHUB_TOKEN"]},
        }

    def get_github_runner_attack_vectors(self) -> List[Dict[str, Any]]:
        """Attack vectors for GitHub Action Self-Hosted Runners (Ported from Gato-X)."""
        return [
            {
                "name": "Runner Registration Token Leak",
                "description": "Leakage of runner registration tokens in logs or code.",
                "severity": "CRITICAL",
            },
            {
                "name": "Workflow Command Injection",
                "description": "Injection into github.event.issue.title or search results used in run: steps.",
                "severity": "HIGH",
            },
            {
                "name": "Non-Ephemeral Runner Persistence",
                "description": "Exploiting long-lived runners for lateral movement in the internal network.",
                "severity": "MEDIUM",
            },
            {
                "name": "Actions PATH Hijacking",
                "description": "Modifying GITHUB_PATH to achieve persistence or privilege escalation on the runner.",
                "severity": "HIGH",
            },
        ]

    async def scan_sccm_dp(self, target: str) -> Dict[str, Any]:
        """Lightweight check for SCCM DP exposure."""
        session = await self.get_session()
        base_url = f"http://{target}"
        results: Dict[str, Any] = {"exposed_paths": []}

        for entry in self.get_sccm_looting_paths(base_url):
            url = base_url + entry["path"]
            try:
                async with session.get(url, timeout=5) as resp:
                    if resp.status == 200:
                        results["exposed_paths"].append(url)
            except Exception:
                continue
        return results
