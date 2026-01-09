#!/usr/bin/env python3

"""Container for shared state and context between agents in a workflow."""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

@dataclass
class WorkflowState:
    """Maintains context, variables, and history for a multi-agent session."""
    task_id: str
    original_request: str
    variables: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)
    context_snippets: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    
    def set(self, key: str, value: Any) -> None:
        self.variables[key] = value
        
    def get(self, key: str, default: Any = None) -> Any:
        return self.variables.get(key, default)
    
    def add_history(self, agent: str, action: str, result: str) -> None:
        self.history.append({
            "agent": agent,
            "action": action,
            "result": result[:500] + "..." if len(result) > 500 else result
        })
