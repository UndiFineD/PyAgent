# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_wappalyzer_next.py\wappalyzer.py\parsers.py\robots_9e2c1b8fd78d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-wappalyzer-next\wappalyzer\parsers\robots.py

from urllib.parse import urlparse

from wappalyzer.core.requester import get_response


def get_robots(url):

    scheme = urlparse(url).scheme

    hostname = urlparse(url).hostname

    robots_url = f"{scheme}://{hostname}/robots.txt"

    r = get_response(robots_url)

    return r.text if r else ""
