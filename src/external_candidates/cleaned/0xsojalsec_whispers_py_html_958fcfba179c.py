# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_whispers.py\whispers.py\plugins.py\html_958fcfba179c.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-whispers\whispers\plugins\html.py

from pathlib import Path

from bs4 import BeautifulSoup, Comment

from bs4.element import PageElement

from whispers.utils import truncate_all_space


class Html:
    def pairs(self, filepath: Path):
        soup = BeautifulSoup(filepath.read_text(), "lxml")

        for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
            yield from self.parse_comments(comment)

    def parse_comments(self, comment: PageElement):
        comment = truncate_all_space(comment.extract()).strip()

        if comment:
            yield "comment", comment
