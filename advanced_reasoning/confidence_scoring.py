#!/usr/bin/env python3
"""Confidence Scoring & Uncertainty Quantification

Measures model certainty across:
- Token-level confidence
- Step-level confidence  
- Answer-level confidence
- Semantic confidence
"""

from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np


@dataclass
class ConfidenceMetrics:
    """Confidence measurements for a prediction"""

    token_confidences: List[float]
    avg_token_confidence: float
    step_confidence: float
    answer_confidence: float
    semantic_confidence: float
    overall_confidence: float
    calibration_score: float  # 0-1, higher = better calibrated


class TokenConfidenceScorer:
    """Score confidence for individual tokens"""

    @staticmethod
    def from_logits(logits: np.ndarray) -> List[float]:
        """Compute token confidence from logits using softmax

        Args:
            logits: Shape (num_tokens, vocab_size)

        Returns:
            List of confidence scores (0-1)

        """
        confidences = []

        for token_logits in logits:
            # Softmax to get probabilities
            exp_logits = np.exp(token_logits - np.max(token_logits))
            probs = exp_logits / np.sum(exp_logits)

            # Confidence = max probability
            confidence = np.max(probs)
            confidences.append(float(confidence))

        return confidences

    @staticmethod
    def from_entropy(logits: np.ndarray) -> List[float]:
        """Compute token confidence using entropy (inverted)

        Low entropy = high confidence
        High entropy = low confidence

        Args:
            logits: Shape (num_tokens, vocab_size)

        Returns:
            List of confidence scores (0-1)

        """
        confidences = []

        for token_logits in logits:
            # Softmax
            exp_logits = np.exp(token_logits - np.max(token_logits))
            probs = exp_logits / np.sum(exp_logits)

            # Entropy
            entropy = -np.sum(probs * np.log(probs + 1e-10))
            max_entropy = np.log(len(probs))

            # Convert to confidence (invert)
            confidence = 1.0 - (entropy / max_entropy)
            confidences.append(float(confidence))

        return confidences


class StepConfidenceScorer:
    """Score confidence for reasoning steps"""

    @staticmethod
    def score_step_validity(step: str, previous_steps: List[str]) -> float:
        """Score how valid a reasoning step is

        Factors:
        - Step length (too short = less confident)
        - Coherence with previous steps
        - Presence of markers (therefore, thus, etc)

        Args:
            step: The reasoning step
            previous_steps: Previous steps for context

        Returns:
            Confidence score (0-1)

        """
        score = 0.0

        # Length factor: prefer substantial steps
        if len(step.split()) < 3:
            score += 0.2
        elif len(step.split()) < 10:
            score += 0.5
        else:
            score += 0.8

        # Coherence: does step reference previous?
        if previous_steps:
            step_lower = step.lower()
            prev_lower = ' '.join(previous_steps).lower()

            # Check for pronouns and references
            if any(ref in step_lower for ref in ['above', 'previous', 'this', 'that']):
                score += 0.1

            # Check for logical connectors
            if any(conn in step_lower for conn in ['therefore', 'thus', 'so', 'because']):
                score += 0.1

        # Confidence markers
        confident_words = ['clearly', 'obviously', 'definitely', 'certainly', 'must be']
        uncertain_words = ['maybe', 'perhaps', 'might', 'could', 'possibly']

        for word in confident_words:
            if word in step.lower():
                score += 0.05

        for word in uncertain_words:
            if word in step.lower():
                score -= 0.05

        return max(0.0, min(1.0, score))

    @staticmethod
    def score_calculation_step(step: str) -> float:
        """Score confidence in a calculation step
        
        Args:
            step: The step containing calculation
            
        Returns:
            Confidence score (0-1)

        """
        score = 0.0

        # Check for explicit numbers
        import re
        numbers = re.findall(r'\d+\.?\d*', step)
        if numbers:
            score += 0.3

        # Check for mathematical operators
        operators = ['+', '-', '*', '/', '=', '%']
        operator_count = sum(1 for op in operators if op in step)
        score += min(0.3, operator_count * 0.1)

        # Check for explicit result
        if '=' in step or 'result' in step.lower():
            score += 0.3

        return min(1.0, score)


