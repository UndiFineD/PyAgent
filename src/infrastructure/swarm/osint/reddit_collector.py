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
import os
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class RedditCollector:
    """
    Reddit OSINT collector.
    Async implementation refactored from auto-news RedditAgent.
    """

    AUTH_URL = 'https://www.reddit.com/api/v1/access_token'
    SUBREDDIT_NEW_URL = "https://oauth.reddit.com/r/{}/new"

    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        self.client_id = client_id or os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = os.getenv("REDDIT_USER_AGENT", "PyAgent:v1.0.0 (by /u/unknown)")
        self._token = None
        self._token_expires = 0

    async def _get_token(self) -> Optional[str]:
        """Obtain OAuth2 token from Reddit."""
        if self._token and datetime.now().timestamp() < self._token_expires:
            return self._token

        if not self.client_id or not self.client_secret:
            logger.error("Reddit API credentials missing (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)")
            return None

        async with aiohttp.ClientSession() as session:
            auth = aiohttp.BasicAuth(self.client_id, self.client_secret)
            data = {'grant_type': 'client_credentials'}
            headers = {'User-Agent': self.user_agent}

            try:
                async with session.post(self.AUTH_URL, data=data, headers=headers, auth=auth) as resp:
                    if resp.status == 200:
                        res_json = await resp.json()
                        self._token = res_json['access_token']
                        # Set expiration buffer of 60 seconds
                        self._token_expires = datetime.now().timestamp() + res_json.get('expires_in', 3600) - 60
                        return self._token
                    else:
                        logger.error(f"Failed to authenticate with Reddit: {resp.status}")
                        return None
            except Exception as e:
                logger.error(f"Reddit Auth Error: {e}")
                return None

    async def fetch_subreddit(self, subreddit: str, limit: int = 10) -> List[Dict]:
        """Fetch 'new' posts from a subreddit."""
        token = await self._get_token()
        if not token:
            return []

        url = self.SUBREDDIT_NEW_URL.format(subreddit)
        headers = {
            'Authorization': f'Bearer {token}',
            'User-Agent': self.user_agent
        }
        params = {'limit': limit}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        posts = []
                        for child in data.get('data', {}).get('children', []):
                            entry = child.get('data', {})
                            posts.append({
                                "id": entry.get("id"),
                                "title": entry.get("title"),
                                "author": entry.get("author"),
                                "permalink": f"https://reddit.com{entry.get('permalink')}",
                                "content": entry.get("selftext", ""),
                                "url": entry.get("url"),
                                "created_utc": datetime.fromtimestamp(entry.get("created_utc", 0)).isoformat(),
                                "subreddit": subreddit
                            })
                        return posts
                    else:
                        logger.error(f"Failed to fetch subreddit {subreddit}: {resp.status}")
                        return []
            except Exception as e:
                logger.error(f"Reddit Fetch Error: {e}")
                return []
