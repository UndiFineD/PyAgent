# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent.py\action.py\tool.py\common_tool.py\command_status_tool_4c2ae14b44ad.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\action\tool\common_tool\command_status_tool.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    : 2025/3/22 18:00

# @Author  : hiro

# @Email   : hiromesh@qq.com

# @FileName: command_status_tool.py

import json

from agentuniverse.agent.action.tool.common_tool.run_command_tool import (
    get_command_result,
)

from agentuniverse.agent.action.tool.tool import Tool, ToolInput


class CommandStatusTool(Tool):
    def execute(self, thread_id: int) -> str:
        if isinstance(thread_id, str) and thread_id.isdigit():
            thread_id = int(thread_id)

        result = get_command_result(thread_id)

        if result is None:
            return json.dumps(
                {
                    "error": f"No command found with thread_id: {thread_id}",
                    "status": "not_found",
                }
            )

        return result.message