class AnswerConfidenceScorer:
    """Score confidence in final answers"""

    @staticmethod
    def from_self_consistency(answers: List[str]) -> float:
        """Score answer confidence based on agreement
        
        If all paths agree = high confidence
        If paths disagree = low confidence
        
        Args:
            answers: Answers from multiple reasoning paths
            
        Returns:
            Confidence score (0-1)

        """
        if not answers:
            return 0.0

        if len(answers) == 1:
            return 0.8  # Single path, moderate confidence

        # Count agreement
        answer_counts = Counter(answers)
        most_common_count = answer_counts.most_common(1)[0][1]

        agreement = most_common_count / len(answers)

        return float(agreement)

    @staticmethod
    def from_semantic_support(answer: str, reasoning_steps: List[str]) -> float:
        """Score how well reasoning supports the answer
        
        Args:
            answer: The proposed answer
            reasoning_steps: Steps that led to answer
            
        Returns:
            Confidence score (0-1)

        """
        score = 0.0

        # Is answer mentioned in reasoning?
        reasoning_text = ' '.join(reasoning_steps).lower()
        if answer.lower() in reasoning_text:
            score += 0.4

        # Multi-step reasoning
        if len(reasoning_steps) >= 3:
            score += 0.3
        elif len(reasoning_steps) >= 2:
            score += 0.2

        # Check for conclusion markers
        conclusion_markers = ['therefore', 'thus', 'so', 'finally', 'answer', 'result']
        for step in reasoning_steps:
            if any(marker in step.lower() for marker in conclusion_markers):
                score += 0.2
                break

        # Quality of final step
        if reasoning_steps:
            final_step = reasoning_steps[-1].lower()
            if len(final_step.split()) >= 5:  # Substantial final step
                score += 0.1

        return min(1.0, score)


class CalibrationScorer:
    """Score how well-calibrated predictions are"""

    @staticmethod
    def compute_ece(confidences: np.ndarray, accuracies: np.ndarray,
                   num_bins: int = 10) -> float:
        """Compute Expected Calibration Error (ECE)
        
        Lower ECE = better calibration
        
        Args:
            confidences: Predicted confidence scores
            accuracies: Whether prediction was correct (0 or 1)
            num_bins: Number of bins for calibration curve
            
        Returns:
            ECE score (0-1)

        """
        bins = np.linspace(0, 1, num_bins + 1)
        ece = 0.0

        for i in range(num_bins):
            mask = (confidences >= bins[i]) & (confidences < bins[i+1])

            if np.sum(mask) > 0:
                avg_conf = np.mean(confidences[mask])
                avg_acc = np.mean(accuracies[mask])
                weight = np.sum(mask) / len(confidences)

                ece += np.abs(avg_conf - avg_acc) * weight

        return float(ece)

    @staticmethod
    def compute_mce(confidences: np.ndarray, accuracies: np.ndarray,
                   num_bins: int = 10) -> float:
        """Compute Maximum Calibration Error (MCE)
        
        Maximum difference between confidence and accuracy in any bin
        
        Args:
            confidences: Predicted confidence scores
            accuracies: Whether prediction was correct (0 or 1)
            num_bins: Number of bins for calibration curve
            
        Returns:
            MCE score (0-1)

        """
        bins = np.linspace(0, 1, num_bins + 1)
        max_error = 0.0

        for i in range(num_bins):
            mask = (confidences >= bins[i]) & (confidences < bins[i+1])

            if np.sum(mask) > 0:
                avg_conf = np.mean(confidences[mask])
                avg_acc = np.mean(accuracies[mask])
                error = np.abs(avg_conf - avg_acc)
                max_error = max(max_error, error)

        return float(max_error)

    @staticmethod
    def compute_brier_score(confidences: np.ndarray, accuracies: np.ndarray) -> float:
        """Compute Brier Score
        
        Mean squared error between confidence and accuracy
        
        Args:
            confidences: Predicted confidence scores
            accuracies: Whether prediction was correct (0 or 1)
            
        Returns:
            Brier score (0-1)

        """
        return float(np.mean((confidences - accuracies) ** 2))


