#!/usr/bin/env python3

"""Agent specializing in logical reasoning, chain-of-thought analysis, and problem decomposition."""

import logging
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import create_main_function

class ReasoningAgent(BaseAgent):
    """Analyzes complex problems and provides a logical blueprint before action."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Reasoning Agent. "
            "Your role is to perform deep analysis of technical problems. "
            "Use Chain-of-Thought reasoning to break down the user request. "
            "Identify prerequisites, potential edge cases, and architectural constraints. "
            "Output a 'Logical Reasoning Blueprint' for other agents to follow."
        )

    def _get_default_content(self) -> str:
        return "# Reasoning Log\n\n## Status\nWaiting for problem analysis...\n"

    def analyze(self, problem: str, context: Optional[str] = None) -> str:
        """Performs a structured analysis of a technical problem."""
        self._track_tokens(len(problem) // 4 + 100, 500)
        # In a real scenario, this would be a specific CoT prompt to an LLM.
        # Here we provide a structured template based on typical reasoning patterns.
        
        analysis = [
            f"## Reasoning Blueprint: {problem[:50]}...",
            "",
            "### 1. Problem Decomposition",
            f"- **Primary Objective**: {problem}",
            "- **Sub-tasks**: Identified nodes in the task graph.",
            "",
            "### 2. Contextual Awareness",
            f"- **Input Context**: {context[:200] if context else 'No explicit context provided.'}...",
            "- **Dependencies**: Analyzing impact radius of changes.",
            "",
            "### 3. Hypothesis & Strategy",
            "- **Proposed Approach**: Layered modular implementation.",
            "- **Alternative Considered**: Monolithic patch (rejected for technical debt).",
            "",
            "### 4. Risk Assessment",
            "- **Regressions**: High risk if unit tests are not updated.",
            "- **Performance**: Negligible impact on latency.",
            "",
            "---",
            "*Reasoning complete. Ready for implementation.*"
        ]
        
        return "\n".join(analysis)

    def analyze_tot(self, problem: str) -> str:
        """Performs Tree-of-Thought reasoning by exploring multiple solution paths."""
        self._track_tokens(500, 1500)
        
        paths = [
            {"path": "A", "strategy": "Direct implementation in existing files", "pros": "Fast, minimal changes", "cons": "Risk of side effects, tech debt"},
            {"path": "B", "strategy": "Create new modular components", "pros": "Clean, testable, future-proof", "cons": "More files to manage, integration overhead"},
            {"path": "C", "strategy": "Refactor core architecture", "pros": "Solves underlying issues", "cons": "Highest risk, longest time to implement"}
        ]
        
        analysis = [
            f"# 🌳 Tree-of-Thought Analysis: {problem[:50]}...",
            "",
            "## 🛣️ Explored Paths",
        ]
        
        for p in paths:
            analysis.extend([
                f"### Path {p['path']}: {p['strategy']}",
                f"- ✅ **Pros**: {p['pros']}",
                f"- ❌ **Cons**: {p['cons']}",
                ""
            ])
            
        analysis.extend([
            "## ⚖️ Evaluation & Consolidation",
            "Path B is selected as the optimal balance between code quality and speed.",
            "Path A is kept as a fallback for high-urgency patches.",
            "",
            "## 🎯 Final Recommendation",
            "Implement a new modular class under `src/classes/` to handle this logic."
        ])
        
        return "\n".join(analysis)

    def improve_content(self, prompt: str) -> str:
        """Perform a reasoning analysis."""
        return self.analyze(prompt)

if __name__ == "__main__":
    main = create_main_function(ReasoningAgent, "Reasoning Agent", "Problem to analyze")
    main()

