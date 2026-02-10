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
import xml.etree.ElementTree as ET
from typing import Dict, Optional
from urllib.parse import quote


class MFAIntelligence:
    """
    Intelligence module for MFA detection and identity service profiling.
    Ported from MFASweep and other O365/Azure tools.
    """

    O365_ENDPOINTS = {
        "GraphAPI": "https://graph.microsoft.com",
        "AzureManagement": "https://management.core.windows.net",
        "ExchangeServices": "https://outlook.office365.com/EWS/Exchange.asmx",
        "ActiveSync": "https://outlook.office365.com/Microsoft-Server-ActiveSync",
        "WebPortal": "https://portal.office.com"
    }

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self.session = session
        self._own_session = False

    async def get_session(self) -> aiohttp.ClientSession:
        if not self.session:
            self.session = aiohttp.ClientSession()
            self._own_session = True
        return self.session

    async def get_user_realm(self, username: str) -> Dict:
        """Checks the authentication realm for a user (ADFS vs Managed)."""
        url = f"https://login.microsoftonline.com/getuserrealm.srf?login={quote(username)}&xml=1"
        try:
            session = await self.get_session()
            async with session.get(url) as response:
                content = await response.text()
                root = ET.fromstring(content)
                name_space = {'ns': 'http://schemas.microsoft.com/identity/userrealm/1.0'}

                state_node = root.find('.//ns:State', name_space)
                auth_url_node = root.find('.//ns:AuthURL', name_space)
                fed_proto_node = root.find('.//ns:FederationProtocol', name_space)

                realm = {
                    "username": username,
                    "state": state_node.text if state_node is not None else "Unknown",
                    "auth_url": auth_url_node.text if auth_url_node is not None else None,
                    "federation_protocol": fed_proto_node.text if fed_proto_node is not None else None
                }
                return realm
        except Exception as e:
            return {"username": username, "error": str(e)}

    async def check_mfa_status(self, username: str, password: str) -> Dict:
        """
        Attempts basic authentication to multiple O365 endpoints to detect MFA.
        WARNING: May trigger lockouts.
        """
        results = {}
        session = await self.get_session()

        async def check_endpoint(name, url):
            # This is a simplified check. Real MFASweep does more complex header handling.
            auth = aiohttp.BasicAuth(username, password)
            try:
                async with session.get(url, auth=auth, timeout=10) as response:
                    # Logic: 401 with specific headers often indicates MFA requirement
                    # whereas 200/302 might mean successful login (MFA bypassed or not enabled)
                    results[name] = {
                        "status_code": response.status,
                        "mfa_indicator": "WAuth=wsignin1.0" in response.headers.get("WWW-Authenticate", "")
                    }
            except Exception as e:
                results[name] = {"error": str(e)}

        await asyncio.gather(*(check_endpoint(n, u) for n, u in self.O365_ENDPOINTS.items()))
        return results
