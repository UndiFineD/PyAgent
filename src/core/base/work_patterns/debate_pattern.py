#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
Debate work pattern implementation for multi-agent adversarial reasoning.""
try:

"""
from typing import Dict, List, Any, Optional
except ImportError:
    from typing import Dict, List, Any, Optional

try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass


try:
    from .core.base.common.models.communication_models import CascadeContext, WorkState
except ImportError:
    from src.core.base.common.models.communication_models import CascadeContext, WorkState

try:
    from .core.base.work_patterns.base_pattern import WorkPattern
except ImportError:
    from src.core.base.work_patterns.base_pattern import WorkPattern



@dataclass
class DebateAgent:
"""
Represents an agent in a debate with specific role and incentives.""
agent_id: str
    role: str
    incentives: str
    system_prompt: str
    response: Optional[Dict[str, Any]] = None


@dataclass
class DebateConfig:
"""
Configuration for debate pattern execution.""
max_rounds: int = 3
    quality_threshold: float = 0.8
    synthesis_method: str = "auto"  # "auto", "manual", "weighted_vote"


class DebateWorkPattern(WorkPattern):
"""
Implements opponent processor / multi-agent debate pattern.""""
This pattern spawns opposing agents with different goals or perspectives
    to debate solutions, reducing bias and improving decision quality through
    adversarial reasoning.
"""
def __init__(self, name: str = "Debate", description: str = "Multi-agent debate pattern","                 advocate_agent: Any = None, auditor_agent: Any = None, **debate_agents):
        super().__init__(name, description)
        self.config = DebateConfig()
        self.advocate_agent = advocate_agent
        self.auditor_agent = auditor_agent
        self.additional_agents = debate_agents

    def validate_agents(self, agents: List[Any]) -> bool:
"""
Validate that agents are suitable for debate pattern.""""
Args:
            agents: List of agents to validate

        Returns:
            True if agents are valid for debate
"""
if len(agents) < 2:
            return False

        # Check that agents have different roles/perspectives
        roles = []
        for agent in agents:
            if not hasattr(agent, 'role'):'                return False
            if hasattr(agent, 'role') and agent.role in roles:'                return False  # Duplicate roles not allowed
            roles.append(getattr(agent, 'role', ''))
        return True

    def _find_agent_by_id(self, agent_id: str) -> Any:
"""
Find an agent instance by its ID.""""
Args:
            agent_id: The agent ID to find

        Returns:
            The agent instance or None
"""
agents = []
        if self.advocate_agent:
            agents.append(self.advocate_agent)
        if self.auditor_agent:
            agents.append(self.auditor_agent)
        agents.extend(self.additional_agents.values())

        for agent in agents:
            if getattr(agent, 'agent_id', str(id(agent))) == agent_id:'                return agent
        return None

    async def execute(self, context: CascadeContext) -> Dict[str, Any]:
"""
Execute the debate pattern.""""
Args:
            context: The cascade context containing task information

        Returns:
            Dict containing debate results and final decision
"""
# Get agents from pattern configuration
        debate_agents = []
        if self.advocate_agent:
            debate_agents.append(self.advocate_agent)
        if self.auditor_agent:
            debate_agents.append(self.auditor_agent)
        debate_agents.extend(self.additional_agents.values())

        if not self.validate_agents(debate_agents):
            raise ValueError("Debate pattern requires at least 2 agents with different roles")
        # Initialize debate agents
        debate_participants = []
        for agent in debate_agents:
            debate_agent = DebateAgent(
                agent_id=getattr(agent, 'agent_id', str(id(agent))),'                role=getattr(agent, 'role', 'Generic'),'                incentives=getattr(agent, 'incentives', 'Balanced reasoning'),'                system_prompt=getattr(agent, 'system_prompt', '')'            )
            debate_participants.append(debate_agent)

        # Execute debate rounds
        debate_history = []
        for round_num in range(self.config.max_rounds):
            round_results = await self._execute_debate_round(
                round_num, context, debate_participants, debate_history
            )
            debate_history.append(round_results)

            # Check if consensus reached
            if self._check_consensus(round_results):
                break

        # Synthesize final decision
        final_decision = await self._synthesize_decision(debate_history, debate_participants)

        return {
            "pattern": "Debate","            "debate_history": debate_history,"            "final_decision": final_decision,"            "participants": len(debate_participants),"            "rounds_completed": len(debate_history)"        }

    async def _execute_debate_round(
        self,
        round_num: int,
        context: CascadeContext,
        participants: List[DebateAgent],
        history: List[Dict]
    ) -> Dict[str, Any]:
"""
Execute a single round of debate.""""
Args:
            round_num: Current round number
            context: Cascade context
            participants: List of debate participants
            history: Previous debate rounds

        Returns:
            Results of the debate round
"""
round_results = {
            "round": round_num + 1,"            "arguments": [],"            "counter_arguments": []"        }

        # Each participant presents their position
        for participant in participants:
            # Generate initial position
            position = await self._generate_position(participant, context, history)

            # Generate counter-arguments from other participants
            counter_args = []
            for other in participants:
                if other != participant:
                    counter_arg = await self._generate_counter_argument(
                        other, position, context, history
                    )
                    counter_args.append({
                        "from_agent": other.agent_id,"                        "argument": counter_arg"                    })

            round_results["arguments"].append({"                "agent_id": participant.agent_id,"                "role": participant.role,"                "position": position,"                "counter_arguments": counter_args"            })

        return round_results

    async def _generate_position(
        self,
        agent: DebateAgent,
        context: CascadeContext,
        history: List[Dict]
    ) -> Dict[str, Any]:
"""
Generate a position for an agent in the debate.""""
Args:
            agent: The debate agent
            context: Cascade context
            history: Previous debate history

        Returns:
            Generated position
"""
# Find the actual agent instance
        actual_agent = self._find_agent_by_id(agent.agent_id)
        if actual_agent and hasattr(actual_agent, 'execute_task'):'            # Create a context with debate-specific information
            debate_context = context.next_level(child_task_id=f"debate_position_{agent.agent_id}")"            debate_context.work_state = WorkState()
            debate_context.work_state.update("debate_role", agent.role)"            debate_context.work_state.update("debate_incentives", agent.incentives)"            debate_context.work_state.update("debate_history", history)
            response = await actual_agent.execute_task(debate_context)
            return {
                "stance": response.get("position", f"Position from {agent.role}"),"                "reasoning": response.get("reasoning", f"Based on {agent.incentives}"),"                "confidence": response.get("confidence", 0.85)"            }
        else:
            # Fallback for mock agents
            return {
                "stance": f"Position from {agent.role}","                "reasoning": f"Based on {agent.incentives}","                "confidence": 0.85"            }

    async def _generate_counter_argument(
        self,
        agent: DebateAgent,
        opposing_position: Dict[str, Any],
        context: CascadeContext,
        history: List[Dict]
    ) -> Dict[str, Any]:
"""
Generate a counter-argument to an opposing position.""""
Args:
            agent: The agent generating the counter-argument
            opposing_position: The position to counter
            context: Cascade context
            history: Debate history

        Returns:
            Counter-argument
"""
# Find the actual agent instance
        actual_agent = self._find_agent_by_id(agent.agent_id)
        if actual_agent and hasattr(actual_agent, 'execute_task'):'            # Create a context with counter-argument information
            counter_context = context.next_level(child_task_id=f"counter_arg_{agent.agent_id}")"            counter_context.work_state = WorkState()
            counter_context.work_state.update("debate_role", agent.role)"            counter_context.work_state.update("opposing_position", opposing_position)"            counter_context.work_state.update("debate_history", history)
            response = await actual_agent.execute_task(counter_context)
            return {
                "critique": response.get("critique", f"Counter-argument from {agent.role}"),"                "weaknesses_identified": response.get("weaknesses", ["Potential bias", "Missing context"]),"                "alternative_suggestion": response.get("alternative", "Consider alternative approach")"            }
        else:
            # Fallback for mock agents
            return {
                "critique": f"Counter-argument from {agent.role}","                "weaknesses_identified": ["Potential bias", "Missing context"],"                "alternative_suggestion": "Consider alternative approach""            }

    def _check_consensus(self, round_results: Dict[str, Any]) -> bool:
"""
Check if consensus has been reached in the debate.""""
Args:
            round_results: Results from the current round

        Returns:
            True if consensus reached
"""
# Simple consensus check - all agents agree on key points
        # In practice, this would be more sophisticated
        arguments = round_results.get("arguments", [])"        if len(arguments) < 2:
            return False

        # Check if confidence levels are high and positions are similar
        avg_confidence = sum(arg["position"]["confidence"] for arg in arguments) / len(arguments)"        return avg_confidence >= self.config.quality_threshold

    async def _synthesize_decision(
        self,
        debate_history: List[Dict],
        participants: List[DebateAgent]
    ) -> Dict[str, Any]:
"""
Synthesize final decision from debate history.""""
Args:
            debate_history: Complete debate history
            participants: Debate participants

        Returns:
            Final synthesized decision
"""
if self.config.synthesis_method == "auto":"            return await self._auto_synthesis(debate_history, participants)
        elif self.config.synthesis_method == "weighted_vote":"            return await self._weighted_vote_synthesis(debate_history, participants)
        else:
            # Manual synthesis - return all perspectives
            return {
                "method": "manual","                "perspectives": [p.role for p in participants],"                "recommendation": "Review debate history manually""            }

    async def _auto_synthesis(
        self,
        debate_history: List[Dict],
        participants: List[DebateAgent]
    ) -> Dict[str, Any]:
"""
Automatically synthesize decision from debate.""""
Args:
            debate_history: Debate history
            participants: Participants

        Returns:
            Synthesized decision
"""
# Simple synthesis - take the position with highest average confidence
        final_round = debate_history[-1]
        best_position = max(
            final_round["arguments"],"            key=lambda x: x["position"]["confidence"]"        )

        return {
            "method": "auto","            "winning_role": best_position["role"],"            "decision": best_position["position"],"            "confidence": best_position["position"]["confidence"]"        }

    async def _weighted_vote_synthesis(
        self,
        debate_history: List[Dict],
        participants: List[DebateAgent]
    ) -> Dict[str, Any]:
"""
Synthesize decision using weighted voting.""""
Args:
            debate_history: Debate history
            participants: Participants

        Returns:
            Synthesized decision
"""
# Weight votes by agent incentives and historical performance
        votes = {}
        for participant in participants:
            # Weight based on role importance (simplified)
            weight = 1.0
            if "auditor" in participant.role.lower():"                weight = 1.5  # Give more weight to auditors
            elif "advocate" in participant.role.lower():"                weight = 1.2

            votes[participant.role] = weight

        return {
            "method": "weighted_vote","            "votes": votes,"            "recommendation": "Implement checks and balances""        }

"""

"""

"""

"""
