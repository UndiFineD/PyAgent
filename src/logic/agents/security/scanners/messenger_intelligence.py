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

from typing import Dict, Any


class MessengerIntelligence:
    """
    Handles discovery and OSINT for messenger platforms (Telegram, Discord, etc.).
    Ported logic from various Telegram OSINT tools.
    """

    TELEGRAM_URL_PATTERN = r"https?://t\.me/([a-zA-Z0-9_]{5,})"
    TELEGRAM_BOT_TOKEN_PATTERN = r"\d{7,10}:[a-zA-Z0-9_-]{35}"

    def get_telegram_recon_endpoints(self, username: str) -> Dict[str, str]:
        """Returns public Telegram endpoints for OSINT."""
        return {
            "profile": f"https://t.me/{username}",
            "api_info": "https://api.telegram.org/bot<token>/getMe",
            "proxy_list": "https://t.me/s/ProxyMTProto",
        }

    def get_discord_patterns(self) -> Dict[str, str]:
        """Returns patterns for Discord OSINT."""
        return {
            "invite": r"https?://discord\.gg/[a-zA-Z0-9]+",
            "webhook": r"https://discord\.com/api/webhooks/\d+/[a-zA-Z0-9_-]+",
            "token": r"[a-zA-Z0-9_-]{24}\.[a-zA-Z0-9_-]{6}\.[a-zA-Z0-9_-]{27}",
        }

    def get_telegram_nearby_params(self) -> Dict[str, Any]:
        """Parameters for Telegram 'People Nearby' exploitation (trilateration)."""
        return {
            "method": "messages.getNearbyUsers",
            "required_fields": ["lat", "long"],
            "description": (
                "Used to find users within a specific radius. Can be used for trilateration by spoofing 3 locations."
            ),
        }

    def audit_bot_token(self, token: str) -> str:
        """Generates a command to verify a Telegram bot token."""
        return f"curl -s https://api.telegram.org/bot{token}/getMe"
