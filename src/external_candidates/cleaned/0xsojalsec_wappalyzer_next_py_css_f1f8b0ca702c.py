# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_wappalyzer_next.py\wappalyzer.py\parsers.py\css_f1f8b0ca702c.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-wappalyzer-next\wappalyzer\parsers\css.py


def get_css(soup):

    css = []

    for link in soup.find_all("style"):
        css.append(link.text)

    return css
