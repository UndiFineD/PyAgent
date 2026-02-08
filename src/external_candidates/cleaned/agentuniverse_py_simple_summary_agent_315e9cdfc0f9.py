# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentuniverse.py\agentuniverse.py\agent.py\default.py\summary_agent.py\simple_summary_agent_315e9cdfc0f9.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\default\summary_agent\simple_summary_agent.py

# !/usr/bin/env python3

# -*- coding:utf-8 -*-

# @Time    : 2024/8/29 11:13

# @Author  : fanen.lhy

# @Email   : fanen.lhy@antgroup.com

# @FileName: simple_summary_agent.py

from agentuniverse.agent.agent import Agent

from agentuniverse.agent.input_object import InputObject


class SimpleSummaryAgent(Agent):
    """ReAct Agent class."""

    def input_keys(self) -> list[str]:
        """Return the input keys of the Agent."""

        return ["input"]

    def output_keys(self) -> list[str]:
        """Return the output keys of the Agent."""

        return ["output"]

    def parse_input(self, input_object: InputObject, agent_input: dict) -> dict:
        """Agent parameter parsing.

        Args:

            input_object (InputObject): input parameters passed by the user.

            agent_input (dict): agent input preparsed by the agent.

        Returns:

            dict: agent input parsed from `input_object` by the user.

        """

        agent_input["input"] = input_object.get_data("input")

        self.agent_model.profile.setdefault("prompt_version", "simple_summary_agent.cn")

        return agent_input

    def parse_result(self, planner_result: dict) -> dict:
        """Planner result parser.

        Args:

            planner_result(dict): Planner result

        Returns:

            dict: Agent result object.

        """

        return planner_result
