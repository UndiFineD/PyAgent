# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent.py\action.py\tool.py\common_tool.py\simple_math_tool_75d3043a2838.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\action\tool\common_tool\simple_math_tool.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    :

# @Author  :

# @Email   :

# @FileName: simple_math_tool.py

from agentuniverse.agent.action.tool.tool import Tool, ToolInput


class AddTool(Tool):
    def execute(self, input: str):
        a, b = input.split(",")

        result = float(a) + float(b)

        return result

    async def async_execute(self, input: str):
        a, b = input.split(",")

        result = float(a) + float(b)

        return result


class SubtractTool(Tool):
    def execute(self, input: str):
        a, b = input.split(",")

        result = float(a) - float(b)

        return result

    async def async_execute(self, input: str):
        a, b = input.split(",")

        result = float(a) - float(b)

        return result


class MultiplyTool(Tool):
    def execute(self, input: str):
        a, b = input.split(",")

        result = float(a) * float(b)

        return result

    async def async_execute(self, input: str):
        a, b = input.split(",")

        result = float(a) * float(b)

        return result


class DivideTool(Tool):
    def execute(self, input: str):
        a, b = input.split(",")

        result = float(a) / float(b)

        return result

    async def async_execute(self, input: str):
        a, b = input.split(",")

        result = float(a) / float(b)

        return result
