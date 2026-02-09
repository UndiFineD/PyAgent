# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-wappalyzer-next\wappalyzer\parsers\css.py
def get_css(soup):
    css = []
    for link in soup.find_all("style"):
        css.append(link.text)
    return css
