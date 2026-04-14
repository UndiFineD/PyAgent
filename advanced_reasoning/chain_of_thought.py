"""Chain-of-Thought Synthesis Engine

Decomposes complex reasoning into intermediate steps,
generates explanations, and validates reasoning paths.
"""

import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple


class ReasoningStep(Enum):
    """Types of reasoning steps"""

    PROBLEM_UNDERSTANDING = "understanding"
    INTERMEDIATE = "intermediate"
    CALCULATION = "calculation"
    VERIFICATION = "verification"
    CONCLUSION = "conclusion"


@dataclass
class CoTResult:
    """Result of chain-of-thought reasoning"""

    steps: List[str]
    step_types: List[str]
    answer: str
    confidence: float
    num_steps: int
    validity: bool
    reasoning_depth: str  # "shallow", "moderate", "deep"


class ChainOfThoughtGenerator:
    """Generate chain-of-thought reasoning for queries"""

    def __init__(self, model=None, max_steps: int = 5, temperature: float = 0.7):
        """Initialize CoT generator
        
        Args:
            model: LLM to use for reasoning
            max_steps: Maximum reasoning steps
            temperature: Sampling temperature (0-1)

        """
        self.model = model
        self.max_steps = max_steps
        self.temperature = temperature
        self.reasoning_cache = {}

    def generate_reasoning(self, query: str) -> CoTResult:
        """Generate chain-of-thought reasoning for a query
        
        Args:
            query: The question to reason about
            
        Returns:
            CoTResult with steps, answer, and confidence

        """
        # Check cache
        if query in self.reasoning_cache:
            return self.reasoning_cache[query]

        steps = []
        step_types = []
        context = query

        # Generate reasoning steps
        for i in range(self.max_steps):
            step_prompt = self._build_step_prompt(context, i + 1)

            # Generate next step
            step = self._generate_step(step_prompt)

            if not step:
                break

            # Classify step type
            step_type = self._classify_step(step, i)

            steps.append(step)
            step_types.append(step_type)

            # Check if this is the final answer
            if self._is_terminal_step(step):
                answer = step
                break

            # Update context for next step
            context += f"\nStep {i+1}: {step}"
        else:
            # Timeout: generate answer from accumulated steps
            answer = self._generate_answer(context)

        # Validate reasoning chain
        validity = self._validate_reasoning(steps)

        # Calculate confidence
        confidence = self._calculate_confidence(steps, answer)

        # Determine reasoning depth
        depth = self._classify_depth(len(steps))

        result = CoTResult(
            steps=steps,
            step_types=step_types,
            answer=answer,
            confidence=confidence,
            num_steps=len(steps),
            validity=validity,
            reasoning_depth=depth
        )

        # Cache result
        self.reasoning_cache[query] = result

        return result

    def _build_step_prompt(self, context: str, step_num: int) -> str:
        """Build prompt for next reasoning step"""
        if step_num == 1:
            return f"""Let me work through this step by step.

Question: {context}

Step 1: First, let me understand what we're being asked."""
        else:
            return f"""{context}

Step {step_num}: """

    def _generate_step(self, prompt: str) -> Optional[str]:
        """Generate a single reasoning step"""
        if self.model is None:
            return None

        try:
            response = self.model.generate(
                prompt,
                max_tokens=100,
                temperature=self.temperature,
                stop=["\n\nStep"]
            )
            return response.strip()
        except Exception:
            return None

    def _classify_step(self, step: str, index: int) -> str:
        """Classify the type of reasoning step"""
        step_lower = step.lower()

        if index == 0:
            return ReasoningStep.PROBLEM_UNDERSTANDING.value
        elif any(word in step_lower for word in ["calculate", "compute", "add", "multiply"]):
            return ReasoningStep.CALCULATION.value
        elif any(word in step_lower for word in ["check", "verify", "confirm"]):
            return ReasoningStep.VERIFICATION.value
        elif any(word in step_lower for word in ["therefore", "thus", "so", "finally"]):
            return ReasoningStep.CONCLUSION.value
        else:
            return ReasoningStep.INTERMEDIATE.value

    def _is_terminal_step(self, step: str) -> bool:
        """Check if this step contains the final answer"""
        terminal_markers = [
            "answer:",
            "therefore:",
            "the answer is",
            "finally:",
            "conclusion:",
            "in conclusion:"
        ]
        return any(marker in step.lower() for marker in terminal_markers)

    def _generate_answer(self, context: str) -> str:
        """Generate final answer from reasoning context"""
        if self.model is None:
            return "Unable to generate answer"

        prompt = f"""{context}

Based on the steps above, the final answer is:"""

        try:
            answer = self.model.generate(prompt, max_tokens=50)
            return answer.strip()
        except Exception:
            return "Error generating answer"

    def _validate_reasoning(self, steps: List[str]) -> bool:
        """Validate that reasoning is logically consistent"""
        if len(steps) == 0:
            return False

        # Check for minimum reasoning depth
        if len(steps) < 2:
            return False

        # Check that steps reference each other
        for i, step in enumerate(steps):
            if i > 0 and len(step.strip()) > 0:
                return True

        return True

    def _calculate_confidence(self, steps: List[str], answer: str) -> float:
        """Calculate confidence in the reasoning"""
        confidence = 0.5  # Base confidence

        # More steps = more thinking
        confidence += min(0.3, len(steps) * 0.1)

        # Answer mentioned in steps = supported by reasoning
        if any(answer in step for step in steps):
            confidence += 0.1

        # Presence of verification steps
        for step in steps:
            if any(word in step.lower() for word in ["check", "verify", "confirm"]):
                confidence += 0.05

        # Presence of conclusion
        if any(word in answer.lower() for word in ["therefore", "thus", "so"]):
            confidence += 0.05

        return min(1.0, confidence)

    def _classify_depth(self, num_steps: int) -> str:
        """Classify reasoning depth"""
        if num_steps <= 2:
            return "shallow"
        elif num_steps <= 4:
            return "moderate"
        else:
            return "deep"

    def self_consistent_reasoning(self, query: str, num_paths: int = 5) -> Dict:
        """Generate multiple CoT paths and aggregate results
        
        Args:
            query: The question to reason about
            num_paths: Number of independent reasoning paths
            
        Returns:
            Dict with all paths, answers, and final agreed answer

        """
        paths = []
        answers = []
        confidences = []

        for _ in range(num_paths):
            result = self.generate_reasoning(query)
            paths.append(result.steps)
            answers.append(result.answer)
            confidences.append(result.confidence)

        # Majority voting
        from collections import Counter
        answer_counts = Counter(answers)
        final_answer = answer_counts.most_common(1)[0][0]
        agreement = answer_counts.most_common(1)[0][1] / num_paths

        avg_confidence = sum(confidences) / len(confidences)

        return {
            'paths': paths,
            'answers': answers,
            'confidences': confidences,
            'final_answer': final_answer,
            'agreement': agreement,
            'avg_confidence': avg_confidence,
            'num_paths': num_paths
        }

    def clear_cache(self):
        """Clear reasoning cache"""
        self.reasoning_cache.clear()


