# Extracted from: C:\DEV\PyAgent\.external\EvoAgentX\evoagentx\hitl\__init__.py
from .approval_manager import (
    HITLManager,
)
from .hitl import (
    HITLContext,
    HITLDecision,
    HITLInteractionType,
    HITLMode,
    HITLRequest,
    HITLResponse,
)
from .interceptor_agent import (
    HITLBaseAgent,
    HITLConversationAction,
    HITLConversationAgent,
    HITLInterceptorAction,
    HITLInterceptorAgent,
    HITLPostExecutionAction,
    HITLUserInputCollectorAction,
    HITLUserInputCollectorAgent,
)
from .special_hitl_agent import (
    HITLOutsideConversationAction,
    HITLOutsideConversationAgent,
)

SPECIAL_HITL_AGENT_REGISTRY = [
    HITLOutsideConversationAgent,
]

__all__ = [
    # HITL data model
    "HITLDecision",
    "HITLInteractionType",
    "HITLMode",
    "HITLContext",
    "HITLRequest",
    "HITLResponse",
    "HITLManager",
    # HITL Agent and Action
    "HITLBaseAgent",
    "HITLInterceptorAgent",
    "HITLUserInputCollectorAgent",
    "HITLConversationAgent",
    "HITLInterceptorAction",
    "HITLUserInputCollectorAction",
    "HITLPostExecutionAction",
    "HITLConversationAction",
    # Special HITL Agent
    "HITLOutsideConversationAgent",
    "HITLOutsideConversationAction",
    # Special HITL Agent Registry
    "SPECIAL_HITL_AGENT_REGISTRY",
]
