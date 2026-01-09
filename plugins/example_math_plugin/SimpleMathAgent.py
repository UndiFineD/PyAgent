from src.classes.base_agent import BaseAgent
from src.classes.orchestration.ToolRegistry import as_tool
from typing import Any, Dict

class SimpleMathAgent(BaseAgent):
    """
    An example community plugin for simple math operations.
    Demonstrates dynamic discovery and tool registration.
    """
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self._language = "python"

    @as_tool
    def quick_add(self, a: float, b: float) -> float:
        """Adds two numbers instantly."""
        return a + b
    
    @as_tool
    def quick_mult(self, a: float, b: float) -> float:
        """Multiplies two numbers instantly."""
        return a * b

    def improve_content(self, prompt: str) -> str:
        """Default execution logic."""
        return "SimpleMathAgent: I am ready to calculate. Use my tools 'quick_add' or 'quick_mult'."
