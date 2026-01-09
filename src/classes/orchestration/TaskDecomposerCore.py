from typing import List, Dict, Any

class TaskDecomposerCore:
    """
    Pure logic for task decomposition.
    Handles heuristic-based planning and plan summarization.
    """

    def generate_plan(self, request: str) -> List[Dict[str, Any]]:
        """Core planning logic."""
        request_lower = request.lower()
        steps = []
        
        # Heuristic rules
        if "analyze" in request_lower or "data" in request_lower:
            steps.append({"agent": "DataAgent", "action": "analyze_csv", "args": ["data.csv"]})
            
        if "code" in request_lower or "refactor" in request_lower:
            steps.append({"agent": "CoderAgent", "action": "improve_content", "args": ["# code here"]})
            
        if "research" in request_lower or "search" in request_lower:
            steps.append({"agent": "ResearchAgent", "action": "search_and_summarize", "args": [request]})
            
        # Default fallback
        if not steps:
            steps.append({"agent": "KnowledgeAgent", "action": "scan_workspace", "args": ["/"]})
            
        return steps

    def summarize_plan(self, steps: List[Dict[str, Any]]) -> str:
        """Core summary logic."""
        summary_lines = ["Plan:"]
        for i, step in enumerate(steps):
            summary_lines.append(f"{i+1}. {step.get('agent')} -> {step.get('action')}")
        return "\n".join(summary_lines)
