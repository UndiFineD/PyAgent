#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Reflection Loop System for Self-Improving Agents

This module implements an iterative reflection pattern where agents can:
1. Generate initial solutions/code
2. Reflect on their work through critique
3. Refine based on feedback
4. Repeat until satisfactory results are achieved

Based on patterns from agentic_design_patterns repository.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ReflectionResult(BaseModel):
    """Result of a reflection iteration."""
    iteration: int
    content: Any
    critique: str
    is_satisfactory: bool
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ReflectionLoopConfig(BaseModel):
    """Configuration for reflection loop execution."""
    max_iterations: int = Field(default=3, description="Maximum number of reflection iterations")
    critique_prompt: str = Field(
        default="You are a senior software engineer and expert code reviewer. Critically evaluate the provided content based on the original requirements. Look for bugs, style issues, missing edge cases, and areas for improvement. If the content is perfect and meets all requirements, respond with the single phrase 'CONTENT_IS_PERFECT'. Otherwise, provide specific, actionable critiques.",
        description="Prompt template for the critic agent"
    )
    refinement_prompt: str = Field(
        default="Please refine the content using the critiques provided. Address each critique systematically and improve the overall quality.",
        description="Prompt template for refinement instructions"
    )
    early_stopping: bool = Field(default=True, description="Stop early if content is deemed perfect")
    timeout_seconds: Optional[float] = Field(default=None, description="Timeout for each iteration")


@dataclass
class ReflectionContext:
    """Context maintained throughout the reflection loop."""
    task_description: str
    current_content: Any = None
    history: List[ReflectionResult] = field(default_factory=list)
    config: ReflectionLoopConfig = field(default_factory=ReflectionLoopConfig)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ReflectionAgent(ABC):
    """Abstract base class for agents that can participate in reflection loops."""

    @abstractmethod
    async def generate(self, context: ReflectionContext) -> Any:
        """Generate initial content or refine existing content."""
        pass

    @abstractmethod
    async def critique(self, context: ReflectionContext, content: Any) -> str:
        """Provide critique of the given content."""
        pass


class LLMReflectionAgent(ReflectionAgent):
    """LLM-based reflection agent using any LLM provider."""

    def __init__(self, llm_callable: Callable[[str], str], name: str = "LLM Agent"):
        self.llm_callable = llm_callable
        self.name = name

    async def generate(self, context: ReflectionContext) -> Any:
        """Generate content using LLM."""
        if context.current_content is None:
            # Initial generation
            prompt = f"Task: {context.task_description}\n\nGenerate a solution:"
        else:
            # Refinement
            last_critique = context.history[-1].critique if context.history else ""
            prompt = f"Original Task: {context.task_description}\n\nCurrent Content:\n{context.current_content}\n\nCritique: {last_critique}\n\n{context.config.refinement_prompt}"

        # Run LLM call in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(None, self.llm_callable, prompt)
        return content

    async def critique(self, context: ReflectionContext, content: Any) -> str:
        """Critique content using LLM."""
        prompt = f"{context.config.critique_prompt}\n\nOriginal Task:\n{context.task_description}\n\nContent to Review:\n{content}"

        loop = asyncio.get_event_loop()
        critique = await loop.run_in_executor(None, self.llm_callable, prompt)
        return critique


class CodeReflectionAgent(LLMReflectionAgent):
    """Specialized agent for code reflection and improvement."""

    def __init__(self, llm_callable: Callable[[str], str], language: str = "python"):
        super().__init__(llm_callable, f"Code Agent ({language})")
        self.language = language

    async def generate(self, context: ReflectionContext) -> str:
        """Generate or refine code with language-specific considerations."""
        if context.current_content is None:
            prompt = f"Write {self.language} code for the following task:\n{context.task_description}\n\nProvide only the code without explanation:"
        else:
            last_critique = context.history[-1].critique if context.history else ""
            prompt = f"Original Task: {context.task_description}\n\nCurrent {self.language} code:\n```python\n{context.current_content}\n```\n\nCritique: {last_critique}\n\n{context.config.refinement_prompt}\n\nProvide only the improved code:"

        loop = asyncio.get_event_loop()
        code = await loop.run_in_executor(None, self.llm_callable, prompt)

        # Clean up code blocks if present
        if "```" in code:
            # Extract code from markdown blocks
            lines = code.split('\n')
            in_code_block = False
            clean_code = []
            for line in lines:
                if line.startswith('```'):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    clean_code.append(line)
            code = '\n'.join(clean_code)

        return code.strip()

    async def critique(self, context: ReflectionContext, content: str) -> str:
        """Provide code-specific critique."""
        prompt = f"""You are a senior software engineer specializing in {self.language} code review.

Critically evaluate this {self.language} code based on:
- Correctness and functionality
- Code style and best practices
- Error handling and edge cases
- Performance considerations
- Security implications
- Maintainability and readability

Original Task:
{context.task_description}

Code to Review:
```python
{content}
```

If the code is perfect and meets all requirements, respond with 'CODE_IS_PERFECT'.
Otherwise, provide specific, actionable critiques numbered as a list."""

        loop = asyncio.get_event_loop()
        critique = await loop.run_in_executor(None, self.llm_callable, prompt)
        return critique


