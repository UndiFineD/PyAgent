# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentkit.py\backend.py\app.py\app.py\deps.py\agent_deps_f195bd795dd9.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentkit\backend\app\app\deps\agent_deps.py

# -*- coding: utf-8 -*-

from typing import Optional

from app.api.deps import get_redis_client

from app.services.chat_agent.meta_agent import create_meta_agent

from app.utils.config_loader import get_agent_config

from app.utils.fastapi_globals import g

from app.utils.uuid7 import uuid7

from langchain.agents import AgentExecutor


async def set_global_tool_context() -> None:
    run_id = str(uuid7())

    g.tool_context = {}

    g.query_context = {
        "run_id": run_id,
    }

    redis_client = await get_redis_client()

    await redis_client.set(run_id, "True")


def get_meta_agent(
    api_key: Optional[str] = None,
) -> AgentExecutor:
    agent_config = get_agent_config()

    agent_config.api_key = api_key

    return create_meta_agent(agent_config)
