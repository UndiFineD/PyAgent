# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\cache.py\work.py\copilot_tmp.py\chunk_0_meta_e3e91ed74457.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\cache\work\copilot_tmp\chunk_0_meta.py

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-wappalyzer-next\wappalyzer\parsers\meta.py

# NOTE: extracted with static-only rules; review before use


def get_meta(soup):
    meta = {}

    for tag in soup.find_all("meta"):
        key = tag.get("name") or tag.get("property")

        value = tag.get("content")

        if key and value:
            if key in meta:
                if isinstance(meta[key], list):
                    meta[key].append(value)

                else:
                    meta[key] = [meta[key], value]

            else:
                meta[key] = value

    return meta
