# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\examples\sample_apps\basic_sop_app\intelligence\test\recommend_sop_agent_test.py
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time    : 2024/11/28 17:17
# @Author  : jijiawei
# @Email   : jijiawei.jjw@antgroup.com
# @FileName: recommend_sop_agent_test.py
from agentuniverse.agent.agent import Agent
from agentuniverse.agent.agent_manager import AgentManager
from agentuniverse.base.agentuniverse import AgentUniverse

AgentUniverse().start(config_path="../../config/config.toml", core_mode=True)


def chat(question: str):
    instance: Agent = AgentManager().get_instance_obj("recommend_sop_agent")
    return instance.run(input=question)


if __name__ == "__main__":
    print(chat("为我想要买医疗类保险").get_data("output"))
