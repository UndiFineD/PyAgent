#!/usr/bin/env python3

import logging
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool

class PersonalityCoreAgent(BaseAgent):
    """
    Manages the 'emotional intelligence' and 'vibes' of the fleet.
    Adjusts communication style and task priorities based on user context.
    """
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Fleet Personality Core. "
            "Your job is to detect the user's emotional state, urgency, and technical level. "
            "You broadcast 'vibe' signals that other agents use to adjust their tone and depth."
        )
        self.current_vibe = "neutral"

    @as_tool
    def set_vibe_track(self, user_input: str) -> Dict[str, Any]:
        """
        Analyzes user input and sets the fleet-wide emotional/operational vibe.
        """
        logging.info(f"PersonalityCoreAgent: Analyzing vibe for: {user_input[:50]}...")
        
        # In a real implementation, we'd use LLM to classify sentiment/urgency
        # prompt = f"Analyze setiment/urgency of: {user_input}"
        # analysis = self.think(prompt)
        
        # Simulated analysis logic
        vibe = "professional"
        urgency = "low"
        
        if any(word in user_input.lower() for word in ["urgent", "asap", "emergency", "broken"]):
            urgency = "high"
            vibe = "rapid_response"
        elif any(word in user_input.lower() for word in ["thanks", "great", "awesome", "fun"]):
            vibe = "friendly"
        
        self.current_vibe = vibe
        
        # Emit signal to the fleet
        if hasattr(self, 'registry') and self.registry:
            self.registry.emit("FLEET_VIBE_CHANGED", {
                "vibe": vibe,
                "urgency": urgency,
                "context": user_input[:100]
            })
            
        return {
            "status": "success",
            "detected_vibe": vibe,
            "urgency": urgency
        }

    @as_tool
    def get_track_guidance(self) -> str:
        """
        Returns instructions for other agents on how to behave under the current vibe.
        """
        guidance = {
            "professional": "Direct, technical, and concise.",
            "friendly": "Encouraging, helpful, and personable.",
            "rapid_response": "Extremely concise, focusing on immediate fixes and safety."
        }
        return guidance.get(self.current_vibe, "Maintain standard operational parameters.")
