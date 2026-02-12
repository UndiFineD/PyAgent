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
PyAgent Chain-of-Recursive-Thoughts (CoRT) Reasoning System.

Based on the Chain-of-Recursive-Thoughts framework for breakthrough
problem-solving and response quality through recursive thinking.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from src.core.base.common.models.communication_models import CascadeContext
from src.inference.engine import InferenceEngine

logger = logging.getLogger("pyagent.reasoning.cort")


@dataclass
class ThinkingRound:
    """Represents a single round of thinking."""
    round_number: int
    response: str
    selected: bool = False
    alternative_number: Optional[int] = None
    evaluation_score: Optional[float] = None
    timestamp: float = field(default_factory=time.time)


@dataclass
class CoRTResult:
    """Result of a CoRT reasoning process."""
    final_response: str
    thinking_history: List[ThinkingRound]
    total_rounds: int
    processing_time: float
    confidence_score: float
    reasoning_chain: List[str]


class CoRTReasoningCore:
    """
    Chain-of-Recursive-Thoughts reasoning system.

    Implements dynamic evaluation, adaptive thinking rounds, and
    multi-path reasoning for breakthrough problem-solving.
    """

    def __init__(self, inference_engine: InferenceEngine):
        self.inference_engine = inference_engine
        self.logger = logging.getLogger("pyagent.reasoning.cort.core")

    async def think_and_respond(
        self,
        user_input: str,
        context: Optional[CascadeContext] = None,
        verbose: bool = True
    ) -> CoRTResult:
        """
        Process user input with recursive thinking.

        Args:
            user_input: The user's input to process
            context: Optional cascade context for lineage tracking
            verbose: Whether to log detailed thinking process

        Returns:
            CoRTResult with final response and thinking history
        """
        start_time = time.time()

        if verbose:
            self.logger.info("🤔 Starting CoRT recursive thinking process")

        # Determine optimal thinking rounds
        thinking_rounds = await self._determine_thinking_rounds(user_input)

        if verbose:
            self.logger.info(f"🤔 Determined {thinking_rounds} thinking rounds needed")

        # Generate initial response
        initial_response = await self._generate_initial_response(user_input)

        thinking_history = [ThinkingRound(
            round_number=0,
            response=initial_response,
            selected=True
        )]

        current_best = initial_response

        # Iterative improvement through recursive thinking
        for round_num in range(1, thinking_rounds + 1):
            if verbose:
                self.logger.info(f"🤔 Round {round_num}/{thinking_rounds}")

            # [Phase 321] Self-Correction Step
            # Before generating alternatives, we perform a deep audit of the current best
            corrected_best = await self._self_correct(current_best, user_input)
            if corrected_best != current_best:
                if verbose:
                    self.logger.info("🛠️ Phase 321: Self-correction triggered and improved the response")
                current_best = corrected_best
                thinking_history.append(ThinkingRound(
                    round_number=round_num,
                    response=current_best,
                    selected=True,
                    alternative_number=0,  # 0 indicates a correction
                    evaluation_score=0.9
                ))

            # Generate alternative responses
            alternatives = await self._generate_alternatives(current_best, user_input)

            # Add alternatives to history
            for i, alt in enumerate(alternatives):
                thinking_history.append(ThinkingRound(
                    round_number=round_num,
                    response=alt,
                    selected=False,
                    alternative_number=i + 1
                ))

            # Evaluate and select best response
            new_best, explanation = await self._evaluate_responses(user_input, current_best, alternatives)

            # Update thinking history
            if new_best != current_best:
                # Mark previous best as not selected
                for item in thinking_history:
                    if item.selected and item.round_number < round_num:
                        item.selected = False
                        break

                # Mark new best as selected
                for item in thinking_history:
                    if item.response == new_best and item.round_number == round_num:
                        item.selected = True
                        break

                current_best = new_best

            if verbose:
                self.logger.info(
                    f"🤔 Round {round_num} complete. Selection: {explanation}"
                )

        # Calculate confidence and reasoning chain
        confidence_score = await self._calculate_confidence(current_best, thinking_history)
        reasoning_chain = self._extract_reasoning_chain(thinking_history)

        processing_time = time.time() - start_time

        result = CoRTResult(
            final_response=current_best,
            thinking_history=thinking_history,
            total_rounds=thinking_rounds,
            processing_time=processing_time,
            confidence_score=confidence_score,
            reasoning_chain=reasoning_chain
        )

        if verbose:
            self.logger.info(
                f"🤔 CoRT process complete in {processing_time:.2f}s "
                f"with {confidence_score:.2f} confidence"
            )

        return result

    async def _determine_thinking_rounds(self, prompt: str) -> int:
        """
        Determine optimal number of thinking rounds (1-5).

        Uses AI to analyze prompt complexity and determine reasoning depth.
        """
        meta_prompt = f"""Given this message: "{prompt}"

How many rounds of iterative thinking (1-5) would be optimal to generate the best response?
Consider the complexity, nuance required, and potential for multiple interpretations.

Respond with just a number between 1 and 5."""

        try:
            response = await self.inference_engine.generate(
                prompt=meta_prompt,
                temperature=0.3,
                max_tokens=10
            )

            # Extract number from response
            import re
            numbers = re.findall(r'\d+', response.strip())
            if numbers:
                rounds = int(numbers[0])
                return min(max(rounds, 1), 5)

        except Exception as e:
            self.logger.warning(f"Failed to determine thinking rounds: {e}")

        # Default to 3 rounds
        return 3

    async def _generate_initial_response(self, user_input: str) -> str:
        """Generate the initial response to the user input."""
        prompt = f"Please provide a thoughtful response to: {user_input}"

        try:
            response = await self.inference_engine.generate(
                prompt=prompt,
                temperature=0.7,
                max_tokens=1000
            )
            return response.strip()
        except Exception as e:
            self.logger.error(f"Failed to generate initial response: {e}")
            return "I apologize, but I encountered an error while processing your request."

    async def _generate_alternatives(self, base_response: str, prompt: str, num_alternatives: int = 3) -> List[str]:
        """
        Generate alternative responses using different approaches.

        Uses temperature variance (0.7, 0.8, 0.9) for creative diversity.
        """
        alternatives = []
        temperatures = [0.7, 0.8, 0.9][:num_alternatives]

        for i, temp in enumerate(temperatures):
            alt_prompt = (
                f"Original message: {prompt}\n"
                f"Current response: {base_response}\n"
                f"Generate an alternative response that might be better. Be creative and consider different approaches, perspectives, or emphases.\n"
                f"Alternative response:"
            )

            try:
                alternative = await self.inference_engine.generate(
                    prompt=alt_prompt,
                    temperature=temp,
                    max_tokens=1000
                )
                alternatives.append(alternative.strip())
            except Exception as e:
                self.logger.warning(f"Failed to generate alternative {i + 1}: {e}")
                alternatives.append(base_response)  # Fallback

        return alternatives

    async def _evaluate_responses(self, prompt: str, current_best: str, alternatives: List[str]) -> Tuple[str, str]:
        """
        Evaluate responses and select the best one.

        Returns (selected_response, explanation)
        """
        eval_prompt = f"""Original message: {prompt}

Evaluate these responses and choose the best one:

Current best: {current_best}

Alternatives:
{chr(10).join([f"{i + 1}. {alt}" for i, alt in enumerate(alternatives)])}

Which response best addresses the original message? Consider accuracy, clarity, completeness, and helpfulness.

First, respond with ONLY 'current' or a number (1-{len(alternatives)}).
Then on a new line, explain your choice in one sentence."""

        try:
            evaluation = await self.inference_engine.generate(
                prompt=eval_prompt,
                temperature=0.2,  # Low temperature for consistent evaluation
                max_tokens=200
            )

            # Parse evaluation response
            lines = [line.strip() for line in evaluation.split('\n') if line.strip()]

            choice = 'current'
            explanation = "No explanation provided"

            if lines:
                first_line = lines[0].lower()
                if 'current' in first_line:
                    choice = 'current'
                else:
                    # Look for number
                    import re
                    numbers = re.findall(r'\d+', first_line)
                    if numbers:
                        choice = numbers[0]

                if len(lines) > 1:
                    explanation = ' '.join(lines[1:])

            # Select response based on choice
            if choice == 'current':
                return current_best, explanation
            else:
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(alternatives):
                        return alternatives[index], explanation
                except (ValueError, IndexError):
                    pass

        except Exception as e:
            self.logger.warning(f"Failed to evaluate responses: {e}")

        # Default to current best
        return current_best, "Evaluation failed, keeping current response"

    async def _self_correct(self, response: str, original_prompt: str) -> str:
        """
        [Phase 321: Self-Correction Module]
        Analyzes the response for common failures and attempts to fix them.
        """
        correction_prompt = f"""[PHASE 321: SELF-CORRECTION AUDIT]
Original Task: {original_prompt}
Current Draft: {response}

Analyze the draft for:
1. Hallucinations or factual errors.
2. Inconsistencies or logical gaps.
3. Tone or style violations.
4. Failure to fully address the original task.

If you find errors, provide the FULL corrected response.
If the response is already perfect, respond with ONLY the word "PERFECT".

Corrected Response:"""

        try:
            correction = await self.inference_engine.generate(
                prompt=correction_prompt,
                temperature=0.3,
                max_tokens=2000
            )

            if "PERFECT" in correction[:20].upper() and len(correction) < 50:
                return response

            return correction.strip()
        except Exception as e:
            self.logger.warning(f"Phase 321: Self-correction failed: {e}")
            return response

    async def _calculate_confidence(self, final_response: str, thinking_history: List[ThinkingRound]) -> float:
        """Calculate confidence score based on thinking consistency and rounds."""
        try:
            # Base confidence on number of rounds and consistency
            total_rounds = max(1, max((r.round_number for r in thinking_history), default=1))

            # Higher rounds generally indicate more complex reasoning
            round_factor = min(total_rounds / 5.0, 1.0)

            # Consistency factor - how many rounds kept the same response
            selected_responses = [r.response for r in thinking_history if r.selected]
            if len(selected_responses) > 1:
                consistency = len(set(selected_responses)) / len(selected_responses)
            else:
                consistency = 1.0

            confidence = (round_factor * 0.6) + (consistency * 0.4)
            return min(confidence, 1.0)

        except Exception as e:
            self.logger.warning(f"Failed to calculate confidence: {e}")
            return 0.5

    def _extract_reasoning_chain(self, thinking_history: List[ThinkingRound]) -> List[str]:
        """Extract the reasoning chain from thinking history."""
        chain = []
        for round_item in thinking_history:
            if round_item.selected:
                # Truncate long responses for chain
                response = round_item.response
                if len(response) > 200:
                    response = response[:200] + "..."
                chain.append(f"Round {round_item.round_number}: {response}")
        return chain


class CoRTAgentMixin:
    """
    Mixin to add CoRT reasoning capabilities to agents.

    Integrates CoRT reasoning into the agent workflow.
    """

    def __init__(self, *args, cort_core: Optional[CoRTReasoningCore] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cort_core = cort_core
        self.enable_cort_reasoning = True

    async def process_with_cort(self, user_input: str, context: Optional[CascadeContext] = None) -> Dict[str, Any]:
        """
        Process user input using CoRT reasoning.

        Args:
            user_input: User input to process
            context: Optional cascade context

        Returns:
            Processing result with CoRT metadata
        """
        if not self.cort_core or not self.enable_cort_reasoning:
            # Fallback to normal processing
            return await self.process_input(user_input, context)

        # Use CoRT reasoning
        cort_result = await self.cort_core.think_and_respond(user_input, context)

        # Create response with CoRT metadata
        result = {
            'response': cort_result.final_response,
            'cort_metadata': {
                'thinking_rounds': cort_result.total_rounds,
                'processing_time': cort_result.processing_time,
                'confidence_score': cort_result.confidence_score,
                'reasoning_chain': cort_result.reasoning_chain,
                'total_alternatives': len(cort_result.thinking_history) - cort_result.total_rounds
            }
        }

        return result
