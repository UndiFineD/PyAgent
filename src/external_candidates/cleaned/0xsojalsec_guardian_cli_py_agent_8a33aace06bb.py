# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_guardian_cli.py\core.py\agent_8a33aace06bb.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\core\agent.py

"""

Base agent class for all Guardian AI agents

"""

from abc import ABC, abstractmethod

from typing import Any, Dict, Optional

from ai.gemini_client import GeminiClient

from utils.logger import get_logger

from core.memory import PentestMemory


class BaseAgent(ABC):
    """Base class for all AI agents in Guardian"""

    def __init__(
        self,
        name: str,
        config: Dict[str, Any],
        gemini_client: GeminiClient,
        memory: PentestMemory,
    ):
        self.name = name

        self.config = config

        self.gemini = gemini_client

        self.memory = memory

        self.logger = get_logger(config)

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the agent's primary function"""

        pass

    async def think(self, prompt: str, system_prompt: str) -> Dict[str, str]:
        """

        Use AI to think through a problem with reasoning

        Returns:

            Dict with 'reasoning' and 'response' keys

        """

        try:
            result = await self.gemini.generate_with_reasoning(prompt=prompt, system_prompt=system_prompt)

            # Log AI decision

            self.logger.log_ai_decision(
                agent=self.name,
                decision=result["response"],
                reasoning=result["reasoning"],
                context={"prompt": prompt[:200]},
            )

            # Store in memory

            self.memory.add_ai_decision(
                agent=self.name,
                decision=result["response"],
                reasoning=result["reasoning"],
            )

            return result

        except Exception as e:
            self.logger.error(f"Agent {self.name} thinking error: {e}")

            raise

    def log_action(self, action: str, details: str):
        """Log an agent action"""

        self.logger.info(f"[{self.name}] {action}: {details}")
