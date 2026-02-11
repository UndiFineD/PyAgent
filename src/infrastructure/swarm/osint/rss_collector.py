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
import feedparser
import logging
from typing import List, Dict
from datetime import datetime
from time import mktime

logger = logging.getLogger(__name__)

class RssCollector:
    """
    RSS feed collector for OSINT agents.
    Refactored from auto-news ops_rss.
    """

    @classmethod
    async def fetch_feed(cls, feed_url: str, limit: int = 10) -> List[Dict]:
        """
        Fetch entries from an RSS/Atom feed asynchronously.
        """
        # feedparser is synchronous, wrap in executor if needed for many feeds
        loop = asyncio.get_event_loop()
        try:
            feed = await loop.run_in_executor(None, feedparser.parse, feed_url)
        except Exception as e:
            logger.error(f"Failed to parse feed {feed_url}: {e}")
            return []

        if feed.get("bozo", 0):
            logger.warning(f"Feed parser reported non-critical error (bozo) for {feed_url}")

        entries = []
        for entry in feed.entries[:limit]:
            published_dt = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published_dt = datetime.fromtimestamp(mktime(entry.published_parsed))
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                published_dt = datetime.fromtimestamp(mktime(entry.updated_parsed))

            entries.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", ""),
                "published": published_dt.isoformat() if published_dt else None,
                "author": entry.get("author", "Unknown"),
                "source_feed": feed_url
            })

        return entries

    @classmethod
    async def fetch_multiple(cls, feed_urls: List[str], limit_per_feed: int = 5) -> List[Dict]:
        """
        Parallel fetch multiple feeds.
        """
        tasks = [cls.fetch_feed(url, limit_per_feed) for url in feed_urls]
        results = await asyncio.gather(*tasks)
        # Flatten results
        return [entry for sublist in results for entry in sublist]
