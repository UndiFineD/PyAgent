# Extracted from: C:\DEV\PyAgent\.external\skills\skills\guoqiao\hn-extract\hn-extract.py
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.32.5",
#     "trafilatura>=2.0.0",
#     "urllib3>=2.6.3",
# ]
# ///

import argparse
import html
import json
import re
import textwrap
from pathlib import Path

import requests
from trafilatura import extract, fetch_url
from urllib3 import Retry


def get_request_session(retry_total=3):
    """Get a request session with automatic retry."""
    retries = Retry(total=retry_total)
    adapter = requests.adapters.HTTPAdapter(max_retries=retries)
    session = requests.Session()
    session.mount("https://", adapter)
    return session


request_session = get_request_session(retry_total=3)


def get_json_from_url(url: str) -> dict:
    """Get JSON from a URL with automatic retry."""
    response = request_session.get(url)
    response.raise_for_status()
    return response.json()


def clean_html_text(text):
    """Clean HTML text by replacing <p> tags with newlines and removing all remaining HTML tags."""

    # 1. Replace <p> tags with newlines to preserve paragraph structure
    # This ensures "end.<p>Start" becomes "end.\nStart" instead of "end.Start"
    text = re.sub(r"<p\s*/?>", "\n", text, flags=re.IGNORECASE)

    # 2. Remove all remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # 3. Decode HTML entities (e.g. &quot; -> ", &#x27; -> ')
    # We do this last so that decoded characters like < or > aren't mistaken for tags
    text = html.unescape(text)

    return text.strip()


class HackerNewsExtractor:
    """Extractor article and comments from a HackerNews Post."""

    def __init__(self, data: dict):
        self.data = data
        self.lines = []
        self.indent_char = " " * 4
        self.indent_level = 0
        self.split_line = "\n" + "-" * 80

    @classmethod
    def from_json_file(cls, path) -> "HackerNewsExtractor":
        assert path.is_file(), f"json file not found: {path}"
        assert path.suffix == ".json", f"input file must be json: {path}"
        json_str = path.read_text()
        data = json.loads(json_str)
        return cls(data)

    @classmethod
    def from_id(cls, id: str) -> "HackerNewsExtractor":
        id_pattern = r"\b(\d{1,10})\b"
        match = re.match(id_pattern, id)
        if match:
            url = f"https://hn.algolia.com/api/v1/items/{id}"
            data = get_json_from_url(url)
            return cls(data)

    @classmethod
    def from_url(cls, url: str) -> "HackerNewsExtractor":
        url = url.lower().strip()
        url_pattern = r"https://news.ycombinator.com/item\?id=(\d{1,10})"
        match = re.match(url_pattern, url)
        if match:
            return cls.from_id(match.group(1))

    @classmethod
    def from_uri(cls, uri: str) -> "HackerNewsExtractor":
        # uri can be id/url/file

        if uri.isdigit() or isinstance(uri, int):
            return cls.from_id(uri)

        path = Path(uri)
        if path.is_file():
            return cls.from_json_file(path)

        return cls.from_url(uri)

    def add_line(self, line: str, indent_level: int = 0, sep="\n"):
        if line.strip():
            indent = self.indent_char * indent_level
            indent_line = textwrap.indent(
                textwrap.fill(line, width=80),
                indent,
            )
            self.lines.append(indent_line + sep)

    def extract_url(self, url: str) -> str:
        """Extract text from URL."""
        html = fetch_url(url, no_ssl=True)
        text = extract(html, output_format="txt", fast=True)
        return (text or "").strip()

    def extract(self) -> str:
        """Extract text from the origin."""
        assert self.data, "data must be populated before extract"

        id = self.data.get("id", "")
        hn_url = f"https://news.ycombinator.com/item?id={id}"
        title = self.data.get("title", "")
        author = self.data.get("author", "")
        created_at = self.data.get("created_at", "")
        points = self.data.get("points", "")
        # story_id = int(self.data.get("story_id", 0))
        article_url = self.data.get("url", "")
        article_text = self.extract_url(article_url)

        self.add_line(f"# {title}")
        self.add_line(f"by @{author}, at {created_at}, {points} points")
        self.add_line(f"Origin: {article_url}")
        self.add_line(f"HackerNews: {hn_url}")

        self.add_line(article_text)

        self.add_line(self.split_line)
        self.add_line("# HackerNews Comments")
        for child in self.data.get("children", []):
            # direct child indent at level 0
            self.extract_comment(child, indent_level=0)

        return "\n".join(self.lines)

    def extract_comment(self, comment: dict, indent_level: int = 0):
        author = comment.get("author", "")
        text = comment.get("text", "")
        text = clean_html_text(text)
        self.add_line(f"{author}: {text}", indent_level=indent_level)
        # child comment indent 1 more level
        child_indent_level = indent_level + 1
        for child in comment.get("children", []):
            self.extract_comment(child, indent_level=child_indent_level)


def main():
    parser = argparse.ArgumentParser(description="HackerNews Extractor")
    parser.add_argument("uri", type=str, help="HackerNews id, url, or json file path")
    parser.add_argument("-o", "--output", help="output file path, default to stdout")
    args = parser.parse_args()
    extractor = HackerNewsExtractor.from_uri(args.uri)
    if not extractor:
        raise ValueError(f"Invalid HN uri, please provide a valid id, url, or json file path: {args.uri}")

    content = extractor.extract()

    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(f"output: {path}")
    else:
        print(content)


if __name__ == "__main__":
    main()
