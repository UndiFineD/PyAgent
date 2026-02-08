# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\evoagentx.py\evoagentx.py\hitl.py\hitl_c30b4eaba0ec.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\EvoAgentX\evoagentx\hitl\hitl.py

import uuid

from enum import Enum

from typing import Any, Dict, Optional


from pydantic import BaseModel, Field


class HITLDecision(str, Enum):
    APPROVE = "approve"

    REJECT = "reject"

    MODIFY = "modify"

    CONTINUE = "continue"


class HITLInteractionType(str, Enum):
    APPROVE_REJECT = "approve_reject"

    COLLECT_USER_INPUT = "collect_user_input"

    REVIEW_EDIT_STATE = "review_edit_state"

    REVIEW_TOOL_CALLS = "review_tool_calls"

    MULTI_TURN_CONVERSATION = "multi_turn_conversation"


class HITLMode(str, Enum):
    PRE_EXECUTION = "pre_execution"  # pre-execution intercept

    POST_EXECUTION = "post_execution"  # post-execution intercept


class HITLContext(BaseModel):
    """HITL context information - simplified version"""

    task_name: str

    agent_name: str

    action_name: str

    workflow_goal: Optional[str] = None

    # execution data

    action_inputs: Dict[str, Any] = Field(default_factory=dict)

    execution_result: Optional[Any] = None

    # display context

    display_context: Dict[str, Any] = Field(default_factory=dict)


class HITLRequest(BaseModel):
    """HITL Request"""

    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    interaction_type: HITLInteractionType

    mode: HITLMode

    context: HITLContext

    prompt_message: str


class HITLResponse(BaseModel):
    """HITL Response"""

    request_id: str

    decision: HITLDecision

    modified_content: Optional[Any] = None

    feedback: Optional[str] = None
