"""Explainability & Interpretability Layer

Makes model decisions understandable through:
- Reasoning trace visualization
- Attribution analysis
- Counterfactual explanations
- Natural language explanations
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Explanation:
    """A model explanation"""

    original: str
    prediction: str
    confidence: float
    explanation_text: str
    important_factors: List[Tuple[str, float]]  # (factor, importance)
    explanation_type: str  # "reasoning", "attribution", "counterfactual"


class ReasoningTraceExplainer:
    """Generate reasoning traces"""

    @staticmethod
    def generate_trace(steps: List[str], answer: str) -> Dict:
        """Generate readable reasoning trace
        
        Args:
            steps: Reasoning steps
            answer: Final answer
            
        Returns:
            Dict with formatted trace

        """
        trace = {
            'steps': [],
            'answer': answer,
            'summary': ''
        }

        for i, step in enumerate(steps, 1):
            trace['steps'].append({
                'number': i,
                'description': step,
                'type': ReasoningTraceExplainer._classify_step_type(step)
            })

        # Generate summary
        if steps:
            trace['summary'] = f"Reasoning chain with {len(steps)} steps leading to: {answer}"

        return trace

    @staticmethod
    def _classify_step_type(step: str) -> str:
        """Classify type of reasoning step"""
        step_lower = step.lower()

        if any(word in step_lower for word in ['calculate', 'compute', 'add', 'multiply']):
            return 'calculation'
        elif any(word in step_lower for word in ['therefore', 'thus', 'so', 'conclude']):
            return 'conclusion'
        elif any(word in step_lower for word in ['check', 'verify', 'confirm']):
            return 'verification'
        elif any(word in step_lower for word in ['assume', 'suppose', 'given']):
            return 'assumption'
        else:
            return 'intermediate'

    @staticmethod
    def trace_to_text(trace: Dict) -> str:
        """Convert trace to natural language explanation"""
        lines = ["Here's how I arrived at this answer:\n"]

        for step_info in trace['steps']:
            lines.append(f"Step {step_info['number']}: {step_info['description']}")

        lines.append(f"\nTherefore: {trace['answer']}")

        return '\n'.join(lines)


class AttributionExplainer:
    """Attribution-based explanations"""

    @staticmethod
    def identify_important_tokens(text: str, attention_weights: Optional[List[float]] = None) -> List[Tuple[str, float]]:
        """Identify important tokens in input
        
        Args:
            text: Input text
            attention_weights: Optional attention weights
            
        Returns:
            List of (token, importance) tuples

        """
        tokens = text.split()

        if attention_weights is None:
            # Simple heuristic: important words are longer, not stop words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'is', 'are', 'was', 'were', 'be', 'been'}

            importance_scores = []
            for token in tokens:
                score = 0.0

                # Length factor
                score += min(1.0, len(token) / 10.0)

                # Not a stop word
                if token.lower() not in stop_words:
                    score += 0.5

                # Capitalized (likely named entity)
                if token[0].isupper():
                    score += 0.3

                importance_scores.append(score)
        else:
            importance_scores = attention_weights

        # Normalize
        max_score = max(importance_scores) if importance_scores else 1.0
        normalized_scores = [s / max_score for s in importance_scores]

        return list(zip(tokens, normalized_scores))

    @staticmethod
    def generate_attribution_explanation(text: str, prediction: str,
                                        important_tokens: List[Tuple[str, float]]) -> str:
        """Generate attribution-based explanation
        
        Args:
            text: Input text
            prediction: Model prediction
            important_tokens: Important tokens
            
        Returns:
            Explanation text

        """
        # Sort by importance
        important = sorted(important_tokens, key=lambda x: x[1], reverse=True)[:5]
        important_words = [word for word, _ in important]

        explanation = f"The prediction '{prediction}' is based on these key phrases: {', '.join(important_words)}."

        return explanation


class CounterfactualExplainer:
    """Counterfactual explanations"""

    def __init__(self, model=None):
        """Initialize counterfactual explainer"""
        self.model = model

    def generate_counterfactual(self, text: str, original_prediction: str) -> Optional[Dict]:
        """Generate counterfactual (minimal change that changes prediction)
        
        Args:
            text: Input text
            original_prediction: Original model prediction
            
        Returns:
            Dict with counterfactual or None if not found

        """
        tokens = text.split()

        # Try replacing each token
        for i, token in enumerate(tokens):
            alternatives = self._get_alternatives(token)

            for alt in alternatives:
                # Create counterfactual
                modified_tokens = tokens.copy()
                modified_tokens[i] = alt
                modified_text = ' '.join(modified_tokens)

                # Get new prediction
                if self.model:
                    new_prediction = self.model.predict(modified_text)
                else:
                    # Simulate
                    new_prediction = f"predicted_{i}"

                # Check if prediction changed
                if new_prediction != original_prediction:
                    return {
                        'original': text,
                        'counterfactual': modified_text,
                        'original_prediction': original_prediction,
                        'counterfactual_prediction': new_prediction,
                        'changed_token': token,
                        'changed_to': alt,
                        'explanation': f"Changing '{token}' to '{alt}' changes prediction "
                                      f"from '{original_prediction}' to '{new_prediction}'"
                    }

        return None

    @staticmethod
    def _get_alternatives(token: str) -> List[str]:
        """Get alternative tokens"""
        # Simple: antonyms, opposites
        opposites = {
            'good': 'bad',
            'bad': 'good',
            'yes': 'no',
            'no': 'yes',
            'true': 'false',
            'false': 'true',
            'positive': 'negative',
            'negative': 'positive',
        }

        alternatives = []

        if token.lower() in opposites:
            alternatives.append(opposites[token.lower()])

        # Remove adjectives if present
        if token.endswith('ly'):
            alternatives.append(token[:-2])

        return alternatives[:3]


class ConfidenceExplainer:
    """Explain confidence scores"""

    @staticmethod
    def explain_low_confidence(confidence: float, reasoning_steps: List[str]) -> str:
        """Explain why confidence is low
        
        Args:
            confidence: Confidence score
            reasoning_steps: Reasoning steps
            
        Returns:
            Explanation text

        """
        reasons = []

        # Few steps
        if len(reasoning_steps) < 2:
            reasons.append("limited reasoning steps")

        # Short steps
        short_steps = sum(1 for s in reasoning_steps if len(s.split()) < 5)
        if short_steps > len(reasoning_steps) / 2:
            reasons.append("brief reasoning steps")

        # Uncertain language
        uncertain_words = ['maybe', 'perhaps', 'might', 'could', 'possibly']
        uncertain_count = sum(1 for s in reasoning_steps
                            for word in uncertain_words if word in s.lower())
        if uncertain_count > 0:
            reasons.append("use of uncertain language")

        if reasons:
            return f"Low confidence ({confidence:.1%}) due to: {', '.join(reasons)}"
        else:
            return f"Confidence is {confidence:.1%}"

    @staticmethod
    def explain_high_confidence(confidence: float, reasoning_steps: List[str]) -> str:
        """Explain why confidence is high
        
        Args:
            confidence: Confidence score
            reasoning_steps: Reasoning steps
            
        Returns:
            Explanation text

        """
        reasons = []

        # Multiple steps
        if len(reasoning_steps) >= 3:
            reasons.append("thorough reasoning")

        # Confident language
        confident_words = ['clearly', 'obviously', 'definitely', 'certainly', 'must']
        confident_count = sum(1 for s in reasoning_steps
                            for word in confident_words if word in s.lower())
        if confident_count > 0:
            reasons.append("use of confident language")

        # Verification steps
        if any('verify' in s.lower() or 'check' in s.lower() for s in reasoning_steps):
            reasons.append("verification of answer")

        if reasons:
            return f"High confidence ({confidence:.1%}) due to: {', '.join(reasons)}"
        else:
            return f"Confidence is {confidence:.1%}"


class ExplainabilityLayer:
    """Main explainability interface"""

    def __init__(self, model=None):
        """Initialize explainability layer"""
        self.model = model
        self.trace_explainer = ReasoningTraceExplainer()
        self.attribution_explainer = AttributionExplainer()
        self.counterfactual_explainer = CounterfactualExplainer(model)
        self.confidence_explainer = ConfidenceExplainer()

    def explain_prediction(self, text: str, prediction: str,
                          reasoning_steps: List[str] = None,
                          confidence: float = 0.5) -> Explanation:
        """Generate comprehensive explanation
        
        Args:
            text: Input text
            prediction: Model prediction
            reasoning_steps: Steps that led to prediction
            confidence: Confidence in prediction
            
        Returns:
            Explanation object

        """
        # Reasoning trace explanation
        if reasoning_steps:
            trace = self.trace_explainer.generate_trace(reasoning_steps, prediction)
            explanation_text = self.trace_explainer.trace_to_text(trace)
        else:
            explanation_text = f"Predicted: {prediction}"

        # Important factors (attribution)
        important_factors = self.attribution_explainer.identify_important_tokens(text)

        # Add confidence explanation
        if confidence < 0.5:
            conf_explanation = self.confidence_explainer.explain_low_confidence(confidence, reasoning_steps or [])
        else:
            conf_explanation = self.confidence_explainer.explain_high_confidence(confidence, reasoning_steps or [])

        explanation_text += f"\n\n{conf_explanation}"

        return Explanation(
            original=text,
            prediction=prediction,
            confidence=confidence,
            explanation_text=explanation_text,
            important_factors=important_factors,
            explanation_type="reasoning"
        )

    def explain_decision(self, text: str, decision: str) -> str:
        """Generate natural language decision explanation
        
        Args:
            text: Input context
            decision: Decision made
            
        Returns:
            Explanation text

        """
        return f"Based on '{text}', the decision is '{decision}'."


# Example usage
if __name__ == "__main__":
    # Reasoning trace
    steps = [
        "Sarah starts with 3 apples",
        "She buys 2 more apples",
        "So she has 3 + 2 = 5 apples"
    ]

    trace = ReasoningTraceExplainer.generate_trace(steps, "5 apples")
    print(ReasoningTraceExplainer.trace_to_text(trace))

    # Attribution
    text = "This movie is absolutely amazing and wonderful"
    important = AttributionExplainer.identify_important_tokens(text)
    print(f"\nImportant tokens: {important}")

    # Confidence explanation
    conf_explain = ConfidenceExplainer.explain_high_confidence(0.95, steps)
    print(f"\n{conf_explain}")
