# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-whispers\whispers\plugins\uri.py
from urllib.parse import parse_qsl, urlparse


class Uri:
    def pairs(self, code: str):
        uri = urlparse(code)
        if uri.password:
            yield "URI_Password", uri.password
        if uri.query:
            for key, value in parse_qsl(uri.query):
                yield key, value
