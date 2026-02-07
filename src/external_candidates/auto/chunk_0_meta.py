# Refactored by Copilot placeholder
# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-wappalyzer-next\wappalyzer\parsers\meta.py
# NOTE: extracted with static-only rules; review before use

def get_meta(soup):

    meta = {}

    for tag in soup.find_all('meta'):

        key = tag.get('name') or tag.get('property')

        value = tag.get('content')

        if key and value:

            if key in meta:

                if isinstance(meta[key], list):

                    meta[key].append(value)

                else:

                    meta[key] = [meta[key], value]

            else:

                meta[key] = value

    return meta

