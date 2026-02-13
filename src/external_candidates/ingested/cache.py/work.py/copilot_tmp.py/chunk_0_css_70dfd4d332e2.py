# Extracted from: C:\DEV\PyAgent\.external\cache\work\copilot_tmp\chunk_0_css.py
# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-wappalyzer-next\wappalyzer\parsers\css.py
# NOTE: extracted with static-only rules; review before use


def get_css(soup):

    css = []

    for link in soup.find_all("style"):

        css.append(link.text)

    return css
