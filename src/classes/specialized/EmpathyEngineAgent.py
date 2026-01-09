import json
import logging
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent

class EmpathyEngineAgent(BaseAgent):
    """
    Phase 61: Emotional Intelligence & Soft-Skill Synthesis.
    Analyzes user sentiment and adjusts agent linguistic "tone" for better HITL collaboration.
    """
    
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.sentiment_state = "neutral"
        self.empathy_score = 1.0

    def analyze_user_sentiment(self, message: str) -> Dict[str, Any]:
        """Simple keyword-based sentiment analysis."""
        positive = ["thanks", "good", "great", "helpful", "perfect", "love"]
        negative = ["error", "bad", "useless", "wrong", "fix", "stop"]
        
        pos_count = sum(1 for w in positive if w in message.lower())
        neg_count = sum(1 for w in negative if w in message.lower())
        
        if pos_count > neg_count:
            self.sentiment_state = "positive"
        elif neg_count > pos_count:
            self.sentiment_state = "frustrated"
        else:
            self.sentiment_state = "neutral"
            
        return {
            "sentiment": self.sentiment_state,
            "confidence": 0.75,
            "linguistic_adjustment": self.get_tone_recommendation()
        }

    def get_tone_recommendation(self) -> str:
        """Determines the linguistic style to adopt based on sentiment."""
        if self.sentiment_state == "frustrated":
            return "concise_and_apologetic"
        elif self.sentiment_state == "positive":
            return "enthusiastic_and_detailed"
        return "professional_neutral"

    def mediate_conflict(self, agent_id: str, human_refusal: str) -> str:
        """Generates a soft-skill response to resolve disagreements."""
        logging.info(f"EmpathyEngine: Mediating conflict between {agent_id} and User.")
        
        prompt = (
            f"The agent {agent_id} proposed a change, but the user refused saying: '{human_refusal}'. "
            "Generate a supportive, non-confrontational response that acknowledges the user's concern "
            "and explores alternative solutions."
        )
        
        # In a real scenario, this would use self.think()
        return "I understand your concern. Let's look at this from a different angle to ensure we meet your requirements safely."
