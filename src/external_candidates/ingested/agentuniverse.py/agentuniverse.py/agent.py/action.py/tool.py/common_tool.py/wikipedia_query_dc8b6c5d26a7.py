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
