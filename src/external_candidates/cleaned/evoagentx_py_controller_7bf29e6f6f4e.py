# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\evoagentx.py\evoagentx.py\workflow.py\controller_7bf29e6f6f4e.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\EvoAgentX\evoagentx\workflow\controller.py

from typing import List


from pydantic import Field


from ..agents.agent_manager import AgentManager

from ..core.module import BaseModule

from ..optimizers.optimizer import Optimizer

from .workflow import WorkFlow


class WorkFlowController(BaseModule):
    agent_manager: AgentManager

    workflow: WorkFlow

    optimizers: List[Optimizer] = Field(default_factory=list)

    def start(self, **kwargs):
        """

        start executing the workflow.

        """

        pass
