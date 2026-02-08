# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_praisonai.py\src.py\praisonai.py\tests.py\tools.py\internet_search_ab9311b5f75a.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai\tests\tools\internet_search.py

from duckduckgo_search import DDGS

from langchain.tools import tool


@tool("Internet Search Tool")
def internet_search_tool(query: str) -> list:
    """Search Internet for relevant information based on a query."""

    ddgs = DDGS()

    results = ddgs.text(keywords=query, region="wt-wt", safesearch="moderate", max_results=5)

    return results
