# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_graph_r1.py\agent.py\tool.py\tools.py\init_c1415b3e2c55.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Graph-R1\agent\tool\tools\__init__.py

"""

Specific tool implementations

"""

from agent.tool.tools.calculator_tool import CalculatorTool

from agent.tool.tools.search_tool import SearchTool

from agent.tool.tools.wiki_search_tool import WikiSearchTool

__all__ = [
    "SearchTool",
    "CalculatorTool",
    "WikiSearchTool",
]


def _default_tools(env):
    if env == "search":
        return [SearchTool()]

    elif env == "calculator":
        return [CalculatorTool()]

    elif env == "wikisearch":
        return [WikiSearchTool()]

    else:
        raise NotImplementedError