class ReflectionLoopOrchestrator:
    """Orchestrates the reflection loop process."""

    def __init__(self, generator_agent: ReflectionAgent, critic_agent: Optional[ReflectionAgent] = None):
        self.generator = generator_agent
        self.critic = critic_agent or generator_agent  # Use same agent if not specified

    async def execute_reflection_loop(
        self,
        task_description: str,
        config: Optional[ReflectionLoopConfig] = None
    ) -> ReflectionContext:
        """Execute the complete reflection loop."""
        context = ReflectionContext(
            task_description=task_description,
            config=config or ReflectionLoopConfig()
        )

        logger.info(f"Starting reflection loop for task: {task_description[:100]}...")

        for iteration in range(context.config.max_iterations):
            logger.info(f"Reflection iteration {iteration + 1}/{context.config.max_iterations}")

            try:
                # Step 1: Generate/Refine content
                content = await self.generator.generate(context)
                context.current_content = content

                # Step 2: Critique the content
                critique = await self.critic.critique(context, content)

                # Step 3: Check for early stopping
                is_perfect = self._is_content_perfect(critique)
                is_satisfactory = is_perfect

                # Create result record
                result = ReflectionResult(
                    iteration=iteration + 1,
                    content=content,
                    critique=critique,
                    is_satisfactory=is_satisfactory,
                    metadata={"agent": self.generator.name}
                )
                context.history.append(result)

                logger.info(f"Iteration {iteration + 1} complete. Satisfactory: {is_satisfactory}")

                # Early stopping if perfect or satisfactory
                if is_perfect and context.config.early_stopping:
                    logger.info("Content deemed perfect. Stopping early.")
                    break

            except Exception as e:
                logger.error(f"Error in reflection iteration {iteration + 1}: {e}")
                # Add error result to history
                error_result = ReflectionResult(
                    iteration=iteration + 1,
                    content=context.current_content,
                    critique=f"Error occurred: {str(e)}",
                    is_satisfactory=False,
                    metadata={"error": str(e)}
                )
                context.history.append(error_result)
                break

        logger.info(f"Reflection loop completed after {len(context.history)} iterations")
        return context

    def _is_content_perfect(self, critique: str) -> bool:
        """Check if critique indicates content is perfect."""
        perfect_indicators = ["CONTENT_IS_PERFECT", "CODE_IS_PERFECT", "PERFECT"]
        return any(indicator.upper() in critique.upper() for indicator in perfect_indicators)

    def get_final_result(self, context: ReflectionContext) -> Optional[ReflectionResult]:
        """Get the final (best) result from the reflection loop."""
        if not context.history:
            return None

        # Return the last satisfactory result, or the last result if none were satisfactory
        satisfactory_results = [r for r in context.history if r.is_satisfactory]
        if satisfactory_results:
            return satisfactory_results[-1]
        else:
            return context.history[-1]

    def get_reflection_summary(self, context: ReflectionContext) -> Dict[str, Any]:
        """Generate a summary of the reflection process."""
        final_result = self.get_final_result(context)

        return {
            "task_description": context.task_description,
            "total_iterations": len(context.history),
            "max_iterations": context.config.max_iterations,
            "final_content": final_result.content if final_result else None,
            "final_critique": final_result.critique if final_result else None,
            "is_satisfactory": final_result.is_satisfactory if final_result else False,
            "iterations_summary": [
                {
                    "iteration": r.iteration,
                    "is_satisfactory": r.is_satisfactory,
                    "critique_preview": r.critique[:100] + "..." if len(r.critique) > 100 else r.critique
                }
                for r in context.history
            ]
        }


# Convenience functions for common use cases

async def reflect_on_code(
    code_task: str,
    llm_callable: Callable[[str], str],
    language: str = "python",
    max_iterations: int = 3
) -> Dict[str, Any]:
    """Convenience function for code reflection."""
    agent = CodeReflectionAgent(llm_callable, language)
    orchestrator = ReflectionLoopOrchestrator(agent)

    config = ReflectionLoopConfig(max_iterations=max_iterations)
    context = await orchestrator.execute_reflection_loop(code_task, config)

    return orchestrator.get_reflection_summary(context)


async def reflect_on_content(
    task: str,
    llm_callable: Callable[[str], str],
    max_iterations: int = 3
) -> Dict[str, Any]:
    """Convenience function for general content reflection."""
    agent = LLMReflectionAgent(llm_callable)
    orchestrator = ReflectionLoopOrchestrator(agent)

    config = ReflectionLoopConfig(max_iterations=max_iterations)
    context = await orchestrator.execute_reflection_loop(task, config)

    return orchestrator.get_reflection_summary(context)
