# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent.py\template.py\default_summarize_agent_template_47527f4cd088.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\template\default_summarize_agent_template.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    : 2024/10/24 21:19

# @Author  : wangchongshi

# @Email   : wangchongshi.wcs@antgroup.com

# @FileName: default_summarize_agent_template.py

from agentuniverse.agent.input_object import InputObject

from agentuniverse.agent.template.rag_agent_template import RagAgentTemplate


class SummarizeRagAgentTemplate(RagAgentTemplate):
    def input_keys(self) -> list[str]:
        return ["input", "summarize_content"]

    def output_keys(self) -> list[str]:
        return ["output"]

    def parse_input(self, input_object: InputObject, agent_input: dict) -> dict:
        agent_input["input"] = input_object.get_data("input")

        agent_input["summarize_content"] = input_object.get_data("summarize_content")

        return agent_input

    def parse_result(self, agent_result: dict) -> dict:
        return {**agent_result, "output": agent_result["output"]}