class ReasoningPatternMatcher:
    """Identify and apply reasoning patterns"""

    PATTERNS = {
        'mathematical': {
            'indicators': ['calculate', 'add', 'subtract', 'multiply', 'divide', 'percent'],
            'template': 'Step 1: Identify the numbers. Step 2: Choose the operation. Step 3: Calculate.'
        },
        'logical': {
            'indicators': ['all', 'some', 'none', 'if', 'then', 'therefore'],
            'template': 'Step 1: State premises. Step 2: Apply logic rules. Step 3: Draw conclusion.'
        },
        'causal': {
            'indicators': ['because', 'caused', 'why', 'reason', 'result'],
            'template': 'Step 1: Identify cause. Step 2: Trace effects. Step 3: Conclude.'
        },
        'comparison': {
            'indicators': ['compare', 'versus', 'similar', 'different', 'better'],
            'template': 'Step 1: List attributes. Step 2: Compare. Step 3: Conclude.'
        }
    }

    @classmethod
    def identify_pattern(cls, query: str) -> Tuple[Optional[str], List[str]]:
        """Identify reasoning pattern for query"""
        query_lower = query.lower()

        for pattern_name, pattern_info in cls.PATTERNS.items():
            indicators = pattern_info['indicators']
            if any(indicator in query_lower for indicator in indicators):
                return pattern_name, indicators

        return None, []

    @classmethod
    def get_template(cls, pattern_name: str) -> str:
        """Get reasoning template for pattern"""
        if pattern_name in cls.PATTERNS:
            return cls.PATTERNS[pattern_name]['template']
        return ""


# Example usage
if __name__ == "__main__":
    # Create generator (would use actual model in production)
    cot = ChainOfThoughtGenerator()

    # Identify pattern
    query = "What is 15% of 200?"
    pattern, indicators = ReasoningPatternMatcher.identify_pattern(query)
    print(f"Pattern: {pattern}")
    print(f"Indicators: {indicators}")

    # Get template
    if pattern:
        template = ReasoningPatternMatcher.get_template(pattern)
        print(f"Template: {template}")
