# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_web_navigator.py\src.py\agent.py\web.py\state_56796cac2051.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Web-Navigator\src\agent\web\state.py

from operator import add

from typing import Annotated, TypedDict

from src.agent.web.context import BrowserState

from src.agent.web.dom.views import DOMState

from src.message import BaseMessage


class AgentState(TypedDict):
    input: str

    output: str

    agent_data: dict

    prev_observation: str

    browser_state: BrowserState | None

    dom_state: DOMState | None

    messages: Annotated[list[BaseMessage], add]
