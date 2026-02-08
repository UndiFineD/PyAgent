# Extracted from: C:\DEV\PyAgent\.external\EvoAgentX\evoagentx\frameworks\multi_agent_debate\utils.py
from ...prompts.workflow.multi_agent_debate import (
    collect_last_round_candidates,
    collect_round_candidates,
    format_transcript,
)

# Re-export functions for backward compatibility
__all__ = [
    "format_transcript",
    "collect_last_round_candidates",
    "collect_round_candidates",
]
