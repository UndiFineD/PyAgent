# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent.py\action.py\tool.py\common_tool.py\wikipedia_query_dc8b6c5d26a7.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\action\tool\common_tool\wikipedia_query.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    :

# @Author  :

# @Email   :

# @FileName: wikipedia_query.py

from agentuniverse.agent.action.tool.common_tool.langchain_tool import LangChainTool

from langchain_community.tools import WikipediaQueryRun

from langchain_community.utilities import WikipediaAPIWrapper


class WikipediaTool(LangChainTool):
    def init_langchain_tool(self, component_configer):
        wrapper = WikipediaAPIWrapper()

        return WikipediaQueryRun(api_wrapper=wrapper)
