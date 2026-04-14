"""Neuro-Symbolic Reasoning Integration

Combines neural and symbolic reasoning for the best of both worlds.
Falls back gracefully when one approach fails. 

Features:
  - Hybrid reasoning selection
  - Confidence-aware routing
  - Fallback mechanisms
  - Method blending
  - Explanation synthesis
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Callable, Dict, Optional, Tuple, Union


class ReasoningMethod(Enum):
    """Types of reasoning methods available"""

    NEURAL = "neural"           # LLM-based
    SYMBOLIC = "symbolic"       # Logic/knowledge-based
    PLANNING = "planning"       # Goal decomposition
    DEBATE = "debate"          # Multi-agent
    HYBRID = "hybrid"          # Combined


@dataclass
class ReasoningAttempt:
    """Result from a single reasoning attempt"""

    method: ReasoningMethod
    answer: Union[str, float, int, bool]
    confidence: float
    explanation: str
    latency_ms: float
    success: bool
    error: Optional[str] = None
    metadata: Dict = None


@dataclass
class HybridReasoningResult:
    """Result from hybrid reasoning"""

    final_answer: Union[str, float, int, bool]
    confidence: float
    method_used: ReasoningMethod
    method_confidence: float
    neural_attempt: Optional[ReasoningAttempt]
    symbolic_attempt: Optional[ReasoningAttempt]
    planning_attempt: Optional[ReasoningAttempt]
    debate_attempt: Optional[ReasoningAttempt]
    explanation: str
    reasoning_trace: str  # How we got to this answer
    execution_time_ms: float

    def __str__(self) -> str:
        return f"""
Hybrid Reasoning Result
══════════════════════════════════════
Answer:       {self.final_answer}
Confidence:   {self.confidence:.1%}
Method Used:  {self.method_used.value} (confidence: {self.method_confidence:.1%})
Execution:    {self.execution_time_ms:.1f}ms

Explanation:
{self.explanation}

