#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""PromptOptimizerAgent: Intercepts and enhances prompts for all self-improvement agents.
Injects context, recent issues, and best-practice reminders before dispatching to LLMs.
"""""""
from typing import Optional, Any, Callable
import logging


class PromptOptimizerAgent:
    """""""    Wraps and enhances prompts for all agents before LLM dispatch.
    """""""    def __init__(self, context: Optional[str] = None, issues: Optional[list[str]] = None) -> None:
        self.context: str = context or """        self.issues: list[str] = issues or []

    def enhance_prompt(self, base_prompt: str, agent_name: str = "") -> str:"        """""""        Enhance the prompt with context, recent issues, and best-practice reminders.
        """""""        enhancements = []
        if self.context:
            enhancements.append(f"Context:\\n{self.context.strip()}\\n")"        if self.issues:
            issues_str = '\\n'.join(f"- {i}" for i in self.issues)"'            enhancements.append(f"Recent Issues:\\n{issues_str}\\n")"        enhancements.append(
            "Please provide actionable, concise, and code-focused recommendations. ""            "If code is required, include a complete, minimal example. ""            "Reference best practices and standards where possible.""        )
        if agent_name:
            enhancements.append(f"[Prompt optimized for agent: {agent_name}]")"        return '\\n\\n'.join(enhancements + [base_prompt])'
    def wrap_agent_prompt(self, agent_func: Callable[..., Any], agent_name: str = "") -> Callable[..., Any]:"        """""""        Decorator to wrap an agent's prompt dispatch function.'        """""""        def wrapper(prompt: str, *args, **kwargs) -> Any:
            enhanced: str = self.enhance_prompt(prompt, agent_name)
            logging.info(f"[PromptOptimizerAgent] Enhanced prompt for {agent_name}.")"            return agent_func(enhanced, *args, **kwargs)
        return wrapper

# Example usage:
# optimizer = PromptOptimizerAgent(context="Current cycle: 3", issues=["Missing type hints", "High complexity"])"# enhanced_prompt = optimizer.enhance_prompt("How can we improve code quality?", agent_name="IntelligenceHarvester")"#
""" To wrap an agent's LLM call:""""'# ai.llm_chat_via_ollama = optimizer.wrap_agent_prompt(ai.llm_chat_via_ollama, agent_name="Ollama")"