class ConfidenceScorer:
    """Main confidence scoring interface"""

    def __init__(self, model=None):
        """Initialize confidence scorer"""
        self.model = model
        self.token_scorer = TokenConfidenceScorer()
        self.step_scorer = StepConfidenceScorer()
        self.answer_scorer = AnswerConfidenceScorer()
        self.calibration_scorer = CalibrationScorer()

    def score_reasoning(self, reasoning_result: Dict) -> ConfidenceMetrics:
        """Score confidence for complete reasoning result
        
        Args:
            reasoning_result: Result from chain_of_thought generator
            
        Returns:
            ConfidenceMetrics with all scores

        """
        steps = reasoning_result.get('steps', [])
        answer = reasoning_result.get('answer', '')

        # Score individual steps
        step_scores = []
        for i, step in enumerate(steps):
            prev_steps = steps[:i]
            score = self.step_scorer.score_step_validity(step, prev_steps)
            step_scores.append(score)

        avg_token_confidence = np.mean(step_scores) if step_scores else 0.5
        step_confidence = np.mean(step_scores) if step_scores else 0.5

        # Score answer
        answer_confidence = self.answer_scorer.from_semantic_support(answer, steps)

        # Score semantic support
        semantic_confidence = answer_confidence

        # Overall confidence
        overall_confidence = np.mean([
            avg_token_confidence,
            step_confidence,
            answer_confidence,
            semantic_confidence
        ])

        return ConfidenceMetrics(
            token_confidences=step_scores,
            avg_token_confidence=float(avg_token_confidence),
            step_confidence=float(step_confidence),
            answer_confidence=float(answer_confidence),
            semantic_confidence=float(semantic_confidence),
            overall_confidence=float(overall_confidence),
            calibration_score=0.5  # Placeholder
        )

    def reason_with_confidence(self, query: str) -> Dict:
        """Generate reasoning and score confidence
        
        Args:
            query: Question to reason about
            
        Returns:
            Dict with reasoning, answer, and confidence

        """
        if self.model is None:
            return {
                'query': query,
                'answer': 'Model not available',
                'confidence': 0.0
            }

        # Generate reasoning (would use actual model)
        result = {
            'steps': [],
            'answer': '',
        }

        # Score confidence
        metrics = self.score_reasoning(result)

        return {
            'query': query,
            'steps': result.get('steps', []),
            'answer': result.get('answer', ''),
            'confidence': metrics.overall_confidence,
            'metrics': metrics
        }


# Example usage
if __name__ == "__main__":
    # Example logits
    logits = np.array([
        [1.0, 2.5, 0.5, 0.2],
        [0.3, 0.1, 2.8, 0.5],
        [1.2, 0.5, 0.3, 0.9]
    ])

    # Score from logits
    token_scorer = TokenConfidenceScorer()
    confidences = token_scorer.from_logits(logits)
    print(f"Token confidences: {confidences}")

    # Self-consistency
    answers = ["42", "42", "41"]
    answer_conf = AnswerConfidenceScorer.from_self_consistency(answers)
    print(f"Answer confidence (agreement): {answer_conf:.2f}")

    # Calibration
    confidences_arr = np.array([0.9, 0.8, 0.7, 0.6, 0.5])
    accuracies_arr = np.array([1.0, 1.0, 0.0, 0.0, 1.0])

    ece = CalibrationScorer.compute_ece(confidences_arr, accuracies_arr)
    print(f"Expected Calibration Error: {ece:.3f}")
