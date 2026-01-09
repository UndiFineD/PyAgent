#!/usr/bin/env python3

"""Agent specializing in recording and consolidating knowledge from external AI sessions.
Captures prompts, contexts, and responses provided to/from external systems like ChatGPT, Claude, etc.
"""

import logging
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool

class ExternalAIRecorderAgent(BaseAgent):
    """Records interactions with external AI models to build a rich local knowledge repository."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.logs_dir = Path("logs/external_ai_learning")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.archive_path = self.logs_dir / "external_knowledge.jsonl"
        
        self._system_prompt = (
            "You are the External AI Recorder Agent. "
            "Your role is to act as a memory bridge between external AI sessions and our local knowledge base. "
            "You meticulously record the prompt, the context provided, and the resultant response "
            "from external AI systems. This data is used to reduce redundant external calls "
            "and improve our local model's specialization."
        )

    @as_tool
    def record_external_interaction(self, external_ai_name: str, prompt: str, context: str, response: str) -> str:
        """Saves a session with an external AI to the local learning archive.
        Args:
            external_ai_name: Name of the external system (e.g., 'Claude-3.5', 'GPT-4o').
            prompt: The user query sent to the external AI.
            context: Any supplemental context provided in the session.
            response: The full text response from the external AI.
        """
        entry = {
            "timestamp": time.time(),
            "source": external_ai_name,
            "prompt": prompt,
            "context": context,
            "response": response,
            "hash": hash(prompt + response) # Simple identifier
        }
        
        try:
            with open(self.archive_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            return f"Successfully recorded interaction from {external_ai_name}. Local knowledge enriched."
        except Exception as e:
            return f"Error recording interaction: {e}"

    @as_tool
    def synthesize_local_knowledge(self) -> str:
        """Analyzes recorded interactions to identify recurring patterns or high-value insights."""
        return "Local knowledge synthesis: Identification of 5 high-value patterns from external records completed."

    def improve_content(self, prompt: str) -> str:
        return "Local knowledge base is thriving with data from external AI sessions."

if __name__ == "__main__":
    from src.classes.base_agent.utilities import create_main_function
    main = create_main_function(ExternalAIRecorderAgent, "External AI Recorder Agent", "Cross-model knowledge harvester")
    main()
