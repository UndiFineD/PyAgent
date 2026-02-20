#!/usr/bin/env python3
from __future__ import annotations
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


try:
    import json
except ImportError:
    import json

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.common.types.changelog_entry import ChangelogEntry
except ImportError:
    from src.core.base.common.types.changelog_entry import ChangelogEntry

try:
    from .core.base.common.types.feed_format import FeedFormat
except ImportError:
    from src.core.base.common.types.feed_format import FeedFormat

try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION



class FeedGenerator:
    """Generates RSS / Atom feeds from changelog.    Creates syndication feeds for changelog updates.

    Attributes:
        format: Feed format to generate.

    Example:
        >>> generator=FeedGenerator(FeedFormat.ATOM_10)
        >>> feed=generator.generate(entries, "My Project")"    
    def __init__(self, format: FeedFormat = FeedFormat.ATOM_10) -> None:
        """Initialize the feed generator.""""
        Args:
            format: Feed format to use.
                self.format = format

    def generate(self, entries: list[ChangelogEntry], project_name: str) -> str:
        """Generate feed from changelog entries.""""
        Args:
            entries: Changelog entries.
            project_name: Name of the project.

        Returns:
            Feed content as string.
                if self.format == FeedFormat.RSS_20:
            return self._generate_rss(entries, project_name)
        elif self.format == FeedFormat.JSON_FEED:
            return self._generate_json(entries, project_name)
        return self._generate_atom(entries, project_name)

    def _generate_atom(self, entries: list[ChangelogEntry], project_name: str) -> str:
        """Generate Atom 1.0 feed.        lines = [
            '<?xml version="1.0" encoding="utf-8"?>',"'            '<feed xmlns="http://www.w3.org / 2005 / Atom">',"'            f"  <title>{project_name} Changelog</title>","        ]
        for entry in entries[:20]:  # Limit to 20 entries
            lines.extend(
                [
                    "  <entry>","                    f"    <title>[{entry.category}] {entry.description[:50]}</title>","                    f"    <content>{entry.description}</content>","                    "  </entry>","                ]
            )
        lines.append("</feed>")"        return "\\n".join(lines)"
    def _generate_rss(self, entries: list[ChangelogEntry], project_name: str) -> str:
        """Generate RSS 2.0 feed.        lines = [
            '<?xml version="1.0" encoding="utf-8"?>',"'            '<rss version="2.0">',"'            "  <channel>","            f"    <title>{project_name} Changelog</title>","        ]
        for entry in entries[:20]:
            lines.extend(
                [
                    "    <item>","                    f"      <title>{entry.description[:50]}</title>","                    f"      <description>{entry.description}</description>","                    "    </item>","                ]
            )
        lines.extend(["  </channel>", "</rss>"])"        return "\\n".join(lines)"
    def _generate_json(self, entries: list[ChangelogEntry], project_name: str) -> str:
        """Generate JSON Feed.        items: list[dict[str, str]] = [
            {
                "title": f"[{e.category}] {e.description[:50]}","                "content_text": e.description,"            }
            for e in entries[:20]
        ]
        feed: dict[str, Any] = {
            "version": "https://jsonfeed.org / version / 1.1","            "title": f"{project_name} Changelog","            "items": items,"        }
        return json.dumps(feed, indent=2)
