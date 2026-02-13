#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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
import random
import string
import re
import logging
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


class EmailIntelligence:
    """Intelligence engine for handling ephemeral/temporary emails and OTP extraction."""

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self.session = session
        self.api_url = "https://www.1secmail.com/api/v1/"

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def generate_random_email(self) -> str:
        """Generates a random ephemeral email address."""
        session = await self._get_session()
        async with session.get(f"{self.api_url}?action=genEmailAddresses&count=1") as resp:
            if resp.status == 200:
                emails = await resp.json()
                return emails[0]
        # Fallback
        user = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"{user}@1secmail.com"

    async def check_inbox(self, email: str) -> List[Dict[str, Any]]:
        """Checks the inbox for the given email address."""
        user, domain = email.split("@")
        url = f"{self.api_url}?action=getMessages&login={user}&domain={domain}"
        session = await self._get_session()
        try:
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    return await resp.json()
        except Exception as e:
            logger.error(f"Error checking inbox for {email}: {e}")
        return []

    async def get_message_content(self, email: str, msg_id: int) -> Dict[str, Any]:
        """Fetches the content of a specific message."""
        user, domain = email.split("@")
        url = f"{self.api_url}?action=readMessage&login={user}&domain={domain}&id={msg_id}"
        session = await self._get_session()
        try:
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    return await resp.json()
        except Exception as e:
            logger.error(f"Error reading message {msg_id} for {email}: {e}")
        return {}

    def extract_otp(self, text: str) -> Optional[str]:
        """Extracts OTPS (4-8 digits) from text."""
        match = re.search(r"\b\d{4,8}\b", text)
        return match.group(0) if match else None

    def extract_links(self, text: str) -> List[str]:
        """Extracts confirmation/activation links from text."""
        return re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", text)

    async def wait_for_otp(self, email: str, timeout: int = 120, interval: int = 5) -> Optional[str]:
        """Polls the inbox until an OTP is found or timeout is reached."""
        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < timeout:
            messages = await self.check_inbox(email)
            for msg in messages:
                content = await self.get_message_content(email, msg["id"])
                body = content.get("textBody", "") + content.get("body", "")
                otp = self.extract_otp(body)
                if otp:
                    return otp
            await asyncio.sleep(interval)
        return None

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
