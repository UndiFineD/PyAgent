# Extracted from: C:\DEV\PyAgent\.external\skills\skills\idanmann10\startclaw-optimizer\scripts\router.py
#!/usr/bin/env python3
"""
Task Router - Classify complexity and route to appropriate models/strategies.
"""

import json
import re
from enum import Enum
from typing import Optional, Tuple


class Complexity(Enum):
    LOW = "low"  # Haiku, single-phase
    MED = "medium"  # Haiku gather → Sonnet finalize
    HIGH = "high"  # Sonnet, might need sub-agents


class Strategy(Enum):
    DIRECT = "direct"  # Single model, single pass
    GATHER_WRITE = "gather_write"  # Two-phase: Haiku → Sonnet
    SPAWN = "spawn"  # Use sub-agent (isolated session)


class TaskRouter:
    # Haiku-only patterns (LOW complexity)
    HAIKU_PATTERNS = [
        r"\b(what|where|when|who)\b",  # Questions
        r"\b(list|show|get|find)\b",  # Lookups
        r"\b(click|navigate|scroll|snapshot)\b",  # Browser commands
        r"\b(extract|scrape|parse)\b",  # Data extraction
        r"\bheartbeat\b",  # Heartbeat checks
        r"\bformat\b",  # Simple formatting
        r"\bstatus\b",  # Status checks
    ]

    # Sonnet-required patterns (HIGH complexity)
    SONNET_PATTERNS = [
        r"\b(analyze|compare|evaluate)\b",  # Analysis
        r"\b(write|draft|compose)\b.*\b(tweet|post|comment|reply|article)\b",  # Writing
        r"\b(plan|strategy|design)\b",  # Planning
        r"\b(debug|fix|solve)\b",  # Problem solving
        r"\bcode\b.*\b(function|class|script)\b",  # Coding
        r"\b(summarize|explain)\b.*\b(document|article)\b",  # Deep summarization
    ]

    # Gather-write patterns (MED complexity)
    GATHER_WRITE_PATTERNS = [
        r"find.*write",  # Find X, then write about it
        r"search.*post",  # Search, then post
        r"scrape.*reply",  # Scrape, then reply
        r"navigate.*comment",  # Navigate, then comment
    ]

    def classify(self, task: str) -> Tuple[Complexity, Strategy, str]:
        """
        Classify a task and return (complexity, strategy, reasoning).
        """
        task_lower = task.lower()

        # Check for gather-write pattern first (MED)
        for pattern in self.GATHER_WRITE_PATTERNS:
            if re.search(pattern, task_lower):
                return (
                    Complexity.MED,
                    Strategy.GATHER_WRITE,
                    f"Matched gather-write pattern: {pattern}",
                )

        # Check for Sonnet-required patterns (HIGH)
        for pattern in self.SONNET_PATTERNS:
            if re.search(pattern, task_lower):
                # If also involves browser, suggest gather-write
                if re.search(r"\b(navigate|browser|click|search)\b", task_lower):
                    return (
                        Complexity.MED,
                        Strategy.GATHER_WRITE,
                        f"Writing task with navigation: Haiku gather → Sonnet write",
                    )
                return (
                    Complexity.HIGH,
                    Strategy.DIRECT,
                    f"Matched complex pattern: {pattern}",
                )

        # Check for Haiku-only patterns (LOW)
        for pattern in self.HAIKU_PATTERNS:
            if re.search(pattern, task_lower):
                return (
                    Complexity.LOW,
                    Strategy.DIRECT,
                    f"Matched simple pattern: {pattern}",
                )

        # Check task length (long tasks → higher complexity)
        if len(task) > 500:
            return (
                Complexity.HIGH,
                Strategy.DIRECT,
                "Long task description suggests complexity",
            )

        # Default: LOW complexity
        return (
            Complexity.LOW,
            Strategy.DIRECT,
            "No clear complexity markers - defaulting to LOW",
        )

    def recommend_model(self, complexity: Complexity, phase: Optional[str] = None) -> str:
        """
        Recommend model based on complexity and phase.
        """
        if complexity == Complexity.LOW:
            return "anthropic/claude-3-5-haiku-latest"

        if complexity == Complexity.MED:
            if phase == "gather":
                return "anthropic/claude-3-5-haiku-latest"
            elif phase == "write":
                return "anthropic/claude-sonnet-4-5"
            # Default to Sonnet if phase unknown
            return "anthropic/claude-sonnet-4-5"

        if complexity == Complexity.HIGH:
            return "anthropic/claude-sonnet-4-5"

        return "anthropic/claude-3-5-haiku-latest"

    def should_spawn(self, task: str, complexity: Complexity) -> bool:
        """
        Decide if task should be spawned to sub-agent.
        """
        # Spawn if explicitly requested
        if re.search(r"\b(spawn|isolate|separate)\b", task.lower()):
            return True

        # Spawn for automation (isolated execution)
        if re.search(r"\b(cron|automation|scheduled)\b", task.lower()):
            return True

        # Don't spawn for simple tasks
        if complexity == Complexity.LOW:
            return False

        # Spawn for very long tasks
        if len(task) > 1000:
            return True

        return False


if __name__ == "__main__":
    import sys

    router = TaskRouter()

    if len(sys.argv) < 2:
        print("Usage: router.py <task>")
        print("\nExamples:")
        print("  router.py 'Find openclaw tweets and reply'")
        print("  router.py 'What is the weather?'")
        print("  router.py 'Analyze this codebase and write a report'")
        sys.exit(1)

    task = " ".join(sys.argv[1:])
    complexity, strategy, reasoning = router.classify(task)

    print(f"Task: {task}")
    print(f"\nComplexity: {complexity.value}")
    print(f"Strategy: {strategy.value}")
    print(f"Reasoning: {reasoning}")

    if strategy == Strategy.GATHER_WRITE:
        gather_model = router.recommend_model(complexity, "gather")
        write_model = router.recommend_model(complexity, "write")
        print(f"\nPhase 1 (gather): {gather_model}")
        print(f"Phase 2 (write): {write_model}")
    else:
        model = router.recommend_model(complexity)
        print(f"\nRecommended model: {model}")

    should_spawn = router.should_spawn(task, complexity)
    print(f"Spawn sub-agent: {should_spawn}")