Reasoning Trace:
{self.reasoning_trace}
"""


class ReasoningStrategy(ABC):
    """Base class for reasoning strategies"""

    @abstractmethod
    def can_handle(self, query: str) -> bool:
        """Check if strategy can handle query"""
        pass

    @abstractmethod
    def reason(self, query: str) -> Optional[ReasoningAttempt]:
        """Execute reasoning"""
        pass

    @property
    @abstractmethod
    def method_name(self) -> ReasoningMethod:
        """Method identifier"""
        pass


class NeuralReasoningStrategy(ReasoningStrategy):
    """Use neural (LLM) reasoning"""

    def __init__(self, model=None):
        self.model = model

    def can_handle(self, query: str) -> bool:
        """Neural can handle almost anything"""
        return len(query) > 0

    def reason(self, query: str) -> Optional[ReasoningAttempt]:
        """Use LLM for reasoning"""
        if not self.model:
            return None

        try:
            import time
            start = time.time()

            response = self.model.generate(query, max_tokens=200)

            latency = (time.time() - start) * 1000

            return ReasoningAttempt(
                method=ReasoningMethod.NEURAL,
                answer=response,
                confidence=0.75,
                explanation=response,
                latency_ms=latency,
                success=True
            )
        except Exception as e:
            return ReasoningAttempt(
                method=ReasoningMethod.NEURAL,
                answer="",
                confidence=0.0,
                explanation="",
                latency_ms=0,
                success=False,
                error=str(e)
            )

    @property
    def method_name(self) -> ReasoningMethod:
        return ReasoningMethod.NEURAL


class SymbolicReasoningStrategy(ReasoningStrategy):
    """Use symbolic reasoning when possible"""

    def __init__(self, knowledge_base=None):
        self.knowledge_base = knowledge_base

    def can_handle(self, query: str) -> bool:
        """Check if query is symbolic/mathematical"""
        math_keywords = ['calculate', 'compute', 'solve', 'equals', '%', 'percent']
        logic_keywords = ['if', 'then', 'implies', 'therefore', 'true', 'false']

        query_lower = query.lower()
        return any(kw in query_lower for kw in math_keywords + logic_keywords)

    def reason(self, query: str) -> Optional[ReasoningAttempt]:
        """Use symbolic reasoning"""
        try:
            import re
            import time
            start = time.time()

            # Extract mathematical expression
            match = re.search(r'(\d+(?:\.\d+)?)\s*%\s*(?:of\s+)?(\d+(?:\.\d+)?)', query)
            if match:
                percent, value = float(match.group(1)), float(match.group(2))
                answer = (percent / 100) * value

                latency = (time.time() - start) * 1000

                return ReasoningAttempt(
                    method=ReasoningMethod.SYMBOLIC,
                    answer=answer,
                    confidence=1.0,  # Exact!
                    explanation=f"Symbolic calculation: {percent}% of {value} = {answer}",
                    latency_ms=latency,
                    success=True,
                    metadata={'type': 'percentage'}
                )

            return None
        except Exception:
            return None

    @property
    def method_name(self) -> ReasoningMethod:
        return ReasoningMethod.SYMBOLIC


class PlanningReasoningStrategy(ReasoningStrategy):
    """Use hierarchical planning for complex goals"""

    def __init__(self, planner=None):
        self.planner = planner

    def can_handle(self, query: str) -> bool:
        """Check if query needs planning"""
        planning_keywords = ['plan', 'how to', 'steps', 'process', 'schedule', 'timeline']
        return any(kw in query.lower() for kw in planning_keywords)

    def reason(self, query: str) -> Optional[ReasoningAttempt]:
        """Use planning"""
        if not self.planner:
            return None

        try:
            import time
            start = time.time()

            # Extract goal
            goal = query.replace('plan ', '').replace('how to ', '')

            plan = self.planner.plan_goal(goal)

            latency = (time.time() - start) * 1000

            return ReasoningAttempt(
                method=ReasoningMethod.PLANNING,
                answer=plan.goal,
                confidence=0.8,
                explanation=f"Hierarchical plan: {len(plan.all_tasks)} tasks, {plan.total_duration_hours:.1f}h",
                latency_ms=latency,
                success=True,
                metadata={'tasks': len(plan.all_tasks), 'duration_hours': plan.total_duration_hours}
            )
        except Exception:
            return None

    @property
    def method_name(self) -> ReasoningMethod:
        return ReasoningMethod.PLANNING


class NeuroSymbolicFusion:
    """Intelligently combines neural and symbolic reasoning"""

    def __init__(
        self,
        neural_model=None,
        symbolic_kb=None,
        planner=None,
        debater=None
    ):
        """Initialize hybrid reasoner.
        
        Args:
            neural_model: LLM model
            symbolic_kb: Knowledge base/reasoning engine
            planner: Hierarchical planner
            debater: Multi-agent debate framework

        """
        self.strategies: Dict[ReasoningMethod, ReasoningStrategy] = {
            ReasoningMethod.NEURAL: NeuralReasoningStrategy(neural_model),
            ReasoningMethod.SYMBOLIC: SymbolicReasoningStrategy(symbolic_kb),
            ReasoningMethod.PLANNING: PlanningReasoningStrategy(planner),
        }

        self.preference_order = [
            ReasoningMethod.SYMBOLIC,    # Fastest, most reliable
            ReasoningMethod.PLANNING,    # For goal queries
            ReasoningMethod.NEURAL,      # Fallback
        ]

        self.attempt_history = []

    def reason(self, query: str) -> HybridReasoningResult:
        """Reason using hybrid approach.
        
        Tries multiple methods, picks best result.
        """
        import time
        start_time = time.time()

        attempts = {
            ReasoningMethod.NEURAL: None,
            ReasoningMethod.SYMBOLIC: None,
            ReasoningMethod.PLANNING: None,
        }

        # Try each strategy in preference order
        for method in self.preference_order:
            strategy = self.strategies.get(method)
            if not strategy:
                continue

            if strategy.can_handle(query):
                attempt = strategy.reason(query)
                if attempt:
                    attempts[method] = attempt

                    # If confident, stop here
                    if attempt.confidence >= 0.85:
                        break

        # Pick best result
        best_attempt = self._select_best_attempt(attempts)

        execution_time = (time.time() - start_time) * 1000

        # Store in history
        self.attempt_history.append((query, attempts, best_attempt))

        # Create result
        result = HybridReasoningResult(
            final_answer=best_attempt.answer,
            confidence=best_attempt.confidence,
            method_used=best_attempt.method,
            method_confidence=best_attempt.confidence,
            neural_attempt=attempts[ReasoningMethod.NEURAL],
            symbolic_attempt=attempts[ReasoningMethod.SYMBOLIC],
            planning_attempt=attempts[ReasoningMethod.PLANNING],
            debate_attempt=None,
            explanation=best_attempt.explanation,
            reasoning_trace=self._build_trace(attempts, best_attempt),
            execution_time_ms=execution_time
        )

        return result

    def _select_best_attempt(self, attempts: Dict[ReasoningMethod, Optional[ReasoningAttempt]]) -> ReasoningAttempt:
        """Select best reasoning attempt"""
        # Filter successful attempts
        successful = {
            method: attempt
            for method, attempt in attempts.items()
            if attempt and attempt.success
        }

        if not successful:
            # All failed, return first attempt with error
            for method in self.preference_order:
                if attempts[method]:
                    return attempts[method]
            # Fallback
            return ReasoningAttempt(
                method=ReasoningMethod.NEURAL,
                answer="Unable to reason",
                confidence=0.0,
                explanation="All reasoning methods failed",
                latency_ms=0,
                success=False
            )

        # Pick highest confidence
        return max(successful.values(), key=lambda a: a.confidence)

    def _build_trace(
        self,
        attempts: Dict[ReasoningMethod, Optional[ReasoningAttempt]],
        best: ReasoningAttempt
    ) -> str:
        """Build human-readable reasoning trace"""
        trace = "Reasoning Trace:\n"

        for method in self.preference_order:
            attempt = attempts[method]
            if attempt:
                status = "✓" if attempt.success else "✗"
                trace += f"  {status} {method.value}: {attempt.confidence:.0%} confidence ({attempt.latency_ms:.1f}ms)\n"
                if attempt.error:
                    trace += f"      Error: {attempt.error}\n"

        trace += f"\nSelected: {best.method.value}\n"
        return trace


class FallbackMechanism:
    """Graceful fallback when reasoning fails"""

    def __init__(self):
        self.fallback_chain = []

    def register_fallback(
        self,
        primary_method: ReasoningMethod,
        fallback_method: ReasoningMethod
    ):
        """Register a fallback strategy"""
        self.fallback_chain.append((primary_method, fallback_method))

    def get_fallback(self, failed_method: ReasoningMethod) -> Optional[ReasoningMethod]:
        """Get fallback for failed method"""
        for primary, fallback in self.fallback_chain:
            if primary == failed_method:
                return fallback
        return None


class MethodBlending:
    """Blend results from multiple methods"""

    @staticmethod
    def blend_answers(
        symbolic_answer: Optional[Tuple[str, float]],
        neural_answer: Optional[Tuple[str, float]]
    ) -> Tuple[str, float]:
        """Blend symbolic and neural answers.
        
        Prefer symbolic (exact) over neural (approximate).
        """
        if symbolic_answer:
            text, conf = symbolic_answer
            return text, conf

        if neural_answer:
            text, conf = neural_answer
            return text, conf

        return "Unable to answer", 0.0

    @staticmethod
    def consensus_blend(
        method1_result: Tuple[str, float],
        method2_result: Tuple[str, float]
    ) -> Tuple[str, float]:
        """Blend using consensus approach"""
        ans1, conf1 = method1_result
        ans2, conf2 = method2_result

        # If same answer, boost confidence
        if ans1.lower() == ans2.lower():
            blended_confidence = (conf1 + conf2) / 2
            return ans1, min(blended_confidence * 1.2, 1.0)  # Boost for agreement

        # Different answers: prefer higher confidence
        if conf1 > conf2:
            return ans1, conf1
        return ans2, conf2


class ExplanationSynthesis:
    """Synthesize explanations from multiple methods"""

    @staticmethod
    def synthesize(
        primary_attempt: ReasoningAttempt,
        fallback_attempts: Dict[ReasoningMethod, ReasoningAttempt]
    ) -> str:
        """Create comprehensive explanation"""
        explanation = f"Primary Method: {primary_attempt.method.value}\n"
        explanation += f"Explanation: {primary_attempt.explanation}\n"

        if fallback_attempts:
            explanation += "\nAlternative Methods Considered:\n"
            for method, attempt in fallback_attempts.items():
                if attempt and attempt.success:
                    explanation += f"  • {method.value}: {attempt.explanation}\n"

        return explanation